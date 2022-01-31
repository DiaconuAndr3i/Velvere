import paho.mqtt.client as mqtt
import time
from random import uniform

mqttBroker = "broker.hivemq.com"
client = mqtt.Client("Humidity")
client.connect(mqttBroker)


while True:
    humidity = uniform(0, 1)
    client.publish("HUMIDITY", f'Hum: {humidity}')
    print("Just published " + str(humidity) + " to topic HUMIDITY")
    time.sleep(1)
