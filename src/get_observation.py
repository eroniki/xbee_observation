#!/usr/bin/python

import time
import thread

import XBeeHandler

from xbee_observation.srv import XBeeArrayService
from xbee_observation.srv import XBeeArrayServiceResponse
from xbee_observation.msg import XBeeMessage
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Int64

import rospy


class xbee_obs(object):
    """docstring for xbee_obs"""

    def __init__(self):
        super(xbee_obs, self).__init__()
        rospy.init_node('xbee_obs_server')
        self.s = rospy.Service(
            'xbee_observation', XBeeArrayService, self.handle_xbee_obs)
        self.xbeeHandler = XBeeHandler.XBeeHandler()
        if self.get_params():
            if self.xbeeHandler.init_port(self.port, self.baud) >= 0:
                rospy.loginfo("Ready to send xbee observations")
                rospy.spin()
            else:
                rospy.logerr(
                    "Could NOT initialize the serial port, \
                    xbee scanning is exiting")
            # pass

    def get_params(self):
        self.namespace = rospy.get_namespace()
        # print self.namespace, "".join((self.namespace, "~port_xbee"))
        try:
            self.port = rospy.get_param('~port_xbee')
            self.baud = rospy.get_param('~baud_xbee')
            self.addr = rospy.get_param("xbee_addresses")
            self.n_beacon = len(self.addr)
        except KeyError as e:
            rospy.logerr("The parameters cannot resolved")
            return False
        return True

    def handle_xbee_obs(self, data):
        rospy.loginfo("Service request captured")
        obsList = list()
        for i in range(len(self.addr)):
            obsList.append(self.xbeeHandler.send_remote_at(
                frame_id="0", dest_addr_long=self.addr[i].decode("hex")))
            print obsList[i]
        return self.construct_response(obsList)

    def construct_response(self, data):
        response = XBeeArrayServiceResponse()
        obsList = list()
        header = Header()
        header.stamp = rospy.get_rostime()
        for i in range(len(data)):
            obs = XBeeMessage()
            obs.header = header
            obs.mac = data[i]["source_addr_long"].encode('hex')
            try:
                obs.rss = ord(data[i]["parameter"])
            except KeyError:
                obs.rss = 0
            obsList.append(obs)

        if(self.n_beacon > 0):
            response.success = True
            response.message = "Success!"
            response.observations = obsList
        else:
            response.success = False
            response.message = "Error!"

        return response


if __name__ == "__main__":
    wifi_obs = xbee_obs()
