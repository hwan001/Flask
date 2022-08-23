#!/bin/bash
source ./properties.sh

docker push ${imagename}:${version}

