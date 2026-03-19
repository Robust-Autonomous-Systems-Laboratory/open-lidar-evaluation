cmake_minimum_required(VERSION 3.0.2)
project(repeatability_processing)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  roscpp
  std_msgs
  sensor_msgs
  pcl_conversions
  pcl_ros
  jsk_recognition_msgs
  dynamic_reconfigure
)


generate_dynamic_reconfigure_options(
  cfg/BoxParams.cfg
)



catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES box_filter
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib

# might need to add dynamic_reconfigure here?

)

###########
## Build ##
###########

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/box_filter.cpp
# )

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
# add_executable(${PROJECT_NAME}_node src/box_filter_node.cpp)

add_executable(pcl_box_filter src/pcl_box_filter.cpp)
add_executable(dynamic_param_box_filter src/dynamic_param_box_filter.cpp)

target_link_libraries(pcl_box_filter ${catkin_LIBRARIES})
target_link_libraries(dynamic_param_box_filter ${catkin_LIBRARIES})

add_dependencies(pcl_box_filter ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS} ${PROJECT_NAME}_gencfg)
add_dependencies(dynamic_param_box_filter ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS} ${PROJECT_NAME}_gencfg)

catkin_install_python(PROGRAMS src/target_processor.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)