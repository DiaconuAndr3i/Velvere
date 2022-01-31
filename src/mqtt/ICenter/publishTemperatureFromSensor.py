import paho.mqtt.client as mqtt
import time
from random import uniform

mqttBroker = "broker.hivemq.com"
client = mqtt.Client("Ambient_temperature")
client.connect(mqttBroker)


while True:
    temperature = uniform(15.0, 25.0)
    client.publish("TEMPERATURE", f'Tem: {temperature}')
    print("Just published " + str(temperature) + " to topic TEMPERATURE")
    time.sleep(1)
