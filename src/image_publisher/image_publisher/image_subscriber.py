import cv2
import rclpy
import base64
from rclpy.node import Node
#from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(String, 'image_topic', self.subscribe_image, 10)
        #self.imagePub_ = self.create_publisher(String, "image_jpeg", 10)
        self.subscription  # prevent unused variable warning
        #self.bridge = CvBridge()

    def subscribe_image(self, msg):
        global jpg_as_text
        jpg_as_text = msg
        print(jpg_as_text)
        return jpg_as_text
        # img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # cv2.imwrite('temp.jpg', img)
        # image_64 = base64.b64encode(open("temp.jpg","rb").read())
        # self.imagePub_.publish(self.String(image_64))

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()