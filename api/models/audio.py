import os
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import subprocess
from uuid import uuid4

class Audio:
    def __init__(self):
        self.videos_directory_path = 'videos/'

    def _get_audio_duration(self, file_path):
        # Comando FFmpeg para obter a duração do vídeo
        command = ['ffmpeg', '-i', file_path, '-f', 'null', '-']
        
        # Executando o comando e capturando a saída
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Verificando se o comando foi executado com sucesso
        if result.returncode == 0:
            # Procurando pela linha que contém a duração do vídeo
            for line in result.stderr.split('\n'):
                if 'Duration' in line:
                    duration_str = line.split(',')[0].split('Duration: ')[1]
                    # Convertendo a duração para segundos
                    duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(duration_str.split(":"))))
                    return duration
        else:
            print("Erro ao obter a duração do vídeo:")
            print(result.stderr)

    def _convert_to_silence_segments(self, segments, file_id):
        if not segments:
            return []
        duration = self._get_audio_duration(self.file_path(file_id))
        start = 0
        silence_segments = []
        for interval in segments:
            if interval[0] > start:
                silence_segments.append((start, interval[0]))
                start = interval[1]

        if segments and segments[-1][1] == start:
            silence_segments.append((start, duration))
        return silence_segments

    def file_path(self, file_id: uuid4):
        return self.videos_directory_path + f'{file_id}.mp4'

    async def detect_silence(self, file_id: str) -> uuid4:
        if not os.path.isfile(f'audios/{file_id}.wav'):
            command = f'ffmpeg -i videos/{file_id}.mp4 -ab 160k -ac 2 -ar 44100 -vn audios/{file_id}.wav'
            subprocess.call(command, shell=True)
        audio_path = f'audios/{file_id}.wav'
        [Fs, x] = aIO.read_audio_file(audio_path)
        sound_segments = aS.silence_removal(x, 
                                    Fs, 
                                    0.020, 
                                    0.020, 
        )
        return sound_segments