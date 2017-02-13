#!/usr/bin/env python
# ROS Packages
import rospy

from xbee import XBee
import time
import serial
import sys
import threading
import serial
import io
import signal
import sys

class XBeeHandler(object):
    """docstring for XBeeHandler"""
    def __init__(self):
        """ TODO: ADD Error Handling """
        super(XBeeHandler, self).__init__()
        signal.signal(signal.SIGINT, self.signal_handler)
        # self.serial          = serial.Serial(self.port, self.baud)
        # self.xbee            = XBee(self.serial, callback=self.message_received)
        self.request_time    = None

    def init_port(self, port, baud):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baud)
            self.xbee = XBee(self.ser)
            return 0

        except Exception as e:
            print "Exception caught while openning the serial port"
            print e
            return -1

    def message_received(self, data):
        print("Data Received: %s", data)

    def send_remote_at(self, frame_id, dest_addr_long, command="DB"):
        self.xbee.remote_at(frame_id=frame_id,
        dest_addr_long=dest_addr_long,
        command=command)
        response = self.xbee.wait_read_frame()

        return response

    def signal_handler(self, signal, frame):
        self.shutdown()

    def shutdown(self):
        rospy.loginfo("Shutdown event caught.")
        self.xbee.halt()
        self.ser.close()

if __name__ == '__main__':
    pass
