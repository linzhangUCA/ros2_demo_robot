from xmlrpc.client import boolean
from ament_index_python.packages import get_package_share_path
import launch
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Package and file paths
    urdf_package_path = get_package_share_path('demobot_description')
    model_path = urdf_package_path / 'urdf/demobot.urdf.xacro'
    rviz_config_path = urdf_package_path / 'rviz/demobot.rviz'
    gazebo_package_path = get_package_share_path('demobot_gazebo')
    world_path = gazebo_package_path / 'worlds/demo_world.sdf'

    # Launch arguments
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=str(model_path),
        description="Absolute path to robot urdf file",
    )
    sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        choices=['true', 'false'],
        description="Flag to enable use simulation time",
    )
    rviz_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=str(rviz_config_path),
        description="Absolute path to rviz config file",
    )

    # Launch node, process, other launch
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]), value_type=str
    )
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'robot_description': robot_description,
            }
        ],
    )
    gazebo_process = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            str(world_path),
        ],
        output='screen',
    )
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity',
            'demobot',
            '-topic',
            'robot_description',
            '-x',
            '0.0',
            '-y',
            '0.0',
            '-z',
            '0.0',
        ],
        output='screen',
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return launch.LaunchDescription(
        [
            sim_time_arg,
            model_arg,
            rviz_arg,
            robot_state_publisher_node,
            gazebo_process,
            spawn_entity,
            rviz_node
        ]
    )
