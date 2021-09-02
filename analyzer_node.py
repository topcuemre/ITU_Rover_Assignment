#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

n_data = String()
start = False
pub_drive = rospy.Publisher('/position/drive', String, queue_size = 10)
pub_arm = rospy.Publisher('/position/robotic_arm', String, queue_size = 10)

def callback(data):
    global start, n_data
    n_data = filter(data.data)
    if type(n_data) == str:
        n_data = trim(n_data)
        n_data = reader(n_data)
        rospy.loginfo(n_data)
        if (not start):
            start = True

def reader(msg):
    msg_mod = ''
    if len(msg) == 16:
        for i in range(0, 16, 4):
            if msg[i] == '0':
                if int(msg[ i+1 : i+4]) > 255:
                    limit = str(255)
                    msg_mod = msg_mod + '+' + limit  + ' '
                else:
                    msg_mod = msg_mod + '+' + msg[ i+1 : i+4 ] + ' '
            else:
                if int(msg[ i+1 : i+4]) < -255:
                    limit = str(-255)
                    msg_mod = msg_mod + '+' + limit  + ' '
                else:
                    msg_mod = msg_mod + '-' + msg[ i+1 : i+4 ] + ' '
        return msg_mod
        print(msg_mod)
    else:
        for i in range(0, 24, 4):
            if msg[i] == '0':
                if int(msg[ i+1 : i+4]) > 255:
                    limit = str(255)
                    msg_mod = msg_mod + '+' + limit  + ' '
                else:
                    msg_mod = msg_mod + '+' + msg[ i+1 : i+4 ] + ' '
            else:
                if int(msg[ i+1 : i+4]) < -255:
                    limit = str(-255)
                    msg_mod = msg_mod + '+' + limit  + ' '
                else:
                    msg_mod = msg_mod + '-' + msg[ i+1 : i+4 ] + ' '
        return msg_mod
        print(msg_mod)

def filter(msg):
    if  msg.startswith('A') and msg.endswith('B'):
        return msg

def trim(msg):
        msg_repl = msg.replace('A','').replace('B','')
        return msg_repl

def timer_callback(event):
    global start, pub_drive, pub_arm, n_data
    if (start) and type(n_data) == str:
        if (len(n_data) == 20):
            pub_drive.publish(n_data)
        else:
            pub_arm.publish(n_data)

def main():
    rospy.init_node('analyzer_node')
    rospy.Subscriber('/serial/drive', String, callback)
    rospy.Subscriber('/serial/robotic_arm', String, callback)    
    timer = rospy.Timer(rospy.Duration(1.), timer_callback)
    rospy.spin()
    timer.shutdown()

if __name__ == '__main__':
    main()

