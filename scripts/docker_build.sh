#!/bin/bash
source ./properties.sh

docker build -t ${imagename}:${version} .