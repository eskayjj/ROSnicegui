#!/bin/bash

#Building Package & running publisher
rosdep install -i --from-path src --rosdistro humble -y
colcon build --packages-select image_publisher
. install/local_setup.bash
cd ~/ROSnodejs/
ros2 run image_publisher image_publisher

