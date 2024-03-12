import os
import subprocess
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from starlette.responses import FileResponse


class Video:
    def __init__(self):
        self.videos_directory_path = 'videos/'

    def cut_and_join_video(self, input_video, output_video, silence_segments):
        commands = []
        # Cortar os intervalos especificados
        def file_name(i):
            return self.file_path(f'{output_video}_segment_{i}')

        for i, interval in enumerate(silence_segments, start=1):
            start_time = interval[0]
            end_time = interval[1]
            output_segment = file_name(i) 
            # Comando FFmpeg para cortar o vídeo
            command = ['ffmpeg', '-i', input_video, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', output_segment]
            commands.append(command)
        
        # Juntar os segmentos restantes
        join_command = ['ffmpeg']
        for segment in [file_name(i) for i in range(1, len(silence_segments) + 1)]:
            join_command.extend(['-i', segment])
        join_command.extend(['-filter_complex', f'concat=n={len(silence_segments)}:v=1:a=1', self.file_path(output_video)])
        # Executar os comandos FFmpeg
        for command in commands:
            subprocess.run(command, check=True)

        subprocess.run(join_command, check=True)

    def file_path(self, file_id: uuid4):
        return self.videos_directory_path + f'{file_id}.mp4'

    async def create(self, file: UploadFile) -> uuid4:
        file_ext = file.filename.split('.')[-1]
        if file_ext != 'mp4':
            raise ValueError('Invalid file extension')
        file_id = uuid4()
        with open(self.file_path(file_id), 'wb') as buffer:
            content = await file.read()
            buffer.write(content)
        return file_id 

    async def jump_cut(self, file_id: uuid4, silence_segments: list[list[float]]) -> FileResponse:
        input_file_path = self.file_path(file_id)
        if not os.path.exists(input_file_path):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        filename = f'{file_id}_jump_cut'
        self.cut_and_join_video(input_file_path, filename, silence_segments)
        output_file_path = self.file_path(filename)
        return FileResponse(output_file_path, media_type='application/octet-stream', filename=filename + '.mp4')
