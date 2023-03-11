import board
import busio
import struct
import digitalio
import time
import supervisor
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
statusLed = digitalio.DigitalInOut(board.GP25)
statusLed.direction = digitalio.Direction.OUTPUT

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="10.10.1.254",
    username="Admin",
    password="iwillhacku",
    is_ssl=False,
    keep_alive=10
)

#Ethernet Crad Hardware Config
SPI1_SCK = board.GP18
SPI1_TX = board.GP19
SPI1_RX = board.GP16
SPI1_CSn = board.GP17
W5500_RSTn = board.GP20
timestamp = 0

print("Setting up (DHCP)")

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x06, 0x07, 0x08, 0x09, 0x10, 0x11)

#If Static IP Config
#IP_ADDRESS = (192, 168, 0, 111)
#SUBNET_MASK = (255, 255, 0, 0)
#GATEWAY_ADDRESS = (192, 168, 0, 1)
#DNS_SERVER = (8, 8, 8, 8)

# For Ethernet CS pic
cs = digitalio.DigitalInOut(SPI1_CSn)
# For Ethernet Reset pic
Rst = digitalio.DigitalInOut(W5500_RSTn)
Rst.direction = digitalio.Direction.OUTPUT
#SPI Configuration
spi_bus = busio.SPI(SPI1_SCK, MOSI=SPI1_TX, MISO=SPI1_RX)
# Reset Ethernet first
Rst.value = False
time.sleep(1)
Rst.value = True

try:
    # # Initialize ethernet interface without DHCP
    # eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
    # # Set network configuration
    # eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

    # Initialize ethernet interface with DHCP
    eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)
except AssertionError as e:
    print(e)
    supervisor.reload()
#Printing Hardware Details
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Setup a feed named 'color_feed' for publishing to a feed
feed = "Switch01"
### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker")

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker")
    client.reconnect()

def loop(keep_alive):
    global timestamp
    if timestamp == 0:
        timestamp = time.monotonic()
    current_time = time.monotonic()
    if current_time - timestamp >= keep_alive:
        timestamp = 0
        rcs = mqtt_client.ping()
        print(rcs)

# Initialize MQTT interface with the ethernet interface
MQTT.set_socket(socket, eth)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected

# Connect the client to the MQTT broker.
print("Connecting to MQTT Broker...")
try:
    mqtt_client.connect()
    statusLed.value = True
except MQTT.MMQTTException as e:
    print(e)
    supervisor.reload()
except RuntimeError as e:
    print(e)
    supervisor.reload()

#Defining Button List
ButtonList,PreviousState = [
    digitalio.DigitalInOut(board.GP0),
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP2),
    digitalio.DigitalInOut(board.GP3),
    digitalio.DigitalInOut(board.GP4),
    digitalio.DigitalInOut(board.GP5),
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP8),
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP10),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP13),
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP15)
    ],[
        True,True,True,True,
        True,True,True,True,
        True,True,True,True,
        True,True,True,True,
        ]
#Setting Button as Input
for button in ButtonList:
    button.direction,button.pull = digitalio.Direction.INPUT,digitalio.Pull.UP

while True:
    # Poll the message queue
    try:
        loop(10)
        for i in range(len(ButtonList)):
            cur_state = ButtonList[i].value
            if(cur_state != PreviousState[i]):
                print("Sending ButtonStatus %d " % cur_state)
                if(mqtt_client.is_connected()):
                    mqtt_client.publish(feed + str(i) , 1 if not cur_state else 0)
                else:
                    print("MQTT Disconnected!!!")
                    supervisor.reload()
            PreviousState[i] = cur_state
    except AssertionError as e:
        print(e)
        supervisor.reload()
    except MQTT.MMQTTException as e:
        print(e)
        supervisor.reload()

print("Done!")