import pygame
from pygame.mixer import Sound, get_init, pre_init
import array
import numpy as np
from operator import add
import wave
import time
import threading
import random


class DrumKit():

    def __init__(self, vol):
        self.vol = vol
        self.kick = pygame.mixer.Sound("bassdrum.wav")
        self.snare = pygame.mixer.Sound("snare.wav")
        self.hat = pygame.mixer.Sound("hat.wav")
        self.clap = pygame.mixer.Sound("clap.wav")

class Chords():

    def __init__(self, vol):
        self.vol = vol
        self.am = pygame.mixer.Sound("chords/chord_am.wav")
        self.f = pygame.mixer.Sound("chords/chord_f.wav")
        self.c = pygame.mixer.Sound("chords/chord_c.wav")
        self.g = pygame.mixer.Sound("chords/chord_g.wav")


class Organ():
    def __init__(self, vol):
        self.vol = vol
        self.c1 = pygame.mixer.Sound("organ/organ_c1.wav")
        self.d = pygame.mixer.Sound("organ/organ_d.wav")
        self.e = pygame.mixer.Sound("organ/organ_e.wav")
        self.f = pygame.mixer.Sound("organ/organ_f.wav")
        self.g = pygame.mixer.Sound("organ/organ_g.wav")
        self.a = pygame.mixer.Sound("organ/organ_a.wav")
        self.h = pygame.mixer.Sound("organ/organ_h.wav")
        self.c2 = pygame.mixer.Sound("organ/organ_c2.wav")

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

    def load_wav(self, click_file, clack_file):
        self.clack = pygame.mixer.Sound(clack_file)
        self.click = pygame.mixer.Sound(click_file)

