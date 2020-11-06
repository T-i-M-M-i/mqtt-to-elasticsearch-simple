#this code is developed by Matthew Field http://www.smart-factory.net
#distributed under GNU public license https://www.gnu.org/licenses/gpl.txt

#this program requires the script to be run on the same server as you
#have elasticsearch running
#change the server and port data according to your installation
#the program is simple, but should work fine for testing
#the program will cope with a mixture of string and numeric data
#however it would be wise to develop further if a variety of data types
#such as json is to be used
import os

mqttServer=os.getenv('MQTT_SERVER')
mqttPort=int(os.getenv("MQTT_PORT"))
mqttUser=os.getenv("MQTT_USER")
mqttPW=os.getenv("MQTT_PW")
elasticHost=os.getenv("ELASTIC_HOST")

channelSubs=os.getenv("MQTT_CHANNEL")
#use below as alternative to subscribe to all channels
#channelSubs="#"

import paho.mqtt.client as mqtt
import ssl
import json
from datetime import datetime
from elasticsearch import Elasticsearch


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(channelSubs)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
 
# this is the syntax to follow for the elasticSearch update taken from documentation
#    es.index(index="my-index", doc_type="test-type", id=42, body={"any": +str(msg.payload, "timestamp": datetime.now()})
#    {u'_id': u'42', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}

#our implementation uses this to separate numeric(float) from string data

    try:
        result = json.loads(msg.payload)
        es.index(index="de4l-timmi-index", doc_type="measurement", body={"topic" : msg.topic, "data" : result, "timestamp": datetime.utcnow()})
    	
    except:
        try:
            es.index(index="my-index", doc_type="measurement_error", body={"topic" : msg.topic, "dataString" : msg.payload, "timestamp": datetime.utcnow()})
        except:
            print("another error occured,while logging error..")
    
# by default we connect to elasticSearch on localhost:9200
es = Elasticsearch( elasticHost )
es.index(index="debugging-index", doc_type="string", body={"topic":  "welcome", "dataString": "Server is up", "timestamp": datetime.utcnow()})


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqttUser, mqttPW)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(mqttServer, mqttPort, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()






