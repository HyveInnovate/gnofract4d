cmake_minimum_required(VERSION 3.10)
project(tests)

set(CMAKE_CXX_STANDARD 17)

include_directories(${PROJECT_SOURCE_DIR})
include_directories(${PROJECT_SOURCE_DIR}/model)

FILE(GLOB MODELFILES ${PROJECT_SOURCE_DIR}/model/*.cpp)

set(CMAKE_CXX_FLAGS "-ffast-math")

# MAIN

# add_executable(testrunner )
add_library(testrunner SHARED test.cpp ${MODELFILES})

find_package(PNG REQUIRED)
include_directories(${PNG_INCLUDE_DIR})
target_link_libraries(testrunner ${PNG_LIBRARY})

find_package(JPEG REQUIRED)
include_directories(${JPEG_INCLUDE_DIR})
target_link_libraries(testrunner ${JPEG_LIBRARY})

find_package(Threads REQUIRED)
target_link_libraries(testrunner ${CMAKE_THREAD_LIBS_INIT})

target_link_libraries(testrunner ${CMAKE_DL_LIBS})

add_definitions(-DTHREADS -D_REENTRANT -DPNG_ENABLED -DJPG_ENABLED)

find_library(CRUNCH_LIBRARY NAMES crunch++)
find_path(CRUNCH_INCLUDE NAMES crunch++.h)
include_directories(${CRUNCH_INCLUDE})
target_link_libraries(testrunner ${CRUNCH_LIBRARY})
message("crunch library ${CRUNCH_LIBRARY}, crunch path ${CRUNCH_INCLUDE}")

# FRACT_STDLIB

add_library(fract_stdlib SHARED
    ${PROJECT_SOURCE_DIR}/fract_stdlib.cpp
    ${PROJECT_SOURCE_DIR}/model/colorutils.cpp
    ${PROJECT_SOURCE_DIR}/model/colormap.cpp
    ${PROJECT_SOURCE_DIR}/model/image.cpp)

set_target_properties(fract_stdlib PROPERTIES PREFIX "")
set_target_properties(fract_stdlib PROPERTIES SUFFIX ".so")
