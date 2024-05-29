



<img src="docker.png" alt="drawing" width="200"/>   <img src="openai.png" alt="drawing" width="225"/>

Weather app using OpenAI function calling
Python Code 
[sample OpenAI function calling example](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)


The supplied openai code has been modified to:

1. modify the content for my use case
2. make a dockerhub repository `rbenson789/demo_openai_weather`

The repository on dockerhub can be pulled and run from a local machine.

# Demo Weather app using Docker and OpenAI

This is a Weather app using OpenAI function calling. 

The user is invited to enter a natural language prompt, free format, with suggested guidelines.

OpenAI will determine the model arguments for building JSON code for calls to a weather api and will call the relevant api's as appropriate for the prompt.

In the example code, 3 locations are used in the prompt, 3 api calls would therefore be expected to return data to the model.

Using the information in the user prompt, OpenAI will determine a considered response using context and inferences.

## Customisable Prompt
### Usage

![prompt.png](prompt.png)

## Prompt and Response

All output in the response has been created by OpenAI.

### request weather in 3 cities



![response_from_prompt.png](response_from_prompt.png)

### Request response in Japanese 
![response_japanese.png](response_japanese.png)

## Docker Hub 

### pull from Docker Hub

`docker pull rbenson789/demo_openai_weather`

### run
#### interactive: -i

`docker run -i weather/demo_ai_app:1.0`


# Background

## Getting the app to dockerhub.


## Build Image (local)

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

`docker build -t weather/demo_openai_weather:1.0 .`

`docker build --build-arg A_weather_api_key=<your key> --build-arg A_openai_api_key=<your key> -t weather/demo_openai_weather:1.0 .`



## Run Image

`docker run -i  rbenson789/demo_openai_weather`

## input from keyboard:   -i





## otherwise
`docker run weather/demo_ai_app:1.0`

## Images

`docker images`

## Remove Image

`docker rmi <docker_image_id> --force`

## Useful Docker Commands

|                            |                                |        Comment |
|----------------------------|:------------------------------:|---------------:|
| Build Image                | docker build -t <image_name> . |                |
| Run Image                  |   docker run -i <image_name>   | -i interactive |
| List Images                |       docker image list        |                |
| Remove Image               | docker image rm <image_id> -f  | -f means force |
| Remove all dangling images |       docker image prune       |                |


### remove container by status


`docker rm -v $(docker ps --filter status=exited -q)`




