#!/usr/bin/env python
import rospy
import sys
from xbee_localization.msg import XBeeRequest

def main():
    rospy.init_node('remote_request', anonymous=True)
    pub = rospy.Publisher("/xbee_request", XBeeRequest, queue_size=10)
    args                    = rospy.myargv(argv=sys.argv)
    address                 = map(int,args[2:])
    request                 = XBeeRequest()
    request.header.seq      = 0
    request.header.stamp    = rospy.get_rostime()
    request.header.frame_id = args[1]
    request.msg_type        = "remote_at"
    request.frame_id        = '0'
    request.dest_addr       = address
    request.command         = "DB"

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        pub.publish(request)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
