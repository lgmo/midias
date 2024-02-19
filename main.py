from fastapi import FastAPI
import uvicorn
from models.audio import Audio
from models.video import Video
from routes.video_routes import video_router

VIDEOS_DICT = {}

app = FastAPI(version='0.1.0')
video_model = Video()
audio_model = Audio()

app.include_router(
    router=video_router(video_model, audio_model),
    prefix='/videos'
)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=3030)