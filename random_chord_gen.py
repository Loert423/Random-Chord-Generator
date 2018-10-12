# -*- coding: utf-8 -*-
"""
random_chord_gen.py - v1.0
A short program for practising the ear
(Present) requirements: MIDIUtils, and WMPlayer set as default MIDI player
Created on Thu Feb  9 17:02:38 2017

@author: Tomek
"""

#!/usr/bin/env python

from midiutil.MidiFile import MIDIFile
import numpy as np
import os
import subprocess
import sys
import time

from ast import literal_eval

#dictionaries for parsing user input
note_name_dict = {'A#2': 46, 'A#0': 22, 'Ab1': 32, 'Db4': 61, 'Eb3': 51, 'A5': 81, 'A1': 33, 'Ab4': 68, 'Gb1': 30, 'C#3': 49, 'Db2': 37, 'D#4': 63, 'D3': 50, 'Ab2': 44, 'Bb3': 58, 'F#3': 54, 'B7': 107, 'A#5': 82, 'D#7': 99, 'D#3': 51, 'Db1': 25, 'C6': 84, 'F4': 65, 'Db5': 73, 'E7': 100, 'C3': 48, 'Eb6': 87, 'Ab5': 80, 'B5': 83, 'G#1': 32, 'G6': 91, 'E1': 28, 'B1': 35, 'Ab6': 92, 'Bb5': 82, 'E6': 88, 'C2': 36, 'E4': 64, 'D#2': 39, 'F6': 89, 'F3': 53, 'C#1': 25, 'Eb4': 63, 'D4': 62, 'Bb6': 94, 'C5': 72, 'C1': 24, 'A#3': 58, 'A0': 21, 'D5': 74, 'A2': 45, 'Eb7': 99, 'A3': 57, 'Gb5': 78, 'D#5': 75, 'B2': 47, 'F#6': 90, 'G5': 79, 'F1': 29, 'A#6': 94, 'F2': 41, 'F#7': 102, 'Ab3': 56, 'G#3': 56, 'C#6': 85, 'A6': 93, 'D#1': 27, 'Eb5': 75, 'G#6': 92, 'E5': 76, 'G#7': 104, 'G2': 43, 'A#4': 70, 'C7': 96, 'G1': 31, 'B0': 23, 'A#7': 106, 'Bb7': 106, 'Gb7': 102, 'G4': 67, 'F7': 101, 'F#2': 42, 'Eb2': 39, 'Bb0': 22, 'B3': 59, 'A7': 105, 'C4': 60, 'Ab7': 104, 'Db3': 49, 'B6': 95, 'C#2': 37, 'C#5': 73, 'B4': 71, 'C#7': 97, 'Gb3': 54, 'G7': 103, 'Eb1': 27, 'E2': 40, 'F#4': 66, 'G3': 55, 'C#4': 61, 'Db7': 97, 'D6': 86, 'Gb6': 90, 'F5': 77, 'G#4': 68, 'A#1': 34, 'G#2': 44, 'G#5': 80, 'C8': 108, 'Bb1': 34, 'Gb4': 66, 'A4': 69, 'D2': 38, 'Db6': 85, 'D#6': 87, 'Gb2': 42, 'Bb4': 70, 'F#5': 78, 'Bb2': 46, 'E3': 52, 'D7': 98, 'D1': 26, 'F#1': 30}
intervals = {'U': 0, 'M3': 4, 'M2': 2, 'm7': 10, 'O': 12, 'D5': 6, 'M7': 11, 'm3': 3, 'm2': 1, 'm6': 8, 'P4': 5, 'M6': 9, 'P5': 7}

points = 0  #keeps the score
state = 2   #state 1 = interval test (WIP), state 2 = chord test
chord_size = 4  #number of notes in chord
low_interval = 1    #minimum interval in chord (semitones)
high_interval = 4   #maximum interval in chord (semitones)

if sys.argv[1]:
    chord_size = int(sys.argv[1])
    print(f'Chord size is {chord_size}')
if sys.argv[2]:
    int_range = literal_eval(sys.argv[2])
    if isinstance(int_range[0], int) and isinstance(int_range[1], int):
        low_interval = int_range[0]
        high_interval = int_range[1]
        print(f'Interval range from {low_interval} to {high_interval}')
    else:
        raise ValueError('Interval range must be in integers.')

#start = eval(input('Starting note?: '))
#note_seq = list(range(40,80,7))

#MIDI file parameters
track    = 0
channel  = 0
tme      = 0   # Position of first note, in beats
duration = 7   # In beats
tempo    = 120  # In BPM
volume   = 100 # 0-127, as per the MIDI standard
program  = 0 #piano

