# Gigibots Project 
The project is a playground created on ROS2 for robotics enthusiasts. The aim of the project is to enable learning image processing, path planning, search, and SLAM using no real-life sensors.

# HOW?
At the top of the playground, there is a camera to keep track of the instantaneous pose of the robots and obstacles. Then from the pose info a digital twin is created (https://github.com/cankancelik/gigibots_webots) in the WEBOTS environment and sensors are attached to each robot and sensor data info is shared to the user hence user can work with the data and apply any kind of algorithms that is desired.

# Nodes to be Manipulated
The game node and user node can be altered. The game node is where the tasks, rules, and sensor specifications are determined by the game master. The user node is the node where users can obtain sensors and other required info published by the game master in order to implement their algorithm.

# Shared Data
Lidar Data
The camera attached on the Robot
Cut Map 
(For easier image processing, the user may be provided bird' eye view map from its position to the limits of the map with a slice of the determined field of view)
Player ID & TYPE

# RQT GRAPH
![rosgraph](https://user-images.githubusercontent.com/68663676/183301031-0190196c-4d51-473f-9b7a-0c2cfcfb0284.jpg)


