# coding=UTF-8
import RPi.GPIO as GPIO
import time
import pygame
import synth as sy
import threading
import os
import sys
from KY040 import KY040

pid = str(os.getpid())
f = open('/mbm.pid','w')
f.write(pid)
f.close()


#GPIO definieren (Modus, Pins, Output)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

CLOCKPIN = 5
DATAPIN = 6
SWITCHPIN = 13

os.environ["SDL_VIDEODRIVER"] = "dummy" 


# Berechnung der Distanz mit HC-SR04 Ultrasound Sensor 
def entfernung():
    #global last_read_distance
    #global last_last_read_distance

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
    #if max(last_read_distance,entfernung)-min(last_read_distance,entfernung) > 30:
        #last_read_distance=entfernung
        #return -1
    #last_read_distance = entfernung
    return int(entfernung)

#Handle alle Änderungen, wenn eine andere Note gepspielt werden soll
def switch_playing_note(index):
    global playing_indx

    if playing_indx is None:
        playing_indx = index
        tones[index].play(-1)

    if playing_indx is not None:
        tones[playing_indx].stop()
        playing_indx = index
        tones[index].play(-1)
    print(playing_indx)

# wird als Thread ausgeführt
def read_from_sensor(stop):
    global playing_indx

    while True:

        if stop():
            break
        distanz = entfernung()
        #print ("Distanz = %d cm" % distanz)
        time.sleep(0.05)

        # Je nach Länge des IRL Moduls, werden Noten relativ zur Gesamtlänge gespielt
        if(distanz>=0 and distanz <= 1*threshold):
            if playing_indx != 0:
                switch_playing_note(0)
        elif(distanz > 1*threshold and distanz <= 2*threshold):
            if playing_indx != 1:
                switch_playing_note(1)
        elif(distanz > 2*threshold and distanz <= 3*threshold):
            if playing_indx != 2:
                switch_playing_note(2)
        elif(distanz > 3*threshold and distanz <= 4*threshold):
            if playing_indx != 3:
                switch_playing_note(3)
        elif(distanz > 4*threshold and distanz <= 5*threshold):
            if playing_indx != 4:
                switch_playing_note(4)
        elif(distanz > 5*threshold and distanz <= 6*threshold):
            if playing_indx != 5:
                switch_playing_note(5)
        elif(distanz > 6*threshold and distanz <= 7*threshold):
            if playing_indx != 6:
                switch_playing_note(6)
        elif(distanz > 7*threshold and distanz <= 8*threshold):
            if playing_indx != 7:
                switch_playing_note(7)
        else:
            if playing_indx is not None:
                 tones[playing_indx].stop()
                 playing_indx = None
    

# Beenden des US Threads, Drehregler Threads und GPIO Cleanup
def stop_program():
    global stop_threads
    stop_threads = True
    ky040.stop()
    GPIO.cleanup()
    exit
    
    

# Einstiegspunkt in das Skript
if __name__ == '__main__':
   
    
    # BPM entsprechend der Drehrichtung des Reglers anpassen
    def rotary_change(direction):
        if direction == 1:
            if bpm_player.bpm < 400:
                bpm_player.bpm += 10
        else:
            if bpm_player.bpm > 10:
                bpm_player.bpm -= 10
           
        print("Bpm %d" % bpm_player.bpm)
    
    # OPTIONAL Funktionalität bei Druck des Drehreglers
    def switch_pressed():
        pass
    
    last_read_distance = -1
    last_last_read_distance = -1
    
    # Init Pygame module
    sy.init_pygame()
    screen = pygame.display.set_mode(  (320,320))
    
    pygame.mixer.Sound("Intro-_Sound_.wav").play()
    time.sleep(6)
    
    # DrumKit aus synth.py initialisieren
    drums = sy.DrumKit(1)
    
    # Diese Noten werden vom US Sensor genutzt
    tones = [sy.Note(261, wave="square"),
             sy.Note(293, wave="square"),
             sy.Note(329, wave="square"),
             sy.Note(349, wave="square"),
             sy.Note(392, wave="square"),
             sy.Note(440, wave="square"),
             sy.Note(494, wave="square"),
             sy.Note(523, wave="square")
            ]

    # Tasteninputs vom Makey makey auf Drumkit gemapt
    perc = {pygame.K_w: drums.hat,
            pygame.K_a: drums.kick,
            pygame.K_s: drums.clap,
            pygame.K_d: drums.snare
           }
    
    running = True
    
    # zeigt den Index der aktuell gespielten Note an  
    playing_indx = None
    
    # Länge des Moduls IRL
    length_module_irl = 35
    threshold = length_module_irl / len(tones)

    # BPM Player aus synth.py initialisieren
    bpm_player = sy.BPMPlayer("met4th.wav","metronome.wav",120,4,1)
    bpm_player.start()
    

    # Thread zum Lesen der Entfernung starten
    stop_threads = False
    sensor_thread = threading.Thread(target=read_from_sensor, args =(lambda : stop_threads, ))
    sensor_thread.start()
    
    GPIO.setmode(GPIO.BCM)
    
    # Modul zum Auslesen des Drehreglers initialisieren
    ky040 = KY040(CLOCKPIN,DATAPIN,SWITCHPIN,rotary_change,switch_pressed)
    ky040.start()


    # Main Loop
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in perc:
                        print("key pressed")
                        perc[event.key].play()
            
        
        # Programm beenden
    except KeyboardInterrupt:
        print("\nProgramm abgebrochen")
        stop_program()
    finally:
        stop_program()
        
