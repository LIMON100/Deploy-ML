# Docker

## What is a Docker Image

A Docker image is an immutable (unchangeable) file that contains the source code, libraries, dependencies, tools, and other files needed for an application to run.


## What is a Docker Container

A Docker container is a virtualized run-time environment where users can isolate applications from the underlying system. These containers are compact, portable units in which you can start up an application quickly and easily.

A container is, ultimately, just a running image. Once you create a container, it adds a writable layer on top of the immutable image, meaning you can now modify it.


From node:12.16.3 (node version build with docker)
WORKDIR /code (working directory)
ENV PORT 4002/80
COPY package.json /code/package.json
RUN npm install
COPY . /code
CMD [ "node", "src/server.js" ]
