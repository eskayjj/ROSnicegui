import base64
import cv2
import rclpy
import threading
import asyncio
import nicegui
import signal
import platform
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.node import Node
from nicegui import ui
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('image_subscriber')
        print("init")
        my_callback_group = MutuallyExclusiveCallbackGroup()
        self.subscription = self.create_subscription(Image, '/image_topic', callback=self.subscribe_image, qos_profile=1, callback_group=my_callback_group)
        self.bridge = CvBridge()
        self.subscription  # prevent unused variable warning
    
    def subscribe_image(self, image):
        img = self.bridge.imgmsg_to_cv2(image, "bgr8")
        encjpg = cv2.imencode('.jpg', img)[1]
        jpg_as_text = base64.b64encode(encjpg)
        jpg_as_text = 'data:image/jpeg;base64,' + str(jpg_as_text.decode('utf-8')) #convert jpg to base64
        self.get_logger().info('Received request')
        with ui.card().tight() as card:
            ui.image(jpg_as_text)
            with ui.card_section():
                ui.label('Ant Image')
        asyncio.run(self.run_gui())
   
    def run_gui(self):
        # start the NiceGUI event loop
        ui.run(reload=False)
        

    def start(self):
        try:
            # create a Queue to handle signals
            self.signal_queue = asyncio.Queue()
            # register a signal handler to put signals into the Queue
            signal.signal(signal.SIGINT, lambda signum, frame: asyncio.create_task(self.signal_queue.put(None)))
            # start the NiceGUI event loop in the main thread
            #ui.image("https://picsum.photos/id/29/640/360")
            # ui.image(self.subscribe_image)
            # asyncio.run(self.run_gui())
            
            # self.thread.start()
            rclpy.spin(self)
        except Exception as e:
            print(str(e))

    def stop(self):
        # shutdown the ROS node
        self.destroy_node()     

def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber()
    try:
        node.start()
        
    except Exception as e:
        print("Error: "+type(e).__name__)
    finally:
        # stop the event loop and shutdown the ROS node when the signal is received
        asyncio.run(node.stop())
        rclpy.shutdown()


print("main.py name: ", __name__)

if __name__ in {"image_publisher.main", "image_publisher.image_publisher"}:
    print("Entered main.py main")
    rclpy.init()
    node = ImageSubscriber()
    try:
        node.start()
        
    except Exception as e:
        print("Error: "+type(e).__name__)
    finally:
        # stop the event loop and shutdown the ROS node when the signal is received
        print("Shutdown")
        asyncio.run(node.stop())
        rclpy.shutdown()