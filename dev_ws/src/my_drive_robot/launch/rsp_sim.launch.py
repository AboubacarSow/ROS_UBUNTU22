import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


   
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_drive_robot' 
    pkg_path=get_package_share_directory(package_name)
    gazebo_pkg_path=get_package_share_directory('gazebo_ros')
    
    rspPath=os.path.join(pkg_path,
                         'launch','rsp.launch.py')
    gazeboPath=os.path.join(gazebo_pkg_path, 
                            'launch', 'gazebo.launch.py')

     # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    #Equivalent= ros2 launch my_drive_robot rsp.launch.py use_sim_time:=true
    rsplaunchfile = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([rspPath]), 
                launch_arguments={'use_sim_time': 'true'}.items())

    # Include the Gazebo launch file, provided by the gazebo_ros package
        #Equivalent= ros2 gazebo_ros gazebo.launch.py
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([gazeboPath]),)

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    #Equivalent= ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity nameofentity
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description','-entity', 'my_bot'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        rsplaunchfile,
        gazebo,
        spawn_entity,
    ])