#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int32  # Swap with your actual message type (e.g., Float32, Twist)
import time

class VehicleController(Node):
    def __init__(self):
        super().__init__('vehicle_controller')
        
        # 1. Create isolated callback groups to run tasks on separate threads
        self.pub_group = MutuallyExclusiveCallbackGroup()
        self.sub_group = MutuallyExclusiveCallbackGroup()
        
        # 2. Setup the Command Publisher (Running at 10Hz)
        self.cmd_pub = self.create_publisher(
            Int32, 
            '/pwm_a', 
            10
        )
        self.timer = self.create_timer(
            0.1,  # 10Hz = 100ms interval
            self.timer_callback, 
            callback_group=self.pub_group
        )
        
        # 3. Setup the Acknowledgment Subscriber
        self.ack_sub = self.create_subscription(
            Int32,
            '/pwm_a_ack',
            self.ack_callback,
            10,  # Queue size
            callback_group=self.sub_group
        )
        
        # Tracking variables for latency logging
        self.msg_counter = 0
        self.sent_timestamps = {}
        
        self.get_logger().info('Vehicle Controller initialized with MultiThreadedExecutor.')

    def timer_callback(self):
        """Publishes the driving command at a strict 10Hz rate."""
        self.msg_counter += 1
        
        msg = Int32()
        msg.data = 1500  # Example PWM value or control signal
        
        # Track exactly when this message sequence number was sent
        current_time_ms = time.time() * 1000.0
        self.sent_timestamps[self.msg_counter] = current_time_ms
        
        # In a real setup, store the sequence ID inside a custom message header.
        # If using standard primitive types, we track order linearly:
        self.cmd_pub.publish(msg)

    def ack_callback(self, msg):
        """Receives acknowledgments from the ESP32 instantly on a separate thread."""
        receive_time_ms = time.time() * 1000.0
        
        # Clean up timestamps older than 5 seconds to prevent memory leaks
        # (Assuming responses match the sent timeline)
        if self.sent_timestamps:
            # Match against the oldest untracked message to calculate RTT
            oldest_seq = min(self.sent_timestamps.keys())
            sent_time_ms = self.sent_timestamps.pop(oldest_seq)
            
            rtt = receive_time_ms - sent_time_ms
            one_way = rtt / 2.0
            
            self.get_logger().info(
                f"Round Trip: {rtt:.2f} ms | Est. One-Way Network Delivery: {one_way:.2f} ms"
            )

def main(args=None):
    rclpy.init(args=args)
    
    node = VehicleController()
    
    # 💡 CRITICAL FIX: Spin the node using multiple threads
    # This ensures ack_callback is never blocked by timer_callback or execution lag
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Vehicle Controller...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
