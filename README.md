# Random-Chord-Generator
A short program for practising the ear. Requires MIDIUtil, and Windows Media Player (wmplayer.exe) set as default MIDI player (internal player planned for future update). Written for Python 3.5.

The program generates a MIDI file in the local directory which is automatically opened and played by WMPlayer while the program is running.

To enter your answer, enter the notes you hear in ascending order, separated by a space (e.g. if you hear a B major chord starting on B4 enter: "B4 D#5 F#5). Sharps (#) and flats (b) are treated enharmonically. 

Other options for the user to enter are:
  'q' - quits the program
  'new' - generates a new chord
  'help1' - rolls chord
  'help2' - rolls chord at slow speed
  'back' - reverts to unrolled chord

Chord parameters are set near top of file:
  chord_size - number of notes in chord
  low_interval - size of lowest allowed interval, in semitones
  high_interval - size of highest allowed interval, in semitones
  starting_note - can set range within which to generate starting note. Default is A2 -> B4.
  
