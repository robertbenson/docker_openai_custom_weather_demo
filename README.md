



<img src="docker.png" alt="drawing" width="200"/>   <img src="openai.png" alt="drawing" width="225"/>

Weather app using OpenAI function calling

# Demo Weather app using Docker and OpenAI

This is a Weather app using OpenAI function calling. 

## Customisable Prompt

![prompt.png](prompt.png)

## Prompt and Response

### request weather in 3 cities

![response_from_prompt.png](response_from_prompt.png)


## Docker Hub   (remote)

### pull from Docker Hub

`docker pull rbenson789/demo_openai_weather`

### run
#### interactive: -i

`docker run -i weather/demo_ai_app:1.0`


## Build Image (local)

### passing hidden keys

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

|  |                                |        Comment |
|--|:------------------------------:|---------------:|
|  |                                |                |
| Build Image | docker build -t <image_name> . |                |
| Run Image |   docker run -i <image_name>   | -i interactive |
| List Images |       docker image list        |                |
| Remove Image | docker image rm <image_id> -f  | -f means force |
| Remove all dangling |       docker image prune       |                |
|  |                                |                |
|  


### remove container by status


`docker rm -v $(docker ps --filter status=exited -q)`




