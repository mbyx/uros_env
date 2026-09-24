#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32


class ImuYaw(Node):
    def __init__(self):
        super().__init__('imu_yaw')
        self.sub = self.create_subscription(
            Imu, '/zed/zed_node/imu/data', self.callback, 10)
        self.pub = self.create_publisher(Float32, '/steering_angle_raw', 10)

    def callback(self, msg):
        q = msg.orientation
        # yaw from quaternion
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw_rad = math.atan2(siny_cosp, cosy_cosp)
        yaw_deg = math.degrees(yaw_rad)

        # publish yaw in degrees
        out = Float32()
        out.data = yaw_deg
        self.pub.publish(out)

        self.get_logger().info(f'yaw = {yaw_deg:7.2f}°')


def main():
    rclpy.init()
    node = ImuYaw()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
