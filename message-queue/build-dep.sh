# build zmq
mkdir zmq-build
cd zmq-build
cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_DRAFTS=1 -DCMAKE_INSTALL_PREFIX=../zmq ../zeromq-4.2.0
make -j4
make install

# build zmq cpp binding
cd ..
mkdir cppzmq-build
cd cppzmq-build
cmake -DCMAKE_BUILD_TYPE=Release -DPC_LIBZMQ_VERSION="4.2.0" -DCMAKE_INSTALL_PREFIX=../zmq ../cppzmq 
make -j4
make install
