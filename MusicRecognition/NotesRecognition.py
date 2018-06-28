import struct
import wave
import scipy.io.wavfile as wav
import numpy as np
from matplotlib.pyplot import plot
from scipy.fftpack import fft


def get_note(pitch):
    notes = []
    for i in range(128):
        notes.append(float(i))
    notes[68] = 440.0

    for i in range(69, 128):
        notes[i] = notes[i - 1] * pow(2, 1 / 12)

    i = 67
    while i >= 0:
        notes[i] = notes[i + 1] / pow(2, 1 / 12)
        i = i - 1

    for i in range(128):
        print(str(i) + ": " + str(notes[i]))

    note = 0
    min_distance = 999999.0

    for j in range(0, len(notes)):
        if min_distance > abs(pitch - notes[j]):
            min_distance = abs(pitch - notes[j])
            note = j

    return note


def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short
    a = struct.unpack("%ih" % (w.getnframes() * w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    w.close()
    return a


def compression_data(file_name):
    signal = wav_to_floats(file_name)

    threshold = 0.2
    ratio = 2.0
    gain = 2.0
    maximum = 0

    for i in range(len(signal)):
        # positive values
        if signal[i] > threshold:
            signal[i] = threshold + (signal[i] - threshold) * (1.0 / ratio)
        # negative values
        if signal[i] < -threshold:
            signal[i] = -threshold + (signal[i] + threshold) * (1.0 / ratio)
        # apply the gain to all samples
        signal[i] *= gain
        if abs(signal[i]) > maximum:
            maximum = abs(signal[i])

    return signal


def create_new_commpression_wav_file(filename):
    signal = compression_data(filename)
    a = np.array(signal)
    wav.write("new_wav.wav", 44100, a)
    return signal

def transformation(data):
    # с этим надо еще поиграться
    signal = np.array(data, dtype=float)
    spectrum = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(spectrum))
    threshold = 0.5 * max(abs(spectrum))
    mask = abs(spectrum) > threshold
    peaks = freq[mask]
    # print(max(peaks)*44100)
    return max(peaks)*44100


def frequencies_detection(data, bar_amount):
    N = int(len(data)/bar_amount/64)
    smallest_duration = 64  #
    frequencies = []
    loudness = []
    for current_bar in range(bar_amount):
        for current_smallest_duration in range(smallest_duration):
            data_for_transformation = []
            for data_index in range((current_bar*smallest_duration+current_smallest_duration)*N,
                                    (current_bar * smallest_duration + current_smallest_duration) * N+N):
                data_for_transformation.append(data[data_index])
            frequencies.append(transformation(data_for_transformation))
            loudness.append(rms(data_for_transformation)*13.2)
    return frequencies, loudness


def rms(data):
    ms = 0
    for i in range(len(data)):
        ms += data[i]*data[i]
    ms /= len(data)
    return pow(ms, 0.5)
