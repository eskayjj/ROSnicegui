import os
import io
import base64
import PIL
import cv2
import rclpy
import base64
from rclpy.node import Node
from nicegui import ui
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

jpg_as_text = ''

class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(String, 'image_topic', self.subscribe_image, 10)
        self.subscription  # prevent unused variable warning
       
    def subscribe_image(self, msg):
        jpg_as_text = msg
        #print(jpg_as_text)
        #return jpg_as_text

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    ui.markdown('''**Image**''')
    ui.image(jpg_as_text)
    #ui.run(title='ROS Example')
    ui.run()
    image_subscriber.destroy_node()
    rclpy.shutdown()


# if __name__ == '__main__':
#     main()