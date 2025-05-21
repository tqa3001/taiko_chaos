import os
import time
import numpy as np
import librosa
import matplotlib.pyplot as plt
import argparse
import sounddevice as sd
import soundfile as sf
import pygame

def play_wav(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)

def play_drum():
    play_wav('.\\mixed_drum.wav')

pygame.mixer.init()
drum = pygame.mixer.Sound('.\\mixed_drum.wav')

# for i in range(100):
#     drum.play()
#     time.sleep(0.2)
# exit(0)

parser = argparse.ArgumentParser(prog='TaikoChaos')
parser.add_argument('--track', help='.mp3 track file to generate chart')

args = parser.parse_args()
track_file = args.track
track_name = os.path.splitext(os.path.basename(track_file))[0]
output_folder = os.path.join('output', track_name)

if not os.path.isdir(output_folder):
    print('todo')
else:
    print('track is already separated, skipping spleeter step')

mode = 'drums'
input_wav = os.path.join(output_folder, mode + '.wav')

y, sr = librosa.load(input_wav)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

for i in range(3, 0, -1):
    print("starting in", i)
    time.sleep(1)

print("play!")
play_wav(os.path.join(output_folder, 'piano.wav'))

last = 0
count = 1
for t in onset_times:
    time.sleep(t - last)
    print(count, end='\r')
    drum.play()
    last = t
    count = count + 1