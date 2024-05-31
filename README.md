

[//]: # (<img src="openai2.png" alt="openai" width="85"/><img src="https://github.com/devicons/devicon/raw/master/icons/docker/docker-original.svg" alt="docker" width="100"/><img src="https://github.com/devicons/devicon/raw/master/icons/python/python-original.svg" alt="python" width="90"/> )
<img src="openai2.png" alt="openai" width="85"/> <img src="docker-mark-blue.svg" alt="docker" width="100"/><img src="https://github.com/devicons/devicon/raw/master/icons/python/python-original.svg" alt="python" width="90"/> 


# Demo Weather app using OpenAI - _Function Calling_
## Python code and Docker Image

This is a customizable Weather app using OpenAI [function calling](https://platform.openai.com/docs/guides/function-calling)

# Retrieval-Augmented Generation (RAG)

RAG allows real-time data and other data, that would not ordinarily be available to the LLM, to be incorporated into model generated responses.

There may be valid reasons to keep information out of the public domain and to only use it in controlled situations. 

Information may be new, and may have missed the last LLM build. For example, a car manufacturer has released a new car since the last build and wants to make that information available.




The retrieved information, using predefined api's, is used to "augment" the model data to give more detailed responses.


RAG allows the model to consider data that was not originally known to the LLM. 






<img src="retrieval_augmented_generation_rag.png" alt="openai rag" width="500"/>



The example OpenAI [Code](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models) has been modified to:

1. modify the content for my use case, add actual real-time weather (openweather) and add prompt
2. make a Docker Hub repository `rbenson789/demo_openai_weather`

The repository on Docker Hub can be pulled and run on a local machine.

```console
docker pull rbenson789/demo_openai_weather
docker run -i rbenson789/demo_openai_weather
```

Weather data is supplied by openWeather api calls.

The user is invited to enter a natural language prompt, free format, with suggested guidelines.

OpenAI will determine the model arguments for building JSON for calls to a weather api. 
The setting up, and processing the return data will be handled by the model. 
The actual api call itself is a predefined api.
In this case, openweather api calls are used to augment model data. 

Any other weather agency could be used to fulfil the user requirements. 

In the example code, 3 locations are used in the prompt, detected by the model, 3 api calls return data to the model.

Using the information in the user prompt, the model will make a response using context and inferences.

<img src="model_api_function_calling.png" alt="openai model prompt api" width="500"/>

[//]: # (![model_api_function_calling.png]&#40;model_api_function_calling.png&#41;)


## Customisable Prompt
### Usage

```console
    What's the weather like in <location 1> <location 2> [<location>...] 
    [% chance of rain, sun index] [language] 
    [metric | imperial]
```



## OpenAI Tools/Functions

**Function calling** uses defined functions that the model calls to retrieve relevant data. The functions and respective arguments are defined.
The model determines the function to call by the information available to it, using input, context and inference. 

If the prompt is asking for weather, it will call the _get_current_weather_ function.
If the prompt is looking for probability of rain, it will call the _get_rain_probability_ function.

### longitude and latitude ? 

The api requests to openWeather require longitude and latitude to return JSON formatted weather results for that area. 

These have not been supplied by the user nor derived within the Python code. 

The model has been asked to supply these as required arguments to build JSON for api calls. 
By using input locations, context and inference, the model can determine these.

## Prompt
Creating a good prompt is important. A good prompt can significantly enhance the quality of the model's output.

Be specific and avoid unnecessary information that may distract from the main task.

This example would expect to _see_ locations, language, percentage, units in the prompt. A vague and unspecific prompt may give vague results. 

```python
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
```
### Example prompt
```console
    What's the weather like in Sydney, Paris and Dublin, % chance of rain, in imperial units 
```

## Prompt and Response


### request weather in 3 cities

Using the example prompt,the model has detected that there are 3 locations in the prompt and has extracted model arguments for api calls.


### Response
```console
### Weather Summary

#### Sydney, Australia
- **Weather**: Clear sky in the morning, with partly cloudy in the afternoon.
- **Temperature**: 18.49°F
  - Feels Like: 17.73°F (day), 16.43°F (night), 19.18°F (evening), 11.2°F (morning)
- **Humidity**: 51%
- **Wind**: 13.65 mph from the NNE (13°)
- **Rain Probability**: 0%
- **UV Index**: 3.25

#### Paris, France
- **Weather**: Partly cloudy with rain.
- **Temperature**: 13.61°F
  - Feels Like: 13.53°F (day), 15.73°F (night), 14.5°F (evening), 12.94°F (morning)
- **Humidity**: 96%
- **Wind**: 10.16 mph from the SW (219°)
- **Rain Probability**: 100%
- **UV Index**: 1.95

#### Dublin, Ireland
- **Weather**: Partly cloudy with rain.
- **Temperature**: 16.06°F
  - Feels Like: 15.65°F (day), 12.3°F (night), 14.03°F (evening), 11.26°F (morning)
- **Humidity**: 74%
- **Wind**: 13.33 mph from the WSW (259°)
- **Rain Probability**: 100%
- **UV Index**: 4.72

Make sure to carry an umbrella in Paris and Dublin!
```
### Language
Prompt asking for output to be in Japanese 

```console
Enter prompt: what's the weather like in singapore, % chance of rain, 
sun index in Japanese in imperial units
```
response

```console
### シンガポールの天気
- **説明**: 晴れ間もあるが、雨が予想される
- **気温**: 30.15°F
- **体感温度**:
  - 日中: 35.16°F
  - 夜: 33.15°F
  - 夕方: 33.55°F
  - 朝: 33.45°F
- **湿度**: 69%
- **風速**: 10.98マイル/時
- **風向**: 199°

### 雨の確率と紫外線指数
- **雨の確率**: 100%
- **紫外線指数 (UVI)**: 8.72

全天候に備え、十分な対策をお取りください。
```
In English, using Google Translate:

```console
### Singapore Weather
- **Description**: Sunny with rain expected
- **Temperature**: 30.15°F
- **Feels like**:
- Day: 35.16°F
- Night: 33.15°F
- Evening: 33.55°F
- Morning: 33.45°F
- **Humidity**: 69%
- **Wind Speed**: 10.98 miles per hour
- **Wind Direction**: 199°

### Chance of Rain and UV Index
- **Chance of Rain**: 100%
- **Ultraviolet Ray Index (UVI)**: 8.72

Please be prepared for all weather conditions and take adequate precautions.
```


<img src="docker-logo-blue.svg" alt="dockerfile to container png" width="200"/>












## Dockerfile

```Dockerfile 
FROM python:3.12.1-slim

ARG A_weather_api_key
ARG A_openai_api_key

ENV WEATHERMAP_API_KEY3=$A_weather_api_key
ENV OPENAI_API_KEY=$A_openai_api_key


# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Command to run the script
CMD ["python", "main.py"]
```

### standard build 

`docker build -t weather/demo_openai_weather:1.0 .`

#### set up api keys in the build

`docker build --build-arg A_weather_api_key=<your key> --build-arg A_openai_api_key=<your key> -t weather/demo_openai_weather:1.0 .`

## Build image for Docker Hub
The name of the image on Docker Hub will be userid/repository name
`userid/repository name`

e.g. 
`docker build --build-arg A_weather_api_key=<key> --build-arg A_openai_api_key=<key> -t rbenson789/demo_openai_weather .`

## Run Image



`docker run -i  rbenson789/demo_openai_weather`

<img src="docker_hub.png" alt="dockerfile to container png" width="600"/>


## login on local device

`Docker login`
enter user id and password


## Push Image to Docker Hub

`docker push rbenson789/demo_openai_weather`


## Pull Image from Docker Hub

`docker pull rbenson789/demo_openai_weather`

### run
#### interactive: -i

`docker run -i rbenson789/demo_openai_weather`


## Useful Docker Commands (local)

<img src="docker_commands.png" alt="dockerfile to container png" width="400"/>

### remove container by status


`docker rm -v $(docker ps --filter status=exited -q)`

## Summary of Docker Hub commands

The image name will be a concatenation of the user id and repository name.

`userid/repository name`

```console
docker build --build-arg A_weather_api_key=<key> --build-arg A_openai_api_key=<key> -t rbenson789/demo_openai_weather .

docker login

docker push rbenson789/demo_openai_weather

docker run -i  rbenson789/demo_openai_weather

docker pull rbenson789/demo_openai_weather

```

 






