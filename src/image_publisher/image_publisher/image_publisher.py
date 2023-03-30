import cv2
import rclpy
import base64
from rclpy.node import Node
#from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

PATH="./src/image_publisher/Ant_1.jpg"

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(String, 'image_topic', 10)
        self.timer = self.create_timer(0.1, self.publish_image)
        #self.bridge = CvBridge()

    def publish_image(self):
        img = cv2.imread(PATH) #this is non-dynamic
        #msg = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
        encjpg = cv2.imencode('.jpg', img)
        jpg_as_text = String()
        jpg_as_text.data = str(base64.b64encode(encjpg[1])) #convert jpg to base64
        #jpg_as_text.data = str(base64.b64encode(img))
        self.publisher_.publish(jpg_as_text)

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()