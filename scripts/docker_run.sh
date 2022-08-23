#!/bin/bash
source ./properties.sh

docker run -it --network=host ${imagename}:${version}
