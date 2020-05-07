#!/usr/bin/env bash
docker-compose up -d --build
curl -X POST -F "image1=@testImages/penguin1.png" -F"image2=@testImages/penguin2.png" localhost:80/uploader
docker-compose down
