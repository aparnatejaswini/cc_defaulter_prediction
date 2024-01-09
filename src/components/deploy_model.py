import pandas as pd
from src.logger import logger
from src.utils.common import save_object, load_json, load_object
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from src.entity.config_entity import ModelDeploymentConfig, DataTransformationConfig
import os


class ModelDeployment:
    def __init__(self, md_config: ModelDeploymentConfig, dt_config:DataTransformationConfig):
        self.md_config = md_config
        self.dt_config = dt_config
    
    def train(self):
        train_data = pd.read_csv(self.dt_config.transformed_train_file)
        test_data = pd.read_csv(self.dt_config.transformed_test_file)
        logger.info(train_data.head())
        complete_data = pd.concat([train_data, test_data], ignore_index=True)
        logger.info(complete_data.head())
        x_data = complete_data.drop(columns=self.md_config.target_column)
        y_data = complete_data[[self.md_config.target_column]]
        metrics = pd.read_json(self.md_config.metrics_file)
        model_name = metrics.sort_values(by='F1-score', ascending=False).reset_index()['Model_name'][0]
        model = load_object(os.path.join(self.md_config.model_dir, (model_name+'.pkl')))
        model.fit(x_data, y_data.values.ravel())
        #y_pred = model.predict(x_data)
        #f1score = f1_score(y_data, y_pred)
        #lr = LogisticRegression(solver=params.solver, C=params.C, class_weight=params.class_weight, max_iter=params.max_iter, penalty=params.penalty, random_state=30)
        #lr.fit(x_train, y_train.values.ravel())
        
        #y_train_pred = lr.predict(x_train)
        #f1score = f1_score(y_train, y_train_pred)
        #logger.info(f"f1 score for the logistic regression model trained on complete data(including train and test) is : {f1score}")
        save_object(self.md_config.selected_model, model)
