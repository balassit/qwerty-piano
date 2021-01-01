from mingus.containers import Note
from mingus.midi import fluidsynth

def get_note(octave, note):
    if note is None or not len(note):
        return
    # c = NoteContainer(note, octave)
    # print(c)
    return Note(note, octave)

def stop(note):
    fluidsynth.stop_Note(note)

def play(note):
    fluidsynth.play_Note(note)
    print(note)
    print("-" * 20)
