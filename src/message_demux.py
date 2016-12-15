#!/usr/bin/env python
import rospy
import sys
from xbee_localization.msg import XBeeResponse

def callback(data):
    if data.header.frame_id == "beacon_1":
        pub_beacon_1.publish(data)
    elif data.header.frame_id == "beacon_2":
        pub_beacon_2.publish(data)
    elif data.header.frame_id == "beacon_3":
        pub_beacon_3.publish(data)
    else:
        rospy.logerr("Couldn't parse the incoming message!")

if __name__ == '__main__':
    try:
        rospy.init_node('xbee_response_demux', anonymous=True)

        pub_beacon_1 = rospy.Publisher("/xbee_response/beacon_1", XBeeResponse, queue_size=10)
        pub_beacon_2 = rospy.Publisher("/xbee_response/beacon_2", XBeeResponse, queue_size=10)
        pub_beacon_3 = rospy.Publisher("/xbee_response/beacon_3", XBeeResponse, queue_size=10)

        rospy.Subscriber("/xbee_response", XBeeResponse, callback)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
