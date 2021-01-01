# -*- coding: utf-8 -*-
"""
*** Description ***
    Converts a progression to chords and plays them using fluidsynth.
    You should specify the SF2 soundfont file.
"""
from pynput.keyboard import Key, KeyCode, Listener

allowed_octaves = {'1','2','3','4','5','6','7'}
left_hand_octave_limit = '4'
left_octave = '3'
right_octave = '5'
pressed_keys = set()

def on_press(key):
    if(key not in pressed_keys):
        pressed_keys.add(key)
        # for line in key:
        if(isinstance(key, KeyCode) and key.char is not None):
            # octave config change
            if(key.char in allowed_octaves):
                if(key.char > left_hand_octave_limit):
                    global right_octave
                    right_octave = key.char
                else:
                    global left_octave
                    left_octave = key.char

                return True

            octave, note = map_key(key.char)
            if(note is not None):
                play(get_note(octave, note))
                return True

def on_release(key):
    if(isinstance(key, KeyCode) and key.char is not None):
        # octave config change
        if(key.char not in allowed_octaves):
            octave, note = map_key(key.char)
            if(note is not None):
                stop(get_note(octave, note))
        try:
            pressed_keys.remove(key)
        except KeyError:
            pass
        return True
    if key == Key.esc:
        # Stop listener
        return False

import sys
import select

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False


import pprint
import os
import asyncio
import aioconsole

import mingus.core.notes as notes
import mingus.core.value as value
from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys
from random import random

pp = pprint.PrettyPrinter(indent=4)

def print_inventory(dct):
    print("Note Mapping: new (standard)")
    pp.pprint(dct)

def get_note(octave, note):
    if note is None or not len(note):
        return
    # c = NoteContainer(note, octave)
    # print(c)
    return Note(note, octave)

def stop(note):
    fluidsynth.stop_Note(note)

def play(note):
    # p = c[1]
    # l.octave_down()

    # Play chord and lowered first note
    fluidsynth.play_Note(note)
    print(note)
    print("-" * 20)

qwerty_keys_to_standard = {
    # LEFT HAND
    'left': {
        'A': 'A',
        'Q': 'A#',
        'S': 'B',
        'W': 'B#',
        'D': 'D',
        'X': 'D#',
        'F': 'F',
        'R': 'F#',
        'E': 'E',
        'C': 'C',
        'V': 'C#',
        'G': 'G',
        'T': 'G#',
    },
    # RIGHT HAND
    'right': {
        ';': 'A',
        'P': 'A#',
        'L': 'B',
        'O': 'B#',
        'K': 'D',
        ',': 'D#',
        'J': 'F',
        'U': 'F#',
        'I': 'E',
        'M': 'C',
        'N': 'C#',
        'H': 'G',
        'Y': 'G#',
    }
}

standard_keys_to_qwerty = dict([(value, key) for key, value in qwerty_keys_to_standard['left'].items()]) | dict([(value, key) for key, value in qwerty_keys_to_standard['right'].items()]) 

print_inventory(qwerty_keys_to_standard.get('left'))
print_inventory(qwerty_keys_to_standard.get('right'))

def convert_to_note(char):
    value = qwerty_keys_to_standard['left'].get(char, None)
    if(value is not None):
        return (int(left_octave), value)
    else:
        return (int(right_octave), qwerty_keys_to_standard['right'].get(char, None))
    
# def map_keys(line):
#     chord = list()
#     origin = [char for char in line.decode().strip('\n')]
#     for index, char in enumerate(origin):
#         note, octave = map_key(char)
#         if note is not None:
#             chord.append(note)
#     return chord

def map_key(key):
    octave, note = convert_to_note(key.upper())
    if note is None or not notes.is_valid_note(note):
        print(f"invalid note: {key}")
    return (octave, note)

def convert(l):
    return { str(i) : v for i,v in enumerate(l) }

async def echo():
    # Collect events until released
    # list all pianos
    piano_folder = "25-Piano-Soundfonts"
    piano_options = convert(os.listdir(piano_folder))
    pp.pprint(piano_options)
    selected_piano = None
    while selected_piano is None:
        piano_name = input("Enter Piano: ")
        selected_piano = piano_options.get(piano_name)

    SF2 = f"{piano_folder}/{selected_piano}"
    key = input("Enter key: ")
    if not fluidsynth.init(SF2):
        print("Couldn't load soundfont", SF2)
        sys.exit(1)
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

loop = asyncio.get_event_loop()
loop.run_until_complete(echo())


"""
TODO
2. determine the length of key is held down and play until up
8. display as sheet music 
"""
