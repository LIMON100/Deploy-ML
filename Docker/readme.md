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



### Build docker image

    docker build -t helmet_api .


### Run docker image

    dokcer run -p 8000:8000 helmet_api
    
or

    docker start "contanier_id"
 

### Delete docker image

    First delete the container 
    docker rm container-id
    
    Delete the docker-image
    docker rmi image-id
 
### Move docker to another folder

    1. open cmd as administrative
    2. wsl --shutdown
    3. wsl -l -v
    4. wsl --export docker-desktop-data H:\doc\dockerdesk.tar
    5. wsl --unregister docker-desktop-data
    6. wsl -l
    7. wsl --import docker-desktop-data H:\doc\ddesktop H:\doc\dockerdesk.tar
    
 
### problem:

ImportError: libgthread-2.0.so.0: cannot open shared object file: No such file or directory when importing cv2 using Docker container

#### Solution

https://stackoverflow.com/questions/53328226/im-unable-to-install-opencv-contrib-python-in-docker
