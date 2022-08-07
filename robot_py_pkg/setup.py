from setuptools import setup

package_name = 'robot_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/robot_py_pkg', ['robot_py_pkg/rules.yaml']),
        ('share/' + package_name + '/launch', ['launch/cici_launch.py']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dodo',
    maintainer_email='dodo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                "robotnode = robot_py_pkg.robotnode:main",
                "terrainnode = robot_py_pkg.terrainnode:main",
                "gamenode=robot_py_pkg.gamenode:main",
                "usersnode=robot_py_pkg.usersnode:main",
                "runnode=robot_py_pkg.runnode:main"
        ],
    },
)
