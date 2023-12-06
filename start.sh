#!/bin/bash

# Set your image name
IMAGE_NAME="animal-exploration"

# Set the container name
CONTAINER_NAME="$IMAGE_NAME-instance"

# Optionally set the Dockerfile path if it's not in the current directory
DOCKERFILE_PATH="."

# Optionally set any additional build options
BUILD_OPTIONS=""

# Stop and remove existing containers
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# Remove the existing image
docker rmi $IMAGE_NAME 2>/dev/null

# Build the Docker image
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH/Dockerfile $BUILD_OPTIONS .

# Create and start a container based on the newly built image
docker run -d --name $CONTAINER_NAME $IMAGE_NAME
