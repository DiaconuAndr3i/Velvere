import paho.mqtt.client as mqtt


def on_message(client, userdate, message):
    message = str(message.payload.decode("utf-8"))
    print("Received message: ", message)
    global Flag
    if message == "stop":
        Flag = False


mqttBroker = "broker.hivemq.com"
client = mqtt.Client("ICenter")
client.connect(mqttBroker)

Flag = True

client.loop_start()
client.subscribe("TEMPERATURE")
client.subscribe("HUMIDITY")
client.on_message = on_message
while True:
    if not Flag:
        break

client.loop_stop()
