import mcp23017_Controller
import NeoPixel
import Display
from time import sleep
mcpList = {}
mcpPinlist = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    Display.Write_Display("MQTT Connected", 0)
    client.subscribe('0x20/#')
    client.subscribe('0x21/#')
    client.subscribe('0x22/#')
    client.subscribe('0x23/#')
    client.subscribe('0x24/#')
    client.subscribe('0x25/#')
    client.subscribe('0x26/#')
    client.subscribe('0x27/#')
    client.subscribe('CTRL01/RGB/#')

def getsetpin(pin):
    try:
        x = int(pin)
        if(x<0):
            return 0
        if(x>12):
            return 12
        return x
    except ValueError:
        return 0

def getValue(value):
    try:
        x = int(value)
        if(x<0):
            return False
        if(x>1):
            return True
        if(x == 1):
            return True
        else:
            return False
    except ValueError:
        return False

def getFanSpeed(vlaue):
    try:
        x = int(vlaue)
        if(x<0):
            return 0
        if(x>4):
            return 4
        return x
    except ValueError:
        return 0

def SetFanSpeed(Speed, MCPpins, MqttClient):
    print(Speed)
    if(Speed == 0):
        Result0 = mcp23017_Controller.SetPinValue(MCPpins,13,False,MqttClient)
        Result1 = mcp23017_Controller.SetPinValue(MCPpins,14,False,MqttClient)
        Result2 = mcp23017_Controller.SetPinValue(MCPpins,15, False,MqttClient)
        if(type(Result0) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result0))
            print(Result0)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result0))
        if(type(Result1) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result1))
            print(Result1)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result1))
        if(type(Result2) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result2))
            print(Result2)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result2))
    elif(Speed == 1):
        Result0 = mcp23017_Controller.SetPinValue(MCPpins,13,True,MqttClient)
        Result1 = mcp23017_Controller.SetPinValue(MCPpins,14,False,MqttClient)
        Result2 = mcp23017_Controller.SetPinValue(MCPpins,15, False, MqttClient)
        if(type(Result0) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result0))
            print(Result0)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result0))
        if(type(Result1) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result1))
            print(Result1)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result1))
        if(type(Result2) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result2))
            print(Result2)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result2))
    elif(Speed == 2):
        Result0 = mcp23017_Controller.SetPinValue(MCPpins,13,False,MqttClient)
        Result1 = mcp23017_Controller.SetPinValue(MCPpins,14,True,MqttClient)
        Result2 = mcp23017_Controller.SetPinValue(MCPpins,15, False,MqttClient)
        if(type(Result0) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result0))
            print(Result0)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result0))
        if(type(Result1) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result1))
            print(Result1)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result1))
        if(type(Result2) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result2))
            print(Result2)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result2))
    elif(Speed == 3):
        Result0 = mcp23017_Controller.SetPinValue(MCPpins,13,True)
        Result1 = mcp23017_Controller.SetPinValue(MCPpins,14,True)
        Result2 = mcp23017_Controller.SetPinValue(MCPpins,15, False)
        if(type(Result0) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result0))
            print(Result0)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result0))
        if(type(Result1) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result1))
            print(Result1)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result1))
        if(type(Result2) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result2))
            print(Result2)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result2))
    else:
        Result0 = mcp23017_Controller.SetPinValue(MCPpins,13,False,MqttClient)
        Result1 = mcp23017_Controller.SetPinValue(MCPpins,14,False,MqttClient)
        Result2 = mcp23017_Controller.SetPinValue(MCPpins,15, True,MqttClient)
        if(type(Result0) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result0))
            print(Result0)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result0))
        if(type(Result1) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result1))
            print(Result1)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result1))
        if(type(Result2) is OSError):
            MqttClient.publish('error/ctrl/pinOutSet', str(Result2))
            print(Result2)
        else:
            MqttClient.publish('Success/ctrl/pinOutSet', str(Result2))

def MCPSetup(client, msg):
    raw = str(msg.topic).split(sep='/')
    checkrow = ['0x20','0x21','0x22','0x23','0x24','0x25','0x26','0x27']
    if(raw[0] in checkrow):
        if(raw[0] not in mcpList):
            mcpClient = mcp23017_Controller.InitMCP23017(int(raw[0],16))
            if(type(mcpClient) is ValueError):
                client.publish('error/ctrl/add', str(mcpClient))
                print(mcpClient)
                return
            else:
                mcpList.update({raw[0]:mcpClient})

        if(raw[1] == 'FanSpeed'):
            speed = getFanSpeed(str(msg.payload,'utf-8'))
            SetFanSpeed(speed, mcpList[raw[0]], client)
        else:
            setpin = getsetpin(raw[1])
            value = getValue(str(msg.payload,'utf-8'))

            Result = mcp23017_Controller.SetPinValue(mcpList[raw[0]],setpin,value,client)
            print(Result)
            if(type(Result) is OSError):
                client.publish('error/ctrl/pinOutSet', str(Result))
                print(Result)
            else:
                client.publish('Success/ctrl/pinOutSet', str(Result))
            #client.publish('error/ctrl/add', str(mcpClient))

def pixelID(ID):
    try:
        x = int(ID)
        if(x<0):
            return 0
        else:
            return x
    except ValueError:
        return 0

def RGBSetup(client, msg):
    raw = str(msg.topic).split(sep='/')
    if(raw[0] == 'CTRL01' and raw[1] == 'RGB'):
        raw_color_value = str(msg.payload,'utf-8').split(',')
        id = pixelID(raw[2])
        NeoPixel.Set_Pixel_Color(id, raw_color_value[0], raw_color_value[1], raw_color_value[2])

def on_message(client, userdata, msg):
    MCPSetup(client,msg)
    #RGBSetup(client, msg)
    print(msg.topic+" "+ str(msg.payload,'utf-8'))
    sleep(0.5)

def on_disconnect(client, userdata, rc):
    if(rc != 0):
        print("Unexpected disconnection.")
        Display.Write_Display("Unexpected disconnection. \n Reconnecting", 0)
        try:
            client.reconnect()
        except OSError as e:
            print(e)
            Display.Write_Display(str(e), 0)
