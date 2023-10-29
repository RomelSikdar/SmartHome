import sys
sys.path.insert(1, './MQTT')
sys.path.insert(1, './RGB')
sys.path.insert(1, './MCP23017')
sys.path.insert(1, './MQTT_Functions')
sys.path.insert(1, './Display')
import MQTT_Controller
import NeoPixel

from mqttfunc import on_connect, on_message, on_disconnect


try:
    client = MQTT_Controller.MqttInit('192.168.254.10',1883,"Admin",'iwillhacku')
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
