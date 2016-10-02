cmake_minimum_required(VERSION 3.0)
project(parser)

set(CMAKE_CXX_COMPILER "/usr/bin/clang++")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -O2")

set(SOURCE_FILES main.cpp Parser.cpp Parser.h)
add_executable(parser ${SOURCE_FILES})
