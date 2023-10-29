import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

def InitMCP23017(address):
    try:
        return MCP23017(i2c, address=address)
    except ValueError as e:
        return e

def SetAllPinOutput(mcp):
    try:
        pins = []
        for pin in range(0, 16):
            pins.append(mcp.get_pin(pin))

        for pin in pins:
            pin.direction = Direction.OUTPUT
        
        return pins
    except Exception as e:
        print(e)
        return e

def SetPinValue(MCP, pin, value, client):
    try:
        pins = SetAllPinOutput(MCP)

        if(type(pins) is Exception):
            client.publish('error/ctrl/PinSet', str(pins))
            print(pins)
            return

        pins[pin].value = value

        return True
    except OSError as e:
        return e
