import os
import librosa
import subprocess
from enum import Enum

from typing import List  # py3.8 tspmo

class GenerationMode(Enum):
    Unimplemented = 0

def get_note_onsets(trackFile: str, mode: GenerationMode) -> List[float]:
    
    track_name = os.path.splitext(os.path.basename(trackFile))[0]
    output_folder = os.path.join('output', track_name)

    if not os.path.isdir(output_folder):
        print(f"Seperating parts for ${trackFile} ...")
        subprocess.run(["powershell", 
                        "-ExecutionPolicy", "Bypass", 
                        "-File", "spleeter_separater_helper.ps1",
                        trackFile])
        print("Seperation finished!")
    else:
        print(f"Track ${trackFile} is already separated, skipping spleeter step")

    instrument = 'drums'
    input_wav = os.path.join(output_folder, instrument + '.wav')

    y, sr = librosa.load(input_wav)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    return onset_times