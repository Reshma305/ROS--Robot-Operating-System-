#!/usr/bin/env python3
import rclpy  # type: ignore
from rclpy.node import Node  # type: ignore
from turtlesim.msg import Pose  # type: ignore

class PoseSubscriberNode(Node):
    def __init__(self):
        super().__init__("pose_subscriber_node")
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.get_logger().info("Pose Subscriber Node has been started.")

    def pose_callback(self, msg: Pose):
        self.get_logger().info(str(msg))

    def main(args=None):
        rclpy.init(args=args)
        node = PoseSubscriberNode()
        rclpy.spin(node)
        rclpy.shutdown()