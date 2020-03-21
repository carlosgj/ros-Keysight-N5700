#!/usr/bin/env python
from N5700SCPI import N5700SCPI
import rospy
from keysight_n5700.msg import PSTelem


def talker():
    pub = rospy.Publisher('N5700-Telem', PSTelem, queue_size=10)
    ps = N5700SCPI("192.168.1.17",timeout=1)
    ps.connect()
    rospy.init_node("N5700", anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        thismsg = PSTelem()
        thismsg.commanded_voltage = ps.getCommandedVoltage()
        thismsg.actual_voltage = ps.getActualVoltage()
        thismsg.commanded_current = ps.getCommandedCurrent()
        thismsg.actual_current = ps.getActualCurrent()
        thismsg.output_enabled = ps.getOutputState()
        rospy.loginfo(thismsg)
        pub.publish(thismsg)
        rate.sleep()
    this.close()


if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
