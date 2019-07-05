# MQTT-Client-Controller

This Python script allows an edge device running a mosquitto client to subscibe to an MQTT topic and execute a shell script when triggered. 
In this specific usecase, a BeaglBone Blue listens for the topic "light". Once a notification is received, a callback is triggered to parse the payload and determine whether or not the light is to be turned "ON" or "OFF". 