import librosa
import matplotlib.pyplot as plt
import argparse
from spleeter.separator import Separator

parser = argparse.ArgumentParser(prog='TaikoChaos')
parser.add_argument('--input', help='input (.mp3) for generating chart')

args = parser.parse_args()
input_file = args.input

print(input_file)

separator = Separator('spleeter:4stems')  # vocals, drums, bass, other
separator.separate_to_file(input_file, "tmp")



y, sr = librosa.load(input_file)

# Detect onset frames
# onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
# onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# # Print event times
# print("Onsets (s):", onset_times)
# 3. Visualize Detected Events (Optional)
# python
# Copy
# Edit
# librosa.display.waveshow(y, sr=sr)
# plt.vlines(onset_times, -1, 1, color='r', linestyle='--')
# plt.title("Onset Detection on Bass Track")
# plt.show()