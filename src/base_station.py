#!/usr/bin/env python
# ROS Packages
import rospy
from xbee_localization.msg import XBeeRequest
from xbee_localization.msg import XBeeResponse
# My Packages
from xbee import XBee
import time
import serial
import sys
import threading

class base_station(object):
    """docstring for base_station"""
    def __init__(self, args):
        """ TODO: ADD Error Handling """
        super(base_station, self).__init__()
        rospy.init_node('base_station', anonymous=True)

        self.args            = rospy.myargv(argv=sys.argv)
        self.port            = self.args[1]
        self.baud            = self.args[2]
        self.publisher       = None
        self.serial          = serial.Serial(self.port, self.baud)
        self.xbee            = XBee(self.serial, callback=self.message_received)
        self.publisher_topic = rospy.get_namespace() + "xbee_response"
        self.publisher       = rospy.Publisher(self.publisher_topic, XBeeResponse, queue_size=10)
        self.request_time    = None
        self.request         = XBeeRequest()
        self.mutex           = threading.Lock()
        rospy.Subscriber("/xbee_request", XBeeRequest, self.callback)
        rospy.on_shutdown(self.shutdown)

        rospy.spin()

    def message_received(self, data):
        rospy.loginfo("Data Received: %s", data)

        response = self.construct_ros_message(data)

        try:
            self.publisher.publish(response)
            print "Sent"
        except Exception as e:
            rospy.logerr("Error occurred while trying to publish the response: %s", e)
            print "Error"
        self.mutex.release()

    def construct_ros_message(self, data):
        response = XBeeResponse()
        try:
            rospy.loginfo("RSSI Obtained ASCII: %s Integer: %s", data['parameter'], ord(data['parameter']))
            response.header.seq       = self.request.header.seq
            response.header.stamp     = rospy.get_rostime()
            response.header.frame_id  = self.request.header.frame_id
            response.msg_type         = data['id']
            response.frame_id         = data['frame_id']
            response.source_addr      = str(map(ord,data['source_addr'])[:])
            response.source_addr_long = str(map(ord,data['source_addr_long'])[:])
            response.command          = data['command']
            response.response_ascii   = data['parameter']
            response.response_int     = ord(data['parameter'])
            response.status           = "Success"
            response.db               = ord(data['parameter'])
            response.rtt              = rospy.get_rostime() - self.request_time
        except Exception as e:
            rospy.logerr("Exception handled! Damaged package received or networking error occurred %s", e)
            rospy.loginfo(data)
            response.header.seq       = self.request.header.seq
            response.header.stamp     = rospy.get_rostime()
            response.header.frame_id  = self.request.header.frame_id
            response.msg_type         = data['id']
            response.frame_id         = data['frame_id']
            response.source_addr      = str(map(ord,data['source_addr'])[:])
            response.source_addr_long = str(map(ord,data['source_addr_long'])[:])
            response.command          = data['command']
            response.response_ascii   = '0'
            response.response_int     = 0
            response.status           = "Error"
            response.db               = 0
            response.rtt              = rospy.Duration(0)

        rospy.loginfo("Data to be sent: \n%s", response)

        return response

    def callback(self, data):
        self.mutex.acquire()
        self.request_time = rospy.get_rostime()
        self.request = data
        try:
            self.xbee.send(data.msg_type, frame_id=data.frame_id, dest_addr=data.dest_addr, command=data.command)
        except Exception as e:
            print e
            rospy.loginfo("Exception caught while trying to communicate with the sensor")
            rospy.loginfo("Received request package: \n%s", data)

    def shutdown(self):
        rospy.loginfo("Shutdown event caught.")
        self.xbee.halt()
        self.serial.close()


def main():
    comm = base_station(sys.argv)

if __name__ == '__main__':
    main()
