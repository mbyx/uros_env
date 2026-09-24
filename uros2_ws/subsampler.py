import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 # Adjust to your actual message type

class Subsampler(Node):
    def __init__(self):
        super().__init__('subsampler')
        self.subscription = self.create_subscription(
            Float32, '/steering_angle_raw', self.listener_callback, 10)
        self.publisher = self.create_publisher(Float32, '/steering_angle', 10)
        self.skip_count = 25  # Keep every 5th message (drops 4 in between)
        self.counter = 0

    def listener_callback(self, msg):
        self.counter += 1
        if self.counter >= self.skip_count:
            self.publisher.publish(msg)
            self.counter = 0

def main(args=None):
    rclpy.init(args=args)
    node = Subsampler()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
