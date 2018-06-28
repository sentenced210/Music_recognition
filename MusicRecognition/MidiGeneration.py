from mido import Message, MidiFile, MidiTrack, MetaMessage
from mido import bpm2tempo


def generate_midi_file(bpm, numerator, denominator, notes, notes_on, notes_off, bar_amount):
    midi_file = MidiFile()
    midi_track = MidiTrack()
    tempo_msg = MetaMessage('set_tempo', tempo=bpm2tempo(bpm))
    time_signature_msg = MetaMessage('time_signature', numerator=numerator, denominator=denominator)
    key_signature_msg = MetaMessage('key_signature', key='C')  # should be change

    midi_track.append(tempo_msg)
    midi_track.append(time_signature_msg)
    midi_track.append(key_signature_msg)
    for i in range(len(notes)):
        msg_on_note = Message('note_on', note=notes[i], time=0)
        msg_off_note = Message('note_off', note=notes[i], time=16)
        print(str(notes_on[i])+" "+str(notes_off[i]))
        midi_track.append(msg_on_note)
        midi_track.append(msg_off_note)

    midi_file.ticks_per_beat = 16
    print(midi_file.ticks_per_beat)
    midi_file.tracks.append(midi_track)
    midi_file.save('test_output.mid')
