from fastapi import FastAPI
import uvicorn
from models.video import Video
from routes.video_routes import video_router

VIDEOS_DICT = {}

app = FastAPI(version='0.1.0')
video_model = Video()

app.include_router(
    router=video_router(video_model),
    prefix='/videos'
)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=3030)
