cmake_minimum_required(VERSION 3.0.2)
cmake_policy(SET CMP0079 NEW)
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

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES box_filter
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(pcl_box_filter src/pcl_box_filter.cpp)
target_link_libraries(pcl_box_filter ${catkin_LIBRARIES})
add_dependencies(pcl_box_filter ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

catkin_install_python(PROGRAMS src/target_processor.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)