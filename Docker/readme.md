# Docker

## What is a Docker Image

A Docker image is an immutable (unchangeable) file that contains the source code, libraries, dependencies, tools, and other files needed for an application to run.


## What is a Docker Container

A Docker container is a virtualized run-time environment where users can isolate applications from the underlying system. These containers are compact, portable units in which you can start up an application quickly and easily.

A container is, ultimately, just a running image. Once you create a container, it adds a writable layer on top of the immutable image, meaning you can now modify it.


### Docker Image

FROM node:12.16.3 (node version build with docker)/ Ubuntu linux - Base Image

COPY package.json /code/package.json - All files into a specific particular location which is present inside docker image

EXPOSE 4002/80

WORKDIR /code (working directory) - Same file where all files are located


RUN pip install -r requiremets.txt

CMD python app.py
