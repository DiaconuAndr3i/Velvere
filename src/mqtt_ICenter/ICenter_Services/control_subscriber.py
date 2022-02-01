import paho.mqtt.client as mqtt

mqttBroker = "broker.hivemq.com"
client_control = mqtt.Client("Control")
client_control.connect(mqttBroker)

client_control.publish("AMBIENT_TEMPERATURE", 'stop')
client_control.publish("AMBIENT_HUMIDITY", 'stop')
