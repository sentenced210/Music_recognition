import NotesRecognition
import Recognition
import MidiGeneration


def file_generation():
    file_name = 'output.wav'

    output_test_file = open("output_test_file.txt", 'w')

    bpm = Recognition.bpm_detection(file_name)
    duration = Recognition.duration_detection(file_name)
    bar_amount = Recognition.bar_numbers(4, duration, bpm)

    output_test_file.write("BPM: " + str(bpm) + "\n")
    output_test_file.write("Duration: " + str(duration) + "\n")
    output_test_file.write("BarAmount for time signature 4/4: " + str(bar_amount) + "\n\n")

    output_test_file.write("----------------------------\n\n")

    data = NotesRecognition.wav_to_floats(file_name)
    frequencies, loudness = NotesRecognition.frequencies_detection(data, bar_amount)

    for i in range(len(frequencies)):
        output_test_file.write(str(i) + ") Frequency: " + str(frequencies[i]) + " RMS: " + str(loudness[i]) + "\n")

    output_test_file.close()


def test():
    bpm = 120
    time_signature_numerator = 4
    time_signature_denominator = 4
    bar_amount = 3
    notes = [60, 64, 67, 72, 60, 64, 67, 72]
    note_on = [0, 16, 32, 48, 64, 80, 96, 112]
    note_off = [15, 31, 47, 63, 79, 95, 111, 127]

    MidiGeneration.generate_midi_file(bpm, time_signature_numerator, time_signature_denominator, notes, note_on,
                                      note_off, bar_amount)


if __name__ == "__main__":
    test()
