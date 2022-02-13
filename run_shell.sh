#!/bin/bash

docker run \
    -v `pwd`:/app \
    -it --rm \
    bitfinex \
    sh
