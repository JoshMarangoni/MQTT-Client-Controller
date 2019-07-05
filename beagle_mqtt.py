#!python3

#------------------------------------------------------------------------------------------
# Author:   Joshua Marangoni
# Date:     June 5, 2019
# Purpose:  1. Connects client devices to MQTT message broker and confirms connection
#           2. Subscripes to topic, based on "topic" variable
#           3. Receives and interprets messages from broker
#           4. Executes shell script if message is "ON", or terminates a script if "OFF"
#------------------------------------------------------------------------------------------

import paho.mqtt.client as mqtt         #import the client class
import subprocess 
import time
import sys

def on_connect(client, userdata, flags, rc):   #server connection callback
    if rc==0:
        print("connected OK")
        client.connected_flag = True  #set flag
    else:
        print("Bad connection Returned code ",rc)
        client.bad_connection_flag = True


def on_disconnect(client, userdata, rc):     #server disconnection callback
    if(rc==0):
        print("disconnected")
    else:
        print("Unexpected disconnect, code " + str(rc) + ", exiting...")
    client.loop_stop()
    sys.exit() 


def on_message(client, userdata, message):       #message received from server callback
    if message.topic != topic: 
        print("Unrecognized topic: ", message.topic)
    else: 
        payload = str(message.payload.decode("utf-8"))
        print("message received, payload: ", payload)
        determine_payload(payload)


def determine_payload(payload): 
    if payload == "ON" or payload == "On" or payload == "on":
        client.execution_flag = True
        client.termination_flag = False
        print("executing "+execute_script)
    elif payload == "OFF" or payload == "Off" or payload == "off":  
        client.termination_flag = True
        client.execution_flag = False
        print("terminating...")
    else: 
        print("Unrecognized payload...message ignored.")


def subscribe_topic(client, topic):
    try: 
        r = client.subscribe(topic)
        if r[0] == 0:
            print("subscribe to topic: '"+topic+"' successful, return code" +str(r))
        else: 
            print("error on subscribing, return code: ", str(r))
    except Exception as e: 
            print("error on subscribing ", str(e))


client = mqtt.Client()           #create a new client instance    

client.connected_flag = False        
client.bad_connection_flag = False
client.disconnect_flag = False
client.execution_flag = False
client.termination_flag = False

topic = "blink"
payload = ""                 #initliaze payload variable
execute_script = "led0_blink.sh"    #program to execute 
terminate_script = "led0_heartbeat.sh"   #program that restores defaults

client.on_connect = on_connect          #bind callback function   
client.on_disconnect = on_disconnect
client.on_message = on_message    

broker = "192.168.1.8"   
client.connect(broker) 
client.loop_start()       #loop_start() buffers incoming/outgoing communication to/from server

while not client.connected_flag and not client.bad_connection_flag:  #wait to connect 
    print("Trying to connect...")
    time.sleep(1)

if client.bad_connection_flag: 
    client.loop_stop()
    sys.exit()

subscribe_topic(client, topic)    

while True: 

    if client.execution_flag: 
        process = subprocess.Popen('sudo ./led0_blink.sh', shell=True, stdout=subprocess.PIPE)
        process.wait()
        client.execution_flag = False

    
    if client.termination_flag:  
        process = subprocess.Popen('sudo ./led0_heartbeat.sh', shell=True, stdout=subprocess.PIPE)
        process.wait()
        client.termination_flag = False 

