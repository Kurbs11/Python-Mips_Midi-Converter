# Python-Mips_Midi-Converter
The aim of this repository is to provide a convenient way to convert desired inputs about notes (such as pitch, duration, volume, and instrument) into the MARS MIPS Assembly code.

V1.1: Added support for a randomizer mode. Now, music can be generated randomly if the mode is selected. 

V1.0: Can customize between different pitches, durations, volumes, and instruments and convert it into MIPS assembly code that is recognized on the MARS simulator. This is leveraged through MARS' exclusive syscalls 31-33. The python script writes all the instructions to a file titled "midifile.txt", and the instructions can be copied and directly run in MARS.
