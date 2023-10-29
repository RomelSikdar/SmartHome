import paho.mqtt.client as mqtt

def MqttInit(host, port, username, password):
    client = mqtt.Client(client_id='CTRL1')
    client.username_pw_set(username, password)
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    try:
        client.connect(host, port, keepalive=10)
    except:
        print('connection error')

    return client
