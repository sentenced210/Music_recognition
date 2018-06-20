from Recognition import *

file = open('Amir testing output.txt', 'w')
for index in range(1, 100):
    file_name = "Input/mono" + str(index) + ".wav"
    bpm = bpm_detection(file_name)
    key, scale = key_and_scale_detection(file_name)
    file.write(file_name + " Real bpm: " + str(bpm) + "; Round bpm: " + str(int(round(bpm)))+"; Key: "+str(key)+" "+str(scale) + '\n')
file.close()
