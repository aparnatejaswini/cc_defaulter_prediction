from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, FileResponse
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.pipeline.prediction_pipeline import Predict_pipeline
from src.pipeline.training_pipeline import Train_Pipeline
from src.logger import logger
import os, shutil


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get('/')
def index():
    return RedirectResponse('/docs')
'''
@app.get('/train')
def train_route():
    try:
        train_pipeline = Train_Pipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training Successful.")
    except Exception as e:
        return Response(f"Error Occured. {e}")
'''
@app.post("/upload_file")
def upload_file(file:UploadFile = File()):
    try:
        predict_pipeline = Predict_pipeline()
        file_path = os.path.join(os.getcwd(), 'data', f'{file.filename}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as buffer:          
            shutil.copyfileobj(file.file, buffer)
        response = predict_pipeline.predict_pipeline(file_path, UPLOAD_DIR)
        if os.path.exists(response):
            return FileResponse(path = response, media_type='application/octet-stream', filename=os.path.basename(response))
        else: 
            return Response(response)
        
    except Exception as e:
        return Response(f"Error Occured. {e}")




'''    
def main():
    try:
        training_pipeline = Train_Pipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        logger.exception(e)
'''
if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)
