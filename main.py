import os
import io
import base64
import PIL
from nicegui import ui
from sensor_msgs.msg import Image
from std_msgs.msg import String

data = ''

ui.add_head_html ('<script type="text/javascript" src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>')
ui.add_head_html ('<script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script>')

ui.add_head_html ('''<script>
                        var ros;
                        var data;
                        function connect(){
                            ros = new ROSLIB.Ros({url : "ws://localhost:9090"});
                            ros.on("connection", function() {console.log("Connected to websocket server.");});       
                            ros.on("error", function(error) {console.log("Error connecting to websocket server: ", error);});       
                            ros.on("close", function() {console.log("Connection to websocket server closed.");});
                        }

                        function sub(){
                            // Setting a new topic
                            var listener = new ROSLIB.Topic({
                                ros : ros,
                                name : "/image_topic",
                                messageType : "std_msgs/String"
                            });
                            // Subscribing to the topic 
                            listener.subscribe(function(message){
                                data = message.data;
                                });
                                //console.log('Received message on ' + listener.name + ': ' + message.data);
                                // If unsubscribed, the topic will not appear in the rqt
                                //listener.unsubscribe();
                            
                            console.log(listener);
                            while(data){
                                console.log(data);
                                return data;
                            }    
                        }
                    </script>''')

async def connection():
    # await "waits" for something to return. But this call does not require a respond. Which is y it kept complaining about request timeout.
    await ui.run_javascript(
        ''' connect() '''
         , respond=False)

async def subber():
    data = await ui.run_javascript(
        '''sub()'''
    , respond=False, timeout = 10)

ui.button('Connect WebSocket', on_click=connection)    
ui.button('Subscribe to Topic', on_click=subber) 
ui.markdown('''**Image**''')
ui.image(data)

ui.run()