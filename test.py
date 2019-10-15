from synth import *
import time

init_pygame()
note = Note(330,wave="square")
print(note.frequency)
time.sleep(1)
while True:
    note.play(-1)