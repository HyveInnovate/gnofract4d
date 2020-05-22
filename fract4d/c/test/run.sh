#!/bin/sh

docker build fract4d/c -f fract4d/c/test/Dockerfile -t fract4dc_test:1.0.0
docker run --rm -it fract4dc_test:1.0.0 bash -c "crunch++ libtestrunner"
