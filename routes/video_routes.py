from uuid import UUID
from fastapi import APIRouter, File, UploadFile
from starlette import status

from models.video import Video

def video_router(video_model: Video):
    router = APIRouter(tags=['Video'])

    @router.post('/', status_code=status.HTTP_200_OK, response_model=str)
    async def upload(file: UploadFile = File(...)):
        return str(await video_model.create(file))

    @router.get('/{file_id}/detect-silence', status_code=status.HTTP_200_OK, response_model=list[float])
    async def detect_silence(
        file_id: str
    ):
        file_id = UUID(file_id) 
        await video_model.get_silence_time_stamps(file_id)
        return [0.0, 1.0, 2.0, 3.0, 4.0, 5.0] 

    return router