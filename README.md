# Images diff checker

All commands are sensible to the directory they are executed from. So please use the README directory for that

# Architecture

I have decided to implement 3 different microservices. All of them uses API servers implemented in Flask. The first one is the frontend. Should only manage browser queries. Despite it is using storage to save the images, in a future it shouldn't. This is the only microservice exposed to the user.

The second service is the backend. It will be the only one with heavy CPU load because it is the one processing the images. As it is done in the frontend it is saving images to disk, but that can be improved to save time and speed up the process

Optionally the backend can connect with the storage service. Actually it is only saving the images in different directories, but at some point should have a UI or a database so the images can be explored.

With this architecture every single process is separated and with a bit of extra work adding a messaging software(like rabbitMQ) it should be possible to decouple them a bit more. That will give as the possibility of increasing and decreasing the number of container on each layer, without any special configuration.

# Known issues

The backend is not sending the images correctly to storage and to the frontend. Because of that, the images saved in the storage cannot be open and the frontend doesn't show it. Testing the storage separately can be seen that the images are stored properly

# Start the environment

    docker-compose up --build

# Quick test of the code

This command will start the environment, check that the service is working and stop it. I would like to have something more useful, but given that the output images are not the correct, it hard to do the end to end test.

    ./quick_test.sh

# Microservices
This section explain how to run and test each microservice separately

## Docker images

Flask image is being used for the 3 microservices. A fixed version is being used to ensure it doesn't change by mistake.
Documentation: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask

## Storage

### Build

    docker build -t storage storage/

### Test

Create volume that will be used for testing

    mkdir -p test_storage

Run the container:

    docker run --rm --name storage -v ${PWD}/test_storage:/var/images -p 8888:80 storage

Test upload images:

    curl -X POST -F "image1=@testImages/penguin1.png" -F"image2=@testImages/penguin2.png" localhost:8888/api/store

The files should have been uploaded in test_storage directory

## Backend

### Build

    docker build -t backend backend/.

### Test

Start conteiner. By default the storage is disabled:

    docker run --rm --name backend -p 8080:80 backend

Test the container

    curl -X POST -F "image1=@testImages/penguin1.png" -F"image2=@testImages/penguin2.png" localhost:8080/api/process

### Integration test

Create volume that will be used for testing

    mkdir -p test_storage

To test the integration with storage it is needed to start both container and connect them:


    docker run --rm --name storage -v ${PWD}/test_storage:/var/images -p 8888:80 storage
    docker run --rm --name backend -e STORE=true -e STORAGE_SERVER=http://storage/api/store -p 8080:80 backend
    docker network create -d bridge --subnet 172.26.0.0/16 mynetwork
    docker network connect mynetwork storage
    docker network connect mynetwork backend

Test the container

    curl -X POST -F "image1=@testImages/penguin1.png" -F"image2=@testImages/penguin2.png" localhost:8080/api/process

Appart of a response with the boxes and an image, a UUID directory with the images should have been created in test_storage directory

Remove test network:

    docker network disconnect mynetwork backend
    docker network disconnect mynetwork storage
    docker network rm mynetwork

## Frontend
### Build

    docker build -t frontend frontend/.

### Test

    docker run --rm --name frontend -p 80:80 frontend
    curl localhost

### Backend integration test

    docker run --rm --name backend -e STORE=false -p 8080:80 backend
    docker run --rm --name frontend -p 80:80 -e BACKEND_SERVER=http://backend/api/process frontend
    docker network create -d bridge --subnet 172.25.0.0/16 backend_network
    docker network connect backend_network frontend
    docker network connect backend_network backend

Execute this to send images to the frontend API to get the HTML response:

    curl -X POST -F "image1=@testImages/penguin1.png" -F"image2=@testImages/penguin2.png" localhost:80/uploader

Alternatively go to a browser, url: 'http://localhost' and use the UI

Remove test network:

    docker network disconnect backend_network backend
    docker network disconnect backend_network frontend
    docker network rm backend_network

### Integration tests

As integration test it is recommended to use docker-compose

    docker-compose up --build

Go to the UI

# TODO

Add unit tests
Solve the big bug when sending the diff image to the frontend
Add a messages brocker(like rabbitMQ) between each microservice
Implement in to Kubernetes

## Frontend

Manage error codes
Improve logging
Better UI
Check that the images size is the same
Move javascript to a separate file
/api/diff method should be able to send the images to the backend without saving them as a file
Split diff method in different methods
The dif should be an API returning a Json not an HTML

## Backend

Manage error codes
Improve logging
Use JSON for the POST instead of a form
Parallelize sending the image to storage with responding frontend

## Storage

Manage error codes
Improve logging
Use JSON for the POST instead of a form
Creating a UI for the storage, so the images are browsable
Creating a database for the images, so it can be query
