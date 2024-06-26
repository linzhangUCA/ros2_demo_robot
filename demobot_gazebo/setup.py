import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'demobot_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join("share", package_name, "launch"), glob(os.path.join("launch", "*"))),
        (os.path.join("share", package_name, "worlds"), glob(os.path.join("worlds", "*"))),
        (os.path.join("share", package_name, "configs"), glob(os.path.join("configs", "*"))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pbd0',
    maintainer_email='lzhang12@uca.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
