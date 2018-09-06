# Random-Chord-Generator
Designed for practising the ear. Requires MIDIUtil (https://github.com/MarkCWirt/MIDIUtil), and Windows Media Player (https://support.microsoft.com/en-us/help/18612/windows-media-player) set as default MIDI player (support for other players planned for future update). Tested with Python 3.5.

## Description
random_chord_gen.py generates a MIDI file in the working directory which contains a random chord. This is automatically opened by WMPlayer during runtime. The user inputs their answer based on the pitches they hear. Every correct answer adds a point to the user's score. A wrong answer quits the program.
## How to use
To enter your answer, enter the pitches you hear in ascending order, separated by a space, and hit enter. For instance, a B major chord starting on B4 would be written thus: 
```
B4 D#5 F#5
```
or even:
```
B4 Eb5 Gb5
```
The initial note will be provided for you.

Sharps (#) and flats (b) are treated enharmonically (i.e. the program treats D# and Eb as the same note. Pitches such as 'Cb' or 'E#', which are accidental but do not represent a black piano key, are not supported). 

Other options for the user to enter are:
- 'q' - quits the program
- 'new' - generates a new chord
- 'help1' - rolls chord
- 'help2' - rolls chord at slow speed
- 'back' - reverts to unrolled chord

### Chord customization
Chord parameters can be set at the top of random_chord_gen.py:
- chord_size - number of notes in chord
- low_interval - size of lowest allowed interval, in semitones
- high_interval - size of highest allowed interval, in semitones
- starting_note - can set range within which to generate starting note. Default is A2 -> B4.
  
