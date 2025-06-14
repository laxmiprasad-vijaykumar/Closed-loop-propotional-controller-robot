#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Global variable to store the current pose of the turtle
pose = Pose()

def pose_callback(data):
    global pose
    pose = data

def euclidean_distance(goal_x, goal_y):
    return math.sqrt((goal_x - pose.x)**2 + (goal_y - pose.y)**2)

def linear_velocity(goal_x, goal_y, constant=1.5):
    return constant * euclidean_distance(goal_x, goal_y)

def steering_angle(goal_x, goal_y):
    return math.atan2(goal_y - pose.y, goal_x - pose.x)

def normalize_angle(angle):
    """ Normalize angle to be between -π and +π """
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def angular_velocity(goal_x, goal_y, constant=6):
    angle_to_goal = steering_angle(goal_x, goal_y)
    angle_error = normalize_angle(angle_to_goal - pose.theta)
    return constant * angle_error

def move_to_goal():
    rospy.init_node('go_to_goal', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    rate = rospy.Rate(10)  # 10 Hz

    # User goal
    goal_x = float(input("Enter goal x (0-11): "))
    goal_y = float(input("Enter goal y (0-11): "))

    vel_msg = Twist()

    while not rospy.is_shutdown() and euclidean_distance(goal_x, goal_y) >= 0.1:
        vel_msg.linear.x = linear_velocity(goal_x, goal_y)
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = angular_velocity(goal_x, goal_y)

        pub.publish(vel_msg)
        rate.sleep()

    # Stop once goal is reached
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    pub.publish(vel_msg)
    rospy.loginfo("✅ Goal Reached!")

if __name__ == '__main__':
    try:
        move_to_goal()
    except rospy.ROSInterruptException:
        pass
