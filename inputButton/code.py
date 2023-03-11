from lib.mqtt import MQTTClient
from usocket import socket
from machine import Pin,SPI
from config.config import CLIENT_ID,MQTT_HOST,PORT,USER,PASSWORD
import network
import time

#Power LED
PowerLed = Pin(25, Pin.OUT)
#MQTT CLIENT
client = None
#INPUT PINS
pins = []
#INPUT PINS STATE
pinsLastState = []

#W5x00 chip init
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    
    #None DHCP
    #nic.ifconfig(('192.168.11.20','255.255.255.0','192.168.1.1','8.8.8.8'))
    
    #DHCP
    nic.ifconfig('dhcp')
    print('IP address :', nic.ifconfig())
    return nic

client = MQTTClient(str(machine.unique_id()), MQTT_HOST,port=PORT,user=USER,password=PASSWORD)
 
def pin_setup():
    for i in range(16):
        pins.append(Pin(i, Pin.IN, Pin.PULL_UP))
        pinsLastState.append(pins[i].value())

def sendMQTT(pin,SwitchNo):
    if (pinsLastState[SwitchNo] != pin.value()):
        print(SwitchNo)
        client.publish(topic=CLIENT_ID + "/" + str(SwitchNo+1), msg=str(pin.value()), qos=0)
    pinsLastState[SwitchNo] = pin.value()
        
def check_lan(nic):
    if not nic.isconnected():
        print("Cable Disconnected Restarting Device")
        time.sleep(1)
        machine.reset()

print("Post Address :- ", CLIENT_ID)
lan = w5x00_init()
check_lan(lan)
pin_setup()
client.connect()
while True:
    try:
        for i in range(16):
            sendMQTT(pins[i],i)
    except Exception as e:
        print("Error in mqtt connect: [Exception] %s: %s" % (type(e).__name__, e))
        machine.reset()


