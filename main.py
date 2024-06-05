import json
import os
import requests
import sys
import signal

from openai import OpenAI
from dotenv import load_dotenv
from openai.lib.streaming import AssistantEventHandler
from openai.types.beta import assistant
from typing_extensions import override

client = OpenAI()
load_dotenv('.env')

def graceful_shutdown(signum, frame):
    print("Received SIGTERM signal. Performing cleanup...")
    # Perform cleanup here
    sys.exit(0)

# Register the SIGTERM signal handler
signal.signal(signal.SIGTERM, graceful_shutdown)

def convert_wind_speed(wind_speed, unit):
    """wind speed will be in meters per second. Convert to unit accordingly"""
    if unit.lower() == 'metric':
        return wind_speed * 3.6
    elif unit.lower() == 'imperial':

        # 1 mile per day = 1.60934 km/h
        return wind_speed * 2.23694
    else:
        return "Invalid unit. Please provide 'km/h' or 'mph'."


def get_current_weather(latitude, longitude, lang, units):
    """Get the current weather in a given latitude and longitude."""
    base = "https://api.openweathermap.org/data/3.0/onecall"
    key = os.getenv('WEATHERMAP_API_KEY3.0')
    key = os.getenv('WEATHERMAP_API_KEY')

    request_url = f"{base}?lat={latitude}&lon={longitude}&appid={key}&units=metric&lang={lang}&units={units}"

    response = requests.get(request_url)
    data = response.json()

    weather_daily_summary = data['daily'][0]['summary']
    weather_daily_humidity = data['daily'][0]['humidity']
    weather_daily_wind_speed = data['daily'][0]['wind_speed']
    weather_daily_wind_speed = convert_wind_speed(weather_daily_wind_speed,
                                                  units)
    weather_daily_wind_degree = data['daily'][0]['wind_deg']
    weather_daily_temperature = data['daily'][0]['temp']['day']
    weather_daily_uvi = data['daily'][0]['uvi']
    weather_daily_temperature_feels_like = data['daily'][0]['feels_like']

    result = {
        "description": weather_daily_summary,
        "temperature": weather_daily_temperature,
        "uvi": weather_daily_uvi,
        "humidity": weather_daily_humidity,
        "wind_speed": weather_daily_wind_speed,
        "wind_direction": weather_daily_wind_degree,
        "latitude": latitude,
        "longitude": longitude,
    }
    # print(result)
    return json.dumps(result)


def get_rain_probability(latitude, longitude):
    """Get the probability of rain in a given latitude and longitude"""
    base = "https://api.openweathermap.org/data/3.0/onecall"
    key = os.getenv('WEATHERMAP_API_KEY3.0')
    request_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid=61b0dd3842dc8e76fb2335d59de1570f"

    response = requests.get(request_url)
    data = response.json()

    weather_daily = data['daily'][0]
    weather_daily_summary = data['daily'][0]['summary']
    weather_daily_pop = data['daily'][0]['pop']

    result = {
        "latitude": latitude,
        "longitude": longitude,
        "probability": weather_daily_pop,
        # "uvi": weather_daily_uvi,
        "summary": weather_daily_summary,
    }

    return json.dumps(result)


class EventHandler(AssistantEventHandler):
    @override
    def on_event(self, event):
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            # print(f"Tool name: {tool.function.name}")
            # print(f"Tool arguments: {tool.function.arguments}")

            if tool.function.name == "get_current_temperature":
                tool_outputs.append({"tool_call_id": tool.id, "output": "57"})
                # print("tool outputs: ", tool_outputs)
            elif tool.function.name == "get_rain_probability":
                # print(f"\n\n Tool name: {tool.function.name}")
                # print(f"Tool arguments: {tool.function.arguments}")
                json_object = json.loads(tool.function.arguments)
                latitude = json_object["latitude"]
                longitude = json_object["longitude"]

                output = get_rain_probability(latitude, longitude)
                tool_outputs.append(
                    {"tool_call_id": tool.id, "output": output})
            elif tool.function.name == "get_current_weather":
                json_object = json.loads(tool.function.arguments)
                latitude = json_object["latitude"]
                longitude = json_object["longitude"]

                try:
                    language = json_object["language"]
                except KeyError:
                    language = "en"

                try:
                    units = json_object["unit"]
                except KeyError:
                    units = "metric"

                output = get_current_weather(latitude, longitude, language,
                                             units)
                tool_outputs.append(
                    {"tool_call_id": tool.id, "output": output})
                # print("tool outputs: ", tool_outputs)
            else:
                print("Error if here !!!!")

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()


def setup(prompt: str):
    assistant = client.beta.assistants.create(
        instructions="You are a weather bot. Use the provided functions to answer questions. Add a detailed description of the precautions to take for that particular uvi. All output should be in requested language. Add an emoji for the weather eg sun for sunshine. The output should be in a table format with metrics down and locations across",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given latitude and longitude",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "string",
                                "description": "The latitude of a place",
                            },
                            "longitude": {
                                "type": "string",
                                "description": "The longitude of a place",
                            },
                            "language": {
                                "type": "string",
                                "description": "The language to respond with eg en for English, nl (Dutch), fr (French), sp (Spanish), ru (Russian), uk (Ukrainian)",
                            },
                            "unit": {"type": "string",
                                     "description": "measurements in either imperial or metric",
                                     "enum": ["imperial", "metric"]},

                        },
                        "required": ["latitude", "longitude"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_rain_probability",
                    "description": "Get the probability of rain in a given latitude and longitude",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "string",
                                "description": "The latitude of a place",
                            },
                            "longitude": {
                                "type": "string",
                                "description": "The longitude of a place",
                            },
                        },
                        "required": ["latitude", "longitude"],
                    }
                }
            },

        ]
    )

    # create a thread
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler()
    ) as stream:
        stream.until_done()


if __name__ == '__main__':
    """Keep prompting the user to enter their input until they quit"""

    while True:
        try:
            content_example_1 = \
                "What's the weather like in <location 1> <location 2> [<location>...] [% chance of rain] [language] [metric | imperial]"

            content_quit = "Quit: Q and then Ctrl c"

            print(80 * '*')
            print(80 * '*')

            print("\n")
            print(content_example_1)
            print("\n")
            print(content_quit)
            print("\n")
            prompt = input("Enter prompt: ")
            if prompt == "Q" or prompt == "quit" or prompt == "exit" or prompt == "q":
                print("\n")
                print("Bye")
                break
            else:
                setup(prompt)
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting...")
            break
