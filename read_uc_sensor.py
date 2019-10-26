import RPi.GPIO as GPIO
import time
import pygame
import synth as sy

#GPIO definieren (Modus, Pins, Output)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
 
def entfernung():
    # Trig High setzen
    GPIO.output(GPIO_TRIGGER, True)
 
    # Trigger Low setzen (nach -0.01ms)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

 
    Startzeit = time.time()
    Endzeit = time.time()
 
    # Start/Stop Zeit ermitteln
    while GPIO.input(GPIO_ECHO) == 0:
        Startzeit = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        Endzeit = time.time()
 
    # Vergangene Zeit

    Zeitdifferenz = Endzeit - Startzeit
    
    # Schallgeschwindigkeit (34300 cm/s) einbeziehen
    entfernung = (Zeitdifferenz * 34300) / 2
 
    return entfernung

def switch_playing_note(index):
    global playing_indx
    
    if playing_indx is not None:
        tones[playing_indx].stop()
        playing_indx = index
        tones[index].play(-1)
 
if __name__ == '__main__':
    
    sy.init_pygame()
    tones = [sy.Note(261.626, wave="square"),
             sy.Note(293.665, wave="square"),
             sy.Note(329.628, wave="square")]
    
    running = True
    note_playing = False
    
    playing_indx = None
    
    try:
        while running:
            distanz = entfernung()
            print ("Distanz = %f cm" % distanz)
            time.sleep(0.02)
            if(distanz <= 10):
                if playing_indx != 0:
                    switch_playing_note(0)
            elif(distanz > 10 and distanz <= 20):
                if playing_indx != 1:
                    switch_playing_note(1)
            elif(distanz > 20 and distanz <= 30):
                if playing_indx != 2:
                    switch_playing_note(2)
            else:
                if playing_indx is not None:
                    tones[playing_indx].stop()
                    playing_indx = None
            
 
        # Programm beenden
    except KeyboardInterrupt:
        print("Programm abgebrochen")
        GPIO.cleanup()
