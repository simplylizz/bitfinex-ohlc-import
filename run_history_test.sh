#!/bin/bash

docker run \
    -v `pwd`:/app \
    -it --rm \
    bitfinex \
    python trade/main.py