#MIDI INITIALIZATION
def gen_MIDI(output, gap):
    tme = 0
    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
    MyMIDI.addTempo(track,tme, tempo)
    MyMIDI.addProgramChange(track, channel, tme, program)

    for pitch in degrees:   #filters pitch to within keyboard range, and adds to track (DOES NOT REPLACE NOTE)
        if pitch <= 108:
            MyMIDI.addNote(track, channel, pitch, tme, duration, volume)
            tme = tme + gap

    #writes to file
    with open(str(output), "wb") as output_file:
        MyMIDI.writeFile(output_file)

    if sys.platform == 'windows':
        os.startfile(str(output))   # WMPlayer must be set as default MIDI player
    elif sys.platform == 'linux':
        start_vlc_process = subprocess.Popen(['setsid', 'vlc', str(output)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(.5)
        focus_IPython = subprocess.Popen('wmctrl -a IPython', shell=True)


while state == 2:   #chord game

    if sys.platform == 'windows':
        #checks that WMPlayer is closed
        os.system("taskkill /f /im wmplayer.exe")
    elif sys.platform == 'linux':
        bash_command = 'killall -9 vlc'
        stop_vlc_process = subprocess.Popen(bash_command, shell=True)

    time.sleep(.1)

    start = np.random.randint(45,70)    # random starting note between A2 and B4
    i = np.random.randint(low_interval,high_interval+1,size = chord_size - 1)  # interval map, (low, high, number)

    note_seq = [start]  
    
    for (x,y) in note_name_dict.items():    # get note name, could be more efficient
        if y == start:
            name = x

    print("Root note is:" + name)   # gives user starting note (for those without perfect pitch)                

    for x in i:                         # generates chord using interval map
        y = note_seq[-1]
        note_seq.append(y+x)        

    degrees  = note_seq # MIDI note number
        
    gen_MIDI("output.mid", 0)       # outputs MIDI file

    while True: #user input handling
        try:
            ans_in = input("Notes? (q to quit): ")
            if ans_in == "q":
                break
            if ans_in == "new":
                break
            elif ans_in == "help1":  #play melodically
                gen_MIDI("output2.mid",1)
            elif ans_in == "help2":  #play melodically, longer gap
                gen_MIDI("output3.mid",2)
            elif ans_in == "back":
                gen_MIDI("output4.mid",0)   #back to chord mode
            else:
                ans = ans_in.split(" ")
                for z in range(0, len(ans)):
                    note = note_name_dict[ans[z]]
                    ans[z] = note
                break
        except KeyError:
            print("Invalid input, try again.")
        except PermissionError:
            print("Not allowed!")

    if ans_in == "new":
        for z in range(0, len(note_seq)):
            for (x,y) in note_name_dict.items():    #convert MIDI value into note name
                if y == note_seq[z]:
                    note_seq[z] = x
        print("Correct answer was: " + str(note_seq))
        state = 2
    elif ans == note_seq:
        print("Correct!")
        points += 1
    else:
        print("Wrong!")
        state = 0

while state == 1:   #WORK IN PROGRESS
        
    if sys.platform == 'windows':
        #checks that WMPlayer is closed
        os.system("taskkill /f /im wmplayer.exe")
    elif sys.platform == 'linux':
        bash_command = 'killall -9 vlc'
        subprocess.Popen(bash_command, shell=True)
    time.sleep(.1)

    i = np.random.randint(1,13,size=1)  # interval map, (low, high, number)

    start = 40                          # starting note
    note_seq = [start]                  

    for x in i:                         # generates chord
        y = note_seq[-1]
        note_seq.append(y+x)        

    degrees  = note_seq # MIDI note number
        
    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
    MyMIDI.addTempo(track,tme, tempo)
    MyMIDI.addProgramChange(track, channel, tme, program)

    for pitch in degrees:
        MyMIDI.addNote(track, channel, pitch, tme, duration, volume)
            #tme = tme + 1

    with open("major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    
    os.startfile("major-scale.mid")

    ans = input("Interval?: ")

    if intervals[ans] == (note_seq[-1] - note_seq[-2]):
        print("Correct!")
        points += 1
    else:
        state = 0

#os.system("taskkill /f /im wmplayer.exe")
        
for z in range(0, len(note_seq)):
    for (x,y) in note_name_dict.items():                      #convert MIDI value into note name
        if y == note_seq[z]:
            note_seq[z] = x
        
print("Correct answer is: " + str(note_seq))
print("Score: " + str(points))



#time.sleep(5.)

#os.system("taskkill /im wmplayer.exe")
