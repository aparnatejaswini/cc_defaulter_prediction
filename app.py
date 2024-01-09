#from src.pipeline.training_pipeline import Train_Pipeline
#Train_Pipeline().run_pipeline()


from src.pipeline.prediction_pipeline import Predict_pipeline
from src.logger import logger
import os
predict_pipeline = Predict_pipeline()
file_path = r"C:\Users\User\Desktop\creditCardDefaulters\code\creditCardDefaulters\Prediction_Batch_files\creditCardFraud_28011961_12.csv"
response = predict_pipeline.predict_pipeline(file_path, 'uploads')
print(response)
