#!/bin/bash

docker run \
    -v `pwd`:/app \
    -it \
    --rm \
    bitfinex-tests \
    pytest -xs tests/trade
