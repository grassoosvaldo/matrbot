import sys, getopt
import time
import ssl
import paho.mqtt.client as mqtt
import json

execute_topic   = ""
response_topic  = ""
mqttc = None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("Subscribing to "+args.execute_topic)
    mqttc.subscribe(execute_topic, args.qos)

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    commandJson = json.loads(msg.payload)
    print(commandJson)

def publish_state(distance d):
    json_state_str = json.dumps(d)
    print(json_state_str)
    mqttc.publish(response_topic, json_state_str)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def setup():
    port = 8883
    
    mqttc = mqtt.Client(args.clientid,clean_session = true)
    
  
    tlsVersion = None
  
  
    mqttc.tls_set(ca_certs="./certs/rootCA.pem", certfile="./certs/Matrbot.certificate.pem", keyfile="./certs/Matrbot.private-key.txt", cert_reqs=ssl.CERT_REQUIRED, tls_version=None)
    

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    
    execute_topic  = "fdea7fe8";
    response_topic = "fdea7fe8";

    host = "a2sq3y7mdrjtom.iot.us-east-1.amazonaws.com";
    
    print("Connecting to "+host+" port: "+str(port))
    mqttc.connect(args.host, port, 60)
    
    mqttc.loop_forever()
    
    
def terminate():
    mqttc.disconnect()
