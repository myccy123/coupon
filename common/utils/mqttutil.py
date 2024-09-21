from paho.mqtt.publish import single

MQTT_HOST = 'www.bjsiri.com'
MQTT_PORT = 1883


def send(topic, msg):
    print(f'mqtt send:{topic}', msg)
    single(topic, msg, hostname=MQTT_HOST, port=MQTT_PORT)