class DrumLooper(threading.Thread):
    def __init__(self, bpm, bpb, vol):
        threading.Thread.__init__(self)
        self.load_wav()
        self.bpm = bpm
        self.bpb = bpb
        self.sleep = (60 / self.bpm)*4
        self.vol = 0.5

    def run(self):
        while True:
            rnd = random.randint(0,2)
            if self.bpm == 70:
                if rnd == 0:
                    self.dl1_70.play()
                if rnd == 1:
                    self.dl2_70.play()
                if rnd == 2:
                    self.dl3_70.play()
            if self.bpm == 80:
                if rnd == 0:
                    self.dl1_80.play()
                if rnd == 1:
                    self.dl2_80.play()
                if rnd == 2:
                    self.dl3_80.play()
            if self.bpm == 90:
                if rnd == 0:
                    self.dl1_90.play()
                if rnd == 1:
                    self.dl2_90.play()
                if rnd == 2:
                    self.dl3_90.play()
            if self.bpm == 100:
                if rnd == 0:
                    self.dl1_100.play()
                if rnd == 1:
                    self.dl2_100.play()
                if rnd == 2:
                    self.dl3_100.play()
            if self.bpm == 110:
                if rnd == 0:
                    self.dl1_110.play()
                if rnd == 1:
                    self.dl2_110.play()
                if rnd == 2:
                    self.dl3_110.play()
            if self.bpm == 120:
                if rnd == 0:
                    self.dl1_120.play()
                if rnd == 1:
                    self.dl2_120.play()
                if rnd == 2:
                    self.dl3_120.play()
            if self.bpm == 130:
                if rnd == 0:
                    self.dl1_130.play()
                if rnd == 1:
                    self.dl2_130.play()
                if rnd == 2:
                    self.dl3_130.play()
            if self.bpm == 140:
                if rnd == 0:
                    self.dl1_140.play()
                if rnd == 1:
                    self.dl2_140.play()
                if rnd == 2:
                    self.dl3_140.play()
            time.sleep(self.sleep)

    def load_wav(self):
        self.dl1_70 = pygame.mixer.Sound("drumloops/dl1_70.wav")
        self.dl1_80 = pygame.mixer.Sound("drumloops/dl1_80.wav")
        self.dl1_90 = pygame.mixer.Sound("drumloops/dl1_90.wav")
        self.dl1_100 = pygame.mixer.Sound("drumloops/dl1_100.wav")
        self.dl1_110 = pygame.mixer.Sound("drumloops/dl1_110.wav")
        self.dl1_120 = pygame.mixer.Sound("drumloops/dl1_120.wav")
        self.dl1_130 = pygame.mixer.Sound("drumloops/dl1_130.wav")
        self.dl1_140 = pygame.mixer.Sound("drumloops/dl1_140.wav")
        self.dl2_70 = pygame.mixer.Sound("drumloops/dl2_70.wav")
        self.dl2_80 = pygame.mixer.Sound("drumloops/dl2_80.wav")
        self.dl2_90 = pygame.mixer.Sound("drumloops/dl2_90.wav")
        self.dl2_100 = pygame.mixer.Sound("drumloops/dl2_100.wav")
        self.dl2_110 = pygame.mixer.Sound("drumloops/dl2_110.wav")
        self.dl2_120 = pygame.mixer.Sound("drumloops/dl2_120.wav")
        self.dl2_130 = pygame.mixer.Sound("drumloops/dl2_130.wav")
        self.dl2_140 = pygame.mixer.Sound("drumloops/dl2_140.wav")
        self.dl3_70 = pygame.mixer.Sound("drumloops/dl3_70.wav")
        self.dl3_80 = pygame.mixer.Sound("drumloops/dl3_80.wav")
        self.dl3_90 = pygame.mixer.Sound("drumloops/dl3_90.wav")
        self.dl3_100 = pygame.mixer.Sound("drumloops/dl3_100.wav")
        self.dl3_110 = pygame.mixer.Sound("drumloops/dl3_110.wav")
        self.dl3_120 = pygame.mixer.Sound("drumloops/dl3_120.wav")
        self.dl3_130 = pygame.mixer.Sound("drumloops/dl3_130.wav")
        self.dl3_140 = pygame.mixer.Sound("drumloops/dl3_140.wav")

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
    def __init__(self,frequency, volume = .3, wave="square"):
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
            #print("%d -> sample nr %d" % (samples[time], time))
        return samples

    def osc(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array.array("h", [0] * period)
        for time in range(period):
            samples[time] = int( self.vol * (np.sin(self.w(self.frequency) * time / 44100 
                + 1 * self.frequency * np.sin(self.w(10))*time/44100))  * 32767)
            #print("%d -> sample nr %d" % (samples[time], time))
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


def post_play():
    newevent = pygame.event.Event(pygame.KEYDOWN, unicode="w", key=pygame.K_w, mod=pygame.KMOD_NONE) #create the event
    pygame.event.post(newevent) #add the event to the queue

def post_stop():
    newevent = pygame.event.Event(pygame.KEYUP, unicode="w", key=pygame.K_w, mod=pygame.KMOD_NONE) #create the event
    pygame.event.post(newevent) #add the event to the queue

def set_vol(tones, bpm_player, volume):
    for tone in tones.values():
        tone.set_volume(volume)
    bpm_player.clack.set_volume(vol)
    bpm_player.click.set_volume(vol)


if __name__ == "__main__":
    init_pygame()
    #drums = DrumKit(1)
    #bpm = BPMPlayer("met4th.wav","metronome.wav",120,4, 1)
    #bpm.start()

    #sound_bass = pygame.mixer.Sound("bassdrum.wav")
    #sound_snare = pygame.mixer.Sound("snare.wav")

    distance = 0

   
    vol = 1

    running = True
    tones = {
        #pygame.K_w: Note(261.626, wave="square"),
        #pygame.K_a: Note(293.665, wave="square"),
        #pygame.K_s: Note(329.628, wave="square"),
        #pygame.K_d: Note(349.228, wave="square"),
        #pygame.K_f: Note(391.995, wave="square"),
        #pygame.K_g: Note(440.000, wave="saw"),
        # pygame.K_u: Note(493.883, wave="saw"),
        # pygame.K_i: Note(523.251, wave="saw"),
        #pygame.K_LEFT: drums.kick,
        #pygame.K_RIGHT: drums.snare,
        #pygame.K_UP: drums.hat,
        #pygame.K_DOWN: drums.clap

    }
    
    #tone_array = [Note(260,wave="square")]
    sensor_thread = threading.Thread(target = calculate_distance) 
    sensor_thread.start()
    

    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height), FULLSCREEN)

    flag = False

    while running:
    
        for event in pygame.event.get():

            # closing window
            if event.type == pygame.QUIT:
                running = False

            # pressing key
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    flag = True

                if event.key in tones:
                    print('press:', event.key)
                    if isinstance(tones[event.key], Note):
                        tones[event.key].play(-1)
                    else:
                        if not flag:
                            tones[event.key].play()

                if flag:
                    if event.key == pygame.K_RIGHT:
                        print("BPM: %d" % bpm.bpm)
                        if bpm.bpm <= 400: #limiting fastest speed
                            bpm.bpm += 10
                    if event.key == pygame.K_LEFT:
                        print("BPM: %d" % bpm.bpm)
                        if bpm.bpm > 10:  #limiting slowest speed
                           bpm.bpm -= 10
                    if event.key == pygame.K_UP:
                        if vol < 1.0:
                            vol += 0.1
                            set_vol(tones,bpm,vol)
                            print("Volume: %.1f" % vol)
                    if event.key == pygame.K_DOWN:
                        if vol > 0.0:
                            vol -= 0.1
                            set_vol(tones, bpm, vol)
                            print("Volume: %.1f" % vol)

            # releasing key
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    flag = False
                if event.key in tones:
                    print('release:', event.key)
                    tones[event.key].stop()


    pygame.quit()
    GPIO.cleanup()
