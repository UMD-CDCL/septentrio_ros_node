# Septentrio Mosaic X4 RTK ROS Node
This is a very simple ROS node that allows for publishing of NMEA messages onto the ROS framework.
This package aims to support the [Septentrio Mosaic X5 RTK GNSS](https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-x5) module by Septentrio.
Right now this supports all NMEA messages from the package, while some are not used to publish anything onto ROS.


## Quickstart Guide

1. Clone this package into your ROS workspace and build it
2. Turn on your Mosaic X5 RTK module
3. Make sure the module is configured correctly. Configuration page can be found at `192.168.3.1` on a browser with the Mosaic X5 connected over the USB C connection.
  * Enable L3 band by going to Admin > Expert Control > Control Panel > Navigation > Advanced User Setting > Signal/Satellite Tracking, and enable all satellite bands [Check all boxes].
  * Go to NMEA/SBF Out menu and add a new NMEA steam over USB1 with the `GGA`, `GST` and `VTG` messages at 100msec interval.
  * Go to Corrections menu and set RTCMv3 input on the USB2 port.
  * Go to GNSS menu and make sure the positioning mode is set to Rover, RTK enabled and reference position set to auto.
4. The node automatically finds the device serial port using pyudev (install `pip3 install pyudev` if not installed), and starts it. 
5. Run using `ros2 run septentrio_ros_node nmea_serial_driver`

## Driver Details

* Publishes GPS fix, velocity, and time reference
  * `/fix` - NavSatFixed
  * `/vel` - TwistedStamped
  * `/time` - TimeReference

## Credit

Original starting point of the driver was the ROS driver [nmea_navsat_driver](https://github.com/ros-drivers/nmea_navsat_driver) which was then expanded by [CearLab](https://github.com/CearLab/nmea_tcp_driver) to work with the Reach RTK. Migrated to ROS2 by [Bart Boogmans](https://github.com/bartboogmans/reach_ros_node).
This package is then modified from the [reach_ros_node](https://github.com/rpng/reach_ros_node) for Emlid Reach GNSS Modules to now work with Septentrio GNSS modules.






