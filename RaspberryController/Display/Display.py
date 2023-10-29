# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(SCL, SDA)

disp = None
draw = None

try:
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    disp.fill(0)
    disp.show()
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    draw = ImageDraw.Draw(image)
except Exception as e:
    print(e)
    print('Status Display Error')

font = ImageFont.load_default()

def Write_Display(text, startPadding):
    try:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")

        draw.text((0, 0), "IP: " + IP, font=font, fill=255)
        draw.text((0, startPadding + 8), text, font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.show()
    except Exception as e:
        print(e)
        print('Status Display WRITE Error')
