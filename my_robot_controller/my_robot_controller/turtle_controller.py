import rclpy  # type: ignore
from rclpy.node import Node  # type: ignore
from turtlesim.msg import Pose  # type: ignore
from geometry_msgs.msg import Twist  # type: ignore
from turtlesim.srv import SetPen  # type: ignore
from functools import partial  # type: ignore

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller_node")
        self.previous_x_ = 0
        self.cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.get_logger().info("Turtle controller node has been started.")

    def pose_callback(self, pose: Pose):
           cmd = Twist()

           if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
                cmd.linear.x = 1.0
                cmd.angular.z = 0.9
           else:
                cmd.linear.x = 5.0
                cmd.angular.z = 0.0
           self.cmd_vel_publisher.publish(cmd)

           if pose.x > 5.5 and self.previous_x_ <= 5.5:
               self.previous_x_ = pose.x
               self.get_logger().info("Set color to red!")
               self.call_set_pen_service(255, 0, 0, 3, 0)
           elif pose.x <= 5.5 and self.previous_x_ > 5.5:
               self.previous_x_ = pose.x
               self.get_logger().info("Set color to green!")
               self.call_set_pen_service(0, 255, 0, 3, 0)

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for set_pen service...") #If the service is not available, this will keep trying until it is.

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:                                                             # This callback is called when the service call is complete.
            response = future.result()                                   # if ROS2 doesn't find the service, it will raise an exception.
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))

def main(args=None):                          # This is the main function that initializes the ROS2 node and starts spinning.
    rclpy.init(args=args)             
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
  