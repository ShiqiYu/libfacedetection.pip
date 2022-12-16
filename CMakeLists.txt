cmake_minimum_required(VERSION 3.4...3.18)
project(YuDet)

find_package(pybind11 REQUIRED)
pybind11_add_module(yudet src/main.cpp)

set(facedetection_LIBRARY_DIR "${PROJECT_SOURCE_DIR}/libfacedetection/lib/")
set(facedetection_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/libfacedetection/include/")
find_library(LIB_FACEDETECTION facedetection ${facedetection_LIBRARY_DIR})
include_directories(${facedetection_INCLUDE_DIR})
target_link_libraries(yudet PRIVATE ${LIB_FACEDETECTION})