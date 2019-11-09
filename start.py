#!/usr/bin/env python3
#start.py
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

# GPIO Pins
buttonPin = 17

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    os.system("./mbm.py 1")
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
