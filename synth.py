import pygame
from pygame.mixer import Sound, get_init, pre_init
import array
import numpy as np
from operator import add
import wave
import time
import threading
from pynput.keyboard import Key, Controller

class BPMPlayer(threading.Thread):
    def __init__(self, click_file, clack_file, bpm, bpb, vol):
        threading.Thread.__init__(self)
        self.load_wav(click_file, clack_file)
        self.bpm = bpm
        self.bpb = bpb
        self.sleep = 60 / self.bpm
        self.vol = 0.5

    def run(self):
        counter = 0
        while True:
            counter += 1
            self.sleep = 60 / self.bpm
            if counter % self.bpb:
                self.clack.play()
            else:
                self.click.play()
            time.sleep(self.sleep)

    def bpm_change(self):
        self._stop()

    def load_wav(self, click_file, clack_file):
        self.clack = pygame.mixer.Sound(clack_file)
        self.click = pygame.mixer.Sound(click_file)

    

class Chord(pygame.mixer.Sound):
    def __init__(self , volume = 1, **chord):
        self.base_freq = 400
        chords = {
            "C": [Note(261), Note(329), Note(391)],
        }
        self.samples = self.build_chord_samples([Note(261),Note(329),Note(391)])
        pygame.mixer.Sound.__init__(self, self.samples)

    def build_chord_samples(self, notes):
        period = int(round(pygame.mixer.get_init()[0] / self.base_freq))
        samples = array.array("h", [0] * period)
    
        for note in notes:
            samples = list(map(add,note.samples,samples))
        return array.array("h", samples)


class Note(pygame.mixer.Sound):
    def __init__(self,frequency, volume = .3, wave="sin"):
        self.frequency = frequency
        self.vol = volume
        wave_forms = {
            "sin": self.build_sinwave_samples(),
            "square": self.build_squarewave_samples(),
            "saw": self.build_sawwave_samples(),
            "osc": self.osc()
        }
        self.samples = wave_forms[wave]
        pygame.mixer.Sound.__init__(self, self.samples)
        

    # square wave
    def build_squarewave_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        #amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        amplitude = 32767
        for time in range(period):
            if time < period / 2:
                samples[time] = int(self.vol * amplitude)
            else:
                samples[time] = int(self.vol * -amplitude)
    
        return samples

    def build_sinwave_samples(self, overtones = 1):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        for time in range(period):
            samples[time] = int( self.vol * (np.sin(overtones * self.w(self.frequency) * time / 44100)/  overtones * 32767))
            print("%d -> sample nr %d" % (samples[time], time))
        return samples
    
    def osc(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        for time in range(period):
            samples[time] = int( self.vol * (np.sin(self.w(self.frequency) * time / 44100 
                + 1 * self.frequency * np.sin(self.w(10))*time/44100))  * 32767)
            print("%d -> sample nr %d" % (samples[time], time))
        return samples

    def build_sawwave_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        for overtones in range(1, 10):
            ret = self.build_sinwave_samples(overtones)
            samples = list(map(add,ret,samples))
        
        return array.array("h", samples)

    def w(self, hertz):
        return hertz * 2 * np.pi


def init_pygame():
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()


class ADSR():
    def __init__(self):
        self.attack_time = 0.01
        self.decay_time = 0.01
        self.release_time = 0.02

        self.sustain_amplitude = 0.8
        self.start_amplitude = 1

        self.trigger_on_time = 0
        self.trigger_off_time = 0

        self.note_on = False

    def get_amplitude(self):
        pass

    def note_on(self, time):
        self.trigger_on_time = time
        self.note_on = True

    def note_off(self, time):
        self.trigger_off_time = time
        self.note_on = False

def t():
    newevent = pygame.event.Event(pygame.KEYDOWN, unicode="q", key=pygame.K_q, mod=pygame.KMOD_NONE) #create the event
    pygame.event.post(newevent) #add the event to the queue

def tt():
    newevent = pygame.event.Event(pygame.KEYUP, unicode="q", key=pygame.K_q, mod=pygame.KMOD_NONE) #create the event
    pygame.event.post(newevent) #add the event to the queue


if __name__ == "__main__":
    init_pygame()
    bpm = BPMPlayer("met4th.wav","metronome.wav",120,4)
    bpm.start()

    pygame.mixer.sound.set_volume(vol)

    tones = {
        pygame.K_UP: Note(261.626, wave="saw"),
        pygame.K_DOWN: Note(293.665, wave="saw"),
        pygame.K_LEFT: Note(329.628, wave="saw"),
        pygame.K_RIGHT: Note(349.228, wave="saw"),
        pygame.K_t: Note(391.995, wave="saw"),
        pygame.K_z: Note(440.000, wave="saw"),
        pygame.K_u: Note(493.883, wave="saw"),
        pygame.K_i: Note(523.251, wave="saw")
    }

    running = True
  
    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height))

    while running:
        for event in pygame.event.get():

            # closing window
            if event.type == pygame.QUIT:
                running = False

            # pressing key
            elif event.type == pygame.KEYDOWN:
                if event.key in tones:
                    print('press:', event.key)
                    tones[event.key].fadeout(50)
                    tones[event.key].play(-1)
                if event.key == pygame.K_n:
                    print("SPEED UP :D")
                    if bpm.bpm <= 400: #limiting fastest speed
                       bpm.bpm += 10
                if event.key == pygame.K_m:
                    print("SLOW DOWN D:")
                    if bpm.bpm > 10:  #limiting slowest speed
                       bpm.bpm -= 10
                if event.key == pygame.K_b:
                    t()
                if event.key == pygame.K_UP:
                    if vol < 1.0
                        vol += 0.1
                        pygame.mixer.sound.set_volume(vol)
                if event.key == pygame.K_DOWN:
                    if vol > 0.0
                        vol -= 0.1
                        pygame.mixer.sound.set_volume(vol)

            # releasing key
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    tt()
                if event.key in tones:
                    print('release:', event.key)
                    tones[event.key].stop()
                    

    pygame.quit()

