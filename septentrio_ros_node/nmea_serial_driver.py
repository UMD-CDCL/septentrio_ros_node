#! /usr/bin/env python

import rclpy
import septentrio_ros_node.driver
from rclpy.node import Node
import glob
import serial
import pyudev


class ros2_SeptentrioSerialHandler(Node):
    # Set our parameters and the default socket to open
    def __init__(self):
        super().__init__('septentrio_ros_node')
        self.port = ''
        self.septentrio = serial.Serial()
        self.device_connected = False
        self.context_ = pyudev.Context()
        self.declare_parameters(
            namespace='',
            parameters=[
                ('frame_gps', 'gps'),
                ('frame_timeref', 'gps'),
                ('use_rostime', True),
                ('use_rmc', False)]
        )

    # Should open the connection and connect to the device
    # This will then also start publishing the information
    def start(self):
        # Try to connect to the device
        self.connect_to_device()
        
        if not self.device_connected:
            self.get_logger().info("Could not connect to Mosaic X5 GPS")
            return

        try:
            driver = septentrio_ros_node.driver.RosNMEADriver(self)
        except Exception as e:
            self.get_logger().error("an error occured while trying to make the driver. Error was: %s." %e)

        try:
            while rclpy.ok():
                data = self.septentrio.readline()
                rclpy.spin_once(self, timeout_sec=0) # allow functions such as ros2 node info, ros2 param list to work
                try:
                    driver.process_line(data.decode('utf-8').rstrip().encode('utf-8').strip(b'\x00'))
                except ValueError as e:
                    self.get_logger().info("Value error, likely due to missing fields in the NMEA message. Error was: %s." % e)
        except Exception as e:
            self.get_logger().error("an error occured while reading lines from device. Error was: %s." %e)

    # Try to connect to the device, allows for reconnection
    # Will loop till we get a connection, note we have a long timeout
    def connect_to_device(self):
        self.get_logger().info("starting to poll.")
        device_list = self.context_.list_devices(subsystem='tty', ID_BUS='usb')

        for device in device_list:

            if device.properties['ID_VENDOR'] == 'Septentrio':
                port = device.properties['DEVNAME']  # Mosaic X-5 device has two ports, the first port found will correspond to the USB1 virtual port
                self.get_logger().info("Septentrio Mosaic X5 GPS device found at port = " + port)

                try:
                    self.septentrio = serial.Serial(port=port, baudrate=115200)
                    self.device_connected = True
                    break

                except Exception as e:
                    self.get_logger().error("Septentrio Mosaic X5 GPS serial connection attempt failed:")
                    self.get_logger().error(e)


def main(args=None):
	rclpy.init(args=args)

	node = ros2_SeptentrioSerialHandler()
	

	# Start the nodes processing thread
	node.start()

	# at termination of the code (generally with ctrl-c) Destroy the node explicitly
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
