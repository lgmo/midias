from uuid import uuid4
from fastapi import UploadFile


class Video:
    def __init__(self):
        self.videos_directory_path = 'videos/'

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
