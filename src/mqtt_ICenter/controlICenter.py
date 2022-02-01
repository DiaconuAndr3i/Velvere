import paho.mqtt.client as mqtt


def on_message(client, userdate, message):
    message = str(message.payload.decode("utf-8"))
    print("Received message: ", message)
    global Flag
    global OptimumTem
    global OptimumHum
    if message == "stop":
        Flag = False
    if message.find('OptimumTem') != -1:
        listMessage = message.split()
        OptimumTem = float(listMessage[1])
    elif message.find('OptimumHum') != -1:
        listMessage = message.split()
        OptimumHum = float(listMessage[1])
    if message.find('Tem') != -1:
        listMessage = message.split()
        currentTemp = float(listMessage[1])
        if currentTemp < OptimumTem - 5 or currentTemp > OptimumTem + 5:
            print('The ambient temperature is not conducive to the plant!')
    elif message.find('Hum') != -1:
        listMessage = message.split()
        currentHum = float(listMessage[1])
        if currentHum < OptimumHum - 0.1 or currentHum > OptimumHum + 0.1:
            print('The ambient humidity is not conducive to the plant!')
    if message.find('Water') != -1:
        listMessage = message.split()
        currentQuantityOfWater = float(listMessage[1])
        if currentQuantityOfWater <= 2:
            print('The amount of water has dropped below the allowable threshold')
    elif message.find('Fertilizer') != -1:
        listMessage = message.split()
        currentQuantityOfFertilizer = float(listMessage[2])
        if currentQuantityOfFertilizer <= 1:
            print('The amount of fertilizer has dropped below the allowable threshold')


mqttBroker = "broker.hivemq.com"
client = mqtt.Client("ICenter")
client.connect(mqttBroker)

Flag = True
OptimumTem = 0
OptimumHum = 0

client.loop_start()
client.subscribe("AMBIENT_TEMPERATURE")
client.subscribe("AMBIENT_HUMIDITY")
client.subscribe("OPTIMUM_TEMPERATURE")
client.subscribe("OPTIMUM_HUMIDITY")
client.subscribe("WATER_GREENHOUSE")
client.subscribe("FERTILIZER_GREENHOUSE")
client.on_message = on_message
while True:
    if not Flag:
        break

client.loop_stop()
