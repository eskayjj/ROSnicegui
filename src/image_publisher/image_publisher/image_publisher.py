import cv2
import rclpy
import base64
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

PATH="./src/image_publisher/Ant_1.jpg"

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_topic', 10)
        self.timer = self.create_timer(0.1, self.publish_image)
        self.bridge = CvBridge()

    def publish_image(self):
        img = cv2.imread(PATH) #this is non-dynamic
        # encjpg = cv2.imencode('.jpg', img)[1]
        # jpg_as_text = String()
        # jpg_as_text.data = str(base64.b64encode(encjpg)) #convert jpg to base64
        self.publisher_.publish(self.bridge.cv2_to_imgmsg(img, "bgr8"))
        #self.publisher_.publish(img)
        # with open(PATH, "rb") as img_file:
        #     jpg_as_text = String()
        #     img_string = base64.b64encode(img_file.read())
        #     jpg_as_text.data = str(img_string.decode('utf-8'))
        # self.publisher_.publish(jpg_as_text)

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

print("image_publisher.py name: ", __name__)

if __name__ in {"image_publisher.main", "image_publisher.image_publisher"}:
    print("Entered image_publisher.py main")
    main()