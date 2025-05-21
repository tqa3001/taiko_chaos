import os
import librosa
from enum import Enum

from typing import List  # py3.8 tspmo

class GenerationMode(Enum):
    Unimplemented = 0

def get_note_onsets(track_path: str, mode: GenerationMode) -> List[float]:
    
    track_name = os.path.splitext(os.path.basename(track_path))[0]
    output_folder = os.path.join('output', track_name)

    if not os.path.isdir(output_folder):
        print('todo')
    else:
        print('track is already separated, skipping spleeter step')

    instrument = 'drums'
    input_wav = os.path.join(output_folder, instrument + '.wav')

    y, sr = librosa.load(input_wav)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    return onset_times