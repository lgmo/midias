import os
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import subprocess
from uuid import uuid4

class Audio:
    def __init__(self):
        self.videos_directory_path = 'videos/'

    def file_path(self, file_id: uuid4):
        return self.videos_directory_path + f'{file_id}.mp4'

    async def detect_silence(self, file_id: str) -> uuid4:
        if not os.path.isfile(f'audios/{file_id}.wav'):
            command = f'ffmpeg -i videos/{file_id}.mp4 -ab 160k -ac 2 -ar 44100 -vn audios/{file_id}.wav'
            subprocess.call(command, shell=True)
        audio_path = f'audios/{file_id}.wav'
        [Fs, x] = aIO.read_audio_file(audio_path)
        segments = aS.silence_removal(x, 
                                    Fs, 
                                    0.020, 
                                    0.020, 
        )
        return segments