# MQTT-Client-Controller

This Python script allows a developer to set-up a target IoT device to execute a specific shell script, and trigger it using MQTT. 
In this specific usecase, a beaglbone blue is set up as an mosquitto client and listens for the topic "light". Once the topic is matched, 
a callback is triggered to parse the payload and determine whether or not the light is to be turned "ON" or "OFF". 
