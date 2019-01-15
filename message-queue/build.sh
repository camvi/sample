#!/bin/bash
if [ -e zmq ]
then
    echo "building..."
else
    echo "Can't find zmq build output. Please run build-dep.sh first."
    exit 0
fi

mkdir -p build-release
cd build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j4

