import wave
from Recognition import *

# audio_file = "MusicFiles/Sample Record 22.wav"
# audio_file = "MusicFiles/34.mp3"
audio_file = "MusicFiles/Mono 100.wav"
bpm_detection(audio_file)
time_signature_detection(audio_file)
duration_detection(audio_file)
key_and_scale_detection(audio_file)
print()
audio_file = "MusicFiles/Mono 120.wav"
bpm_detection(audio_file)
time_signature_detection(audio_file)
duration_detection(audio_file)
key_and_scale_detection(audio_file)
print()
audio_file = "MusicFiles/Sample Record 22.wav"
bpm_detection(audio_file)
time_signature_detection(audio_file)
duration_detection(audio_file)
key_and_scale_detection(audio_file)
