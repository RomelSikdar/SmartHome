from rpi_ws281x import *
import PixelsConfig
import numpy as np

# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def Set_Pixel_Color(ID, Red, Green, Blue):
    if(ID<10):
        PixelsConfig.UpdatePixels(ID, Red, Green, Blue)
        pixels = PixelsConfig.ReadPixels()
        pixels = np.array(pixels)
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
        strip.begin()
        for i in range(0,10):
            color = Color(int(pixels[i,0]),int(pixels[i,1]),int(pixels[i,2]))
            strip.setPixelColor(i,color)

        strip.show()
        return 'Done'
    else:
        return 'ID Must Be Between 0-9'
