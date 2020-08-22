#!/bin/bash
version=1.0.2
tag=smugzombie/epicreminder
name=epicreminder

# Check if running
running=$(docker ps | grep "$name" | awk {'print $1'})

echo $running

if [[ ! -z "$running" ]]
then

        echo "Running Instance Found.. Stopping"
        docker stop $running
        echo "Deleting Image"
        docker rm $running

fi

# Build the image
docker build -t $tag:$version .

# Run the image
docker run -td --restart unless-stopped --name $name $tag:$version

