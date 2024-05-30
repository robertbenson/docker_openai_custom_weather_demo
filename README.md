

<img src="openai2.png" alt="openai" width="85"/><img src="https://github.com/devicons/devicon/raw/master/icons/docker/docker-original.svg" alt="docker" width="100"/><img src="https://github.com/devicons/devicon/raw/master/icons/python/python-original.svg" alt="python" width="90"/> 


# Demo Weather app using Docker and OpenAI
Customizable Weather app using OpenAI [function calling](https://platform.openai.com/docs/guides/function-calling)

# Retrieval-Augmented Generation (RAG)

RAG incorporates real-time data into model generated responses.

The retrieved information, using predefined api's, is used to "augment" the model data to give more detailed responses.
RAG allows the model to consider data that was not originally known to the LLM. In this case, real-time weather information
is used. 


The example OpenAI [Code](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models) has been modified to:

1. modify the content for my use case
2. make a dockerhub repository `rbenson789/demo_openai_weather`

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

In the example code, 3 locations are used in the prompt, 3 api calls would are expected to return data to the model.

Using the information in the user prompt, the model will make a response using context and inferences.






## Customisable Prompt
### Usage

```console
    What's the weather like in <location 1> <location 2> [<location>...] 
    [% chance of rain, sun index] [language] 
    [metric | imperial]
```

### Example prompt
```console
    What's the weather like in Sydney, Paris and Dublin, % chance of rain, in imperial units 
```

## Prompt and Response


### request weather in 3 cities

Using the example prompt,the model has detected that there are 3 locations in the prompt and has extracted model arguments for api calls.

### longitude and latitude ? 
The api requests to openWeather require longitude and latitude to return json formatted weather results for that area. 

These have not been supplied by the user nor derived within the Python code. 

The model has been asked to supply these as required arguments to build JSON for api calls.

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
## Language
Prompt ran asking for output to be in Japanese 

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


## Docker Hub 

### pull from Docker Hub

`docker pull rbenson789/demo_openai_weather`

### run
#### interactive: -i

`docker run -i weather/demo_ai_app:1.0`


# Background

## Getting the app to Docker Hub.

<img src="dockerfile_container.png" alt="dockerfile to container png" width="600"/>

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

### passing hidden keys

do not expose api keys. 

#### standard build 

`docker build -t weather/demo_openai_weather:1.0 .`

#### set up api keys in the build

`docker build --build-arg A_weather_api_key=<your key> --build-arg A_openai_api_key=<your key> -t weather/demo_openai_weather:1.0 .`



## Run Image

`docker run -i  rbenson789/demo_openai_weather`

## input from keyboard:   -i


# Push to Docker Hub

`docker push rbenson789/demo_openai_weather`


## Useful Docker Commands (local)

|                            |                                |        Comment |
|----------------------------|:------------------------------:|---------------:|
| Build Image                | docker build -t <image_name> . |                |
| Run Image                  |   docker run -i <image_name>   | -i interactive |
| List Images                |       docker image list        |                |
| Remove Image               | docker image rm <image_id> -f  | -f means force |
| Remove all dangling images |       docker image prune       |                |


### remove container by status


`docker rm -v $(docker ps --filter status=exited -q)`

## Summary of Docker Hub commands

The build will be a concatenation of the user id and repository name.

`userid/repository name`

```console
docker build --build-arg A_weather_api_key=<key> --build-arg A_openai_api_key=<key> -t rbenson789/demo_openai_weather .

docker login

docker push rbenson789/demo_openai_weather

docker run -i  rbenson789/demo_openai_weather

docker pull rbenson789/demo_openai_weather

```






