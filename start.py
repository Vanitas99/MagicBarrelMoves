#!/usr/bin/env python3
#start.py
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

# GPIO Pins
buttonPin = 17

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pid = 99999
running = False

#os.system("sudo python3 read_uc_sensor.py & 1")
#running = true

try:
    while True:
       GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
       if running:
          f = open('mbm.pid','r')
          pid = f.read()
          f.close()
          print(pid )
          try:
             os.system("sudo pkill -9 -f read_uc_sensor.py")
             print("Killing Process: %s\n" % pid)
          except OSError:
             print("Error Killing Process")
             continue
          running = False
       else:
          os.system("sudo python3 read_uc_sensor.py & 1")
          running = True
       time.sleep(2)
       
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
