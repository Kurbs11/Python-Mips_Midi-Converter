# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:34:35 2024

@author: Chris Kurbiel
"""
import random

#Consider adding randomizer feature
def MIDI( sync, pitch, length, instrument, vol):
    fname = open("midifile.txt", "a")
    if (sync):
        fname.write("li $v0 33\n")
    else:
        fname.write("li $v0 31\n")
    fname.write("li $a0," + str(pitch) + "\n")
    fname.write("li $a1," + str(length) + "\n")
    fname.write("li $a2," + str (instrument) + "\n")
    fname.write("li $a3," + str(vol) + "\n")
    fname.write("syscall\n")
    fname.close()
    return

def sleep(duration):
    fname = open("midifile.txt", "a")
    fname.write("li $v0 32\n")
    fname.write("li $a0," + str(duration) + "\n")
    fname.write("syscall\n")
    fname.close()
    return
    
def pitch_calc(tone, octave, notes):
    difference = octave-4
    #If you want C2, then that's C4 + (12*-2) => 60-24
    #If you want C7, then that's C4 + (12*3) => 96
    return notes[tone] +12*difference
    
    
    
def instrument_codes(): 
    print("0-7: Piano, 8-15: Chromatic Percussion")
    print("16-23: Organ, 24-31: Guitar")
    print("32-39: Bass, 40-47: Strings")
    print("48-55: Ensemble, 56-63: Brass")
    print("64-71: Reed, 72-79 Pipe")
    print("80-87: Synth Lead, 88-95: Synth Pad")
    print("96-103: Synth Effects, 104-111: Ethnic")
    print("112-119: Percussion, 120-127: SFX")
    return
        
    
#if __name__=="main":
    #Based on B#4-B4
notes = {"B#":60,
         "C": 60,
         "C#":61,
         "Db": 61,
         "D":62,
         "D#":63,
         "Eb": 63,
         "E": 64,
         "E#":65,
         "F":65,
         "F#":66,
         "Gb": 66,
         "G":67,
         "G#":68,
         "Ab":68,
         "A":69,
         "A#":70,
         "Bb":70,
         "B":71
    }
random_tone = ["C","C#","D","D#","E","F", "F#", "G", "G#", "A", "Bb", "B"]

print("Welcome to the Python-MIDI-Mips converter (PMMC)")
valid_number = False
while (valid_number == False):
    mode = input("Press 1 to create your own music. Press 0 to randomize a song. ")
    try:
        mode = int(mode)
        if (mode < 0):
            mode = 0
        if (mode > 1):
            mode = 1
        valid_number = True
    except:
        print("Error: Invalid Mode selection (expecting integer)")
    
midi_file = open("midifile.txt", "w") #Creates a new file(if it doesn't already exist) to store midi instructions
midi_file.write("li $v0 33\nli $a0,69\nli $a1,300\nli $a2,2\nli $a3,80\nsyscall\n")
keep_composing = True
while (keep_composing):
    #First section handles if command is synchronous
    if(mode):
        valid_number = False
        while (valid_number == False):
            sync = input("Press 1 for single note, 0 for chord: ")
            try:
                sync = int(sync)
                if sync >=1:
                    sync =1
                if sync <=0:
                    sync = 0
                valid_number = True    
            except:
                print("Please provide a number")
    elif (not mode): #AKA Randomizer 
            sync = random.randrange(0,2) #Consider weighting single notes and chords differently
    #This section decides pitch
    if(mode):
        valid_pitch = False
        while (valid_pitch == False):
            pitch = input("Select pitch (ex: C, F#, or Ab): ")
            if (pitch in notes):
                valid_pitch = True
            else:    
                print("Please select a valid pitch in the 12-tone equal temperment (A-G#)")
        valid_number = False
        while (valid_number == False):
            octave = input("Select the octave for this pitch (-2 to 8) ")
            try:
                octave = int(octave)
                if (octave == -2 and (pitch == "Ab" or pitch == "A" or pitch == "A#" or pitch == "Bb" or pitch == "B")):
                    print("Error: The lowest pitch selectable is C-2")
                    continue
                if (octave == 8 and pitch == "G#"):
                    print("Error: The highest pitch selectable is G8")
                    continue
                if (octave < -2 or octave > 8):
                    print("Error: Out of Octave range")
                    continue
                note = pitch_calc(pitch,octave, notes) #Will be used for Midi's pitch argument ($A0)
                print("Midi value: ", note)
                valid_number = True
            except:
                print("Please provide a number")
    elif(not mode):
              pitch = random_tone[random.randrange(0,len(random_tone))]
              octave = random.randrange(-2,9)
              note = pitch_calc(pitch, octave, notes)
    #This section is for duration control  
    if(mode):      
        valid_number = False
        while (valid_number == False):
            length = input("Select the note duration in ms: ")
            try:
                length = int(length)
                if (length < 0):
                    print("Error: Duration less than zero")
                    continue
                valid_number = True
                
            except:
                print("Please select a valid integer")
    elif(not mode):
        length = random.randrange(200,2000,50) #Not 1800 Choices, but 1800/50
    #This section is for Instrument selection 
    if(mode):       
        valid_number = False        
        while (valid_number == False):
            print("Select an instrument (0-127)")
            choice = input("Type \"128\" to display a list of instruments or type 0-127: ")
            try:
                instrument = int(choice)
                if (instrument == 128):
                    instrument_codes()
                    continue
                if(instrument < 0 or instrument > 128):
                    print("Error: Instrument Out of Range")
                    continue
                valid_number = True
            except:
                print("Error: Wrong instrument format (expecting integer)")
    elif(not mode):
        instrument = random.randrange(0,128) 
    #This section is for volume control
    if (mode):
        valid_number = False
        while (valid_number == False):
            volume = input("Select the volume (0-127): ")
            try:
                volume = int(volume)
                if (volume > 128):
                    print("volume will be set to max")
                    volume = 128
                if (volume < 0):
                    print("volume will be mute")
                    volume = 0
                valid_number = True
            except:
                print("Error: Invalid volume format (expecting integer)")
    if(not mode):
        volume = random.randrange(0,128)
    #Putting it all together        
    MIDI(sync, note, length, instrument, volume)
    if(mode):
        keep_composing = input("Continue adding notes? (1/Y or 0/N) ")
        if( keep_composing != "1" and keep_composing != "Y" and keep_composing != "y"):
            keep_composing = False
            break
    elif(not mode):
        weighted_decision = random.randrange(0,10)
        if(weighted_decision == 9):
            keep_composing = False
            print("CPU decides to terminate.")
            break
        print("CPU decides to continue.")
    if(mode):        
        choice = input("Pause between notes? (1/Y or 0/N) ") 
        if (choice == "1" or choice == "Y" or choice == "y"):
            valid_number = False
            while (valid_number == False):
                pause = input("Select pause duration in ms: ")
                try:
                    pause = int(pause)
                    sleep(pause)
                    valid_number = True
                except:
                    print("Error: Invalid pause format (expecting integer)")
    elif(not mode):
        weighted_decision = random.randrange(0,5)
        if(weighted_decision>=3):
            sleep_amount = random.randrange(250,1000,50)
            sleep(sleep_amount)
    #It is recommended to Pause in after switching between chords (syscall-31) and single notes (syscall-33)
    #Known issue in MARS: System always cuts out first note, so I hardcoded the brief call that will be cut out (~Line 91)          
    #Additionally, many waveforms don't start producing noise until ~250ms    