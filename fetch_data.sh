#!/bin/bash

docker run \
    -v `pwd`:/app \
    -it --rm \
    bitfinex \
    python bitfinex/main.py --debug /app/bitfinex.sqlite
