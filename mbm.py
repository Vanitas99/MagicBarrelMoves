from synth import *
import RPi.GPIO as GPIO
import time

    
#GPIO definieren (Modus, Pins, Output)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def calculate_distance():
    # Trig High setzen
    GPIO.output(GPIO_TRIGGER, True)
 
    # Trig Low setzen (nach 0.01ms)
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
    

if __name__ == "__main__":
  
  
    init_pygame()
    
    tones = [Note(261.626, wave="square"),
             Note(293.665, wave="square"),
             Note(329.628, wave="square"),
             Note(349.228, wave="square"),
             Note(391.995, wave="square"),
             ]
  
  
    #drums = DrumKit(1)
    #bpm_machine = BPMPlayer("met4th.wav","metronome.wav",120,4, 1)
    #bpm_machine.start()
    
    running = True
    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height))
    
    
    
    
    while running:
        
        distance = calculate_distance()
        print("distance = %d cm" % distance)
        time.sleep(0.01)
        if distance = < 10:
            tones[0].play(-1)
        
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()