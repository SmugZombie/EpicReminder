#!/bin/bash
version=1.0.0
docker build -t smugzombie/epicreminder:$version .
docker run -td --restart unless-stopped smugzombie/epicreminder:$version 

