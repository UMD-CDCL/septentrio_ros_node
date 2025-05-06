from setuptools import find_packages, setup

package_name = 'septentrio_ros_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='srijal',
    maintainer_email='srijal@umd.edu',
    description='TODO: Package description',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nmea_serial_driver = septentrio_ros_node.nmea_serial_driver:main'
        ],
    },
)
