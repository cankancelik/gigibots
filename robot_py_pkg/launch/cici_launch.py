#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
#    package_dir = get_package_share_directory('robot_py_pkg')
#    robot_description = pathlib.Path(os.path.join(package_dir, 'robot_py_pkg', 'rules.yaml')).read_text()
    # include another launch file

    cam2image = Node(
            package='image_tools',
            executable='cam2image'
        )
    gamenode = Node(
            package='robot_py_pkg',
            executable='gamenode'
        )
    robotnode = Node(
            package='robot_py_pkg',
            executable='robotnode'
        )
    terrainnode = Node(
            package='robot_py_pkg',
            executable='terrainnode'
        )
    usersnode = Node(
            package='robot_py_pkg',
            executable='usersnode'
        )
    runnode = Node(
            package='robot_py_pkg',
            executable='runnode'
        )
    
    return LaunchDescription([
        cam2image,
        terrainnode,
        robotnode,
        gamenode,
        usersnode,
        runnode,
        
        
    ])