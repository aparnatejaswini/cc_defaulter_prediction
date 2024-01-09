#import os
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from urllib.parse import urlparse
import mlflow, dagshub
import mlflow.sklearn
#import numpy as np
from src.utils.common import load_json, load_object
from src.logger import logger
from src.entity.config_entity import ModelEvaluationConfig, ModelTrainerConfig
from pathlib import Path
import os


class ModelEvaluation:
    def __init__(self, me_config: ModelEvaluationConfig, mt_config:ModelTrainerConfig):
        self.me_config = me_config
        self.mt_config = mt_config

    
    def eval_metrics(self,actual, pred):
        f1score = f1_score(actual, pred)
        precisionscore = precision_score(actual, pred)
        recallscore = recall_score(actual, pred)
        rocaucscore = roc_auc_score(actual, pred)
        return f1score, precisionscore, recallscore, rocaucscore
    


    def log_into_mlflow(self):

        dagshub.init(repo_owner='aparnatejaswini', repo_name='cc_defaulter_prediction', mlflow=True)
        test_data = pd.read_csv(self.me_config.test_data_path)
        model_dir = self.mt_config.root_dir
        logger.info(model_dir)
        hyper_params = load_json(Path(self.mt_config.model_params))

        test_x = test_data.drop([self.me_config.target_column], axis=1)
        test_y = test_data[[self.me_config.target_column]]


        mlflow.set_registry_uri(self.me_config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme


        model_list, f1_list, prec_list, rec_list, rocauc_list = [], [], [], [], []
        #train_f1_list, train_prec_list, train_rec_list, train_rocauc_list = [], [], [], []
        for file in os.listdir(model_dir): 
            if file.endswith('.pkl'):
                print("File name is: ", file)    
                model_name = file.split('.')[0]
                model = load_object(os.path.join(model_dir,file))
                  #logger.info(model_name, type(model))
                predicted_values = model.predict(test_x)
                with mlflow.start_run():

                    f1, prec, rec, rocauc = self.eval_metrics(test_y, predicted_values)
                    model_list.append(model_name)
                    f1_list.append(f1)
                    prec_list.append(prec)
                    rec_list.append(rec)
                    rocauc_list.append(rocauc)
                    scores = {"Model_name" :model_list, "F1-score": f1_list, "Precision": prec_list, "Recall": rec_list, "roc-auc-score": rocauc_list}
                    logger.info(scores)
                    logger.info(hyper_params[model_name])
                    #mlflow.autolog()
                    #mlflow.log_model(model)
                    mlflow.log_params(hyper_params[model_name])
                    mlflow.log_metric("F1-score", f1)
                    mlflow.log_metric("Precision", prec)
                    mlflow.log_metric("Recall", rec)
                    mlflow.log_metric("roc-auc-score", rocauc)
                        #mlflow.autolog()
                        # Model registry does not work with file store
                    if tracking_url_type_store != "file":

                            # Register the model
                            # There are other ways to use the Model Registry, which depends on the use case,
                            # please refer to the doc for more information:
                            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                            mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)
                    else:
                        mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)

        pd.DataFrame().from_dict(scores).to_json(self.me_config.metric_file_name, index='Model_name')
