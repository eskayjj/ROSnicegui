import os
import io
import base64
import PIL
from nicegui import ui
from sensor_msgs.msg import Image
from std_msgs.msg import String
#import src.image_publisher.image_publisher.image_subscriber as f


async def connection():
    await ui.run_javascript(
        '''var ros = new ROSLIB.Ros({url : "ws://localhost:9090"});
           ros.on("connection", function() {console.log("Connected to websocket server.");});       
           ros.on("error", function(error) {console.log("Error connecting to websocket server: ", error);});       
           ros.on("close", function() {console.log("Connection to websocket server closed.");});'''
    )

async def subber():
    await ui.run_javascript(
        '''var listener = new ROSLIB.Topic({
            ros : ros, 
            name : "/image_topic",  
            messageType : "std_msgs/msg/String"  });'''
    )

async def execute():
    await ui.run_javascript(
        '''listener.subscribe(function(message) {
            console.log("listening");  
            listener.unsubscribe();  
            });'''
    )

ui.add_head_html ('<script type="text/javascript" src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>')
ui.add_head_html ('<script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script>')
ui.button('Connect WebSocket', on_click=connection)    
ui.button('Subscribe to Topic', on_click=subber) 

ui.run()