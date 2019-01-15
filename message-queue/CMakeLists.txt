cmake_minimum_required (VERSION 3.1.0)

project( test_messages VERSION 0.1.0 )

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTRA_FLAGS  "-DZMQ_BUILD_DRAFT_API")
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_EXTRA_FLAGS})
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS} -std=c++11 -O0 -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS} -std=c++11 -O3 -DNDEBUG")

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(SEND_ERROR "In-source builds are not allowed.")
endif ()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})


set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
find_package(Threads REQUIRED)

find_path(ZeroMQ_INCLUDE_DIR
        NAMES zmq.hpp
        PATHS ${CMAKE_SOURCE_DIR}/zmq/include
        )

message("include path ${ZeroMQ_INCLUDE_DIR}")

find_library(ZeroMQ_LIBRARY 
	NAMES zmq libzmq libzmq-static.a 
	PATHS ${CMAKE_SOURCE_DIR}/zmq/lib
	)

message("test")

message("lib path ${ZeroMQ_LIBRARY}")

#
# .end find_package
#

include_directories(${ZeroMQ_INCLUDE_DIR})

set(SRC_LIST messages.cpp
        json.h)
add_executable(${PROJECT_NAME} ${SRC_LIST})

target_link_libraries(${PROJECT_NAME}
                      ${ZeroMQ_LIBRARY}
                      Threads::Threads)

#
# END OF FILE
#
