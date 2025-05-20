import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
import argparse
import sounddevice as sd
import time
from spleeter.separator import Separator

def play_beat(frequency=1000, duration=0.05, sample_rate=44100):
    """Play a short beep-like sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate a sine wave (tone) or white noise (for a snare-like sound)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # sine wave for a click
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

for i in range(10):
    play_beat()
    time.sleep(0.5)

exit(0)

parser = argparse.ArgumentParser(prog='TaikoChaos')
parser.add_argument('--track', help='.mp3 track file to generate chart')

args = parser.parse_args()
track_file = args.track
track_name = os.path.splitext(os.path.basename(track_file))[0]
output_folder = os.path.join('output', track_name)

if not os.path.isdir(output_folder):
    separator = Separator('spleeter:4stems')  # vocals, drums, bass, other
    separator.separate_to_file(track_file, "output")

mode = 'vocals'
input_wav = os.path.join(output_folder, mode + '.wav')

y, sr = librosa.load(input_wav)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

print(onset_times)

librosa.display.waveshow(y, sr=sr)
plt.vlines(onset_times, -1, 1, color='r', linestyle='--')
plt.show()