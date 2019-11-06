"""
KY040 Python Class
Martin O'Hanlon
stuffaboutcode.com


Additional code added by Conrad Storz 2015 and 2016
"""

import RPi.GPIO as GPIO
from time import sleep


class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    DEBOUNCE = 50

    def __init__(self, clockPin, dataPin, switchPin, rotaryCallback, switchCallback):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback

        #setup pins
        GPIO.setup(clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self._clockCallback, bouncetime=self.DEBOUNCE)
        GPIO.add_event_detect(self.switchPin, GPIO.FALLING, callback=self.switchCallback, bouncetime=self.DEBOUNCE)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
    
    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            self.rotaryCallback(GPIO.input(self.dataPin))
        """
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)
        
        self.rotaryCallback(GPIO.input(self.dataPin))
        """

    def _switchCallback(self, pin):
        """
        if GPIO.input(self.switchPin) == 0:
            self.switchCallback()
        """
        self.switchCallback()

#test
if __name__ == "__main__":

    print ('Program start.')

    CLOCKPIN = 5
    DATAPIN = 6
    SWITCHPIN = 3

    def rotaryChange(direction):
        print ("turned - " + str(direction))
    def switchPressed(pin):
        print ("button connected to pin:{} pressed".format(pin))

    GPIO.setmode(GPIO.BCM)
    ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChange, switchPressed)

    print ("Launch switch monitor class.")

    ky040.start()
    print ("Start program loop...")
    try:
        while True:
            sleep(10)
            print ("Ten seconds...")
    finally:
        print ("Stopping GPIO monitoring...")
        ky040.stop()
        GPIO.cleanup()
        print ("Program ended.")
