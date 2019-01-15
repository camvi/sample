# Simple message queue implementation

This is a sample application that subscribes to events from Camvi 
face recognition engine and prints out some event information as it 
receives them.

## To Build

```
./build-dep.sh
./build.sh
```

## To Test

You must be on the same machine as the Camvi engine. Note you CAN subscribe to
messages from Camvi engine running elsewhere in the network - you just need
to change the code slightly.
```
cd build-release
./test_messages
```

Now if the camera is running on the Camvi engine, events will be printed out. Here is some
sample output:

```
Waiting to receive message...
received {"camera": "webcam","time": "2019-01-15T17:57:28.588","type": "ADD","persons":[{"enabled":true,"details":[{"key":"height","value":"202"},{"key":"location","value":"home"}],"person":42871,"name":"Steven0709","creation":"2018-07-09 14:05:47","log":3573}]}
Event ADD
Camera webcam
Person ID 42871
Waiting to receive message...
received {"camera": "webcam","time": "2019-01-15T17:57:35.688","type": "OUT","persons":[{"enabled":true,"details":[{"key":"height","value":"202"},{"key":"location","value":"home"}],"person":42871,"name":"Steven0709","creation":"2018-07-09 14:05:47","log":3573}]}
Event OUT
Camera webcam
Waiting to receive message...
received {"camera": "webcam","time": "2019-01-15T17:57:35.697","type": "CLEARED"}
Event CLEARED
Camera webcam
Waiting to receive message...
```