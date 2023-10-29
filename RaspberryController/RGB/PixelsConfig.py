import numpy as np
from os.path import exists

def UpdatePixels(ID, Red, Green, Blue):
    pixelFile = exists('./neopixel.txt')
    if (not pixelFile):
        x = np.zeros([10, 3], dtype=int).reshape((10,3))
        np.savetxt('neopixel.txt', x, fmt='%i')

    pixels = ReadPixels()
    if(type(pixels) is not bool):
        pixels[ID] = [Green, Red, Blue]
        #print(pixels)
        np.savetxt('neopixel.txt', pixels, fmt='%s')
    

def ReadPixels():
    pixelFile = exists('./neopixel.txt')
    if (not pixelFile):
        return False
    else:
        tmp = np.loadtxt('neopixel.txt', dtype=object)
        return tmp.tolist()
