import pandas as pd
import os
from src.logger import logger
from src.utils.common import save_object
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score,precision_score,recall_score
from src.entity.config_entity import ModelTrainerConfig, DataTransformationConfig



class ModelTrainer:
    def __init__(self, dt_config: DataTransformationConfig, mt_config: ModelTrainerConfig):
        self.dt_config = dt_config
        self.mt_config = mt_config
    
    def train(self):
        train_data = pd.read_csv(self.dt_config.transformed_train_file)
        test_data = pd.read_csv(self.dt_config.transformed_test_file)


        train_x = train_data.drop(columns= self.mt_config.target_column)
        test_x = test_data.drop(columns=self.mt_config.target_column)
        train_y = train_data[[self.mt_config.target_column]]
        test_y = test_data[[self.mt_config.target_column]]
        params = self.mt_config.params

        lr = LogisticRegression(C=params.C, class_weight=params.class_weight, max_iter=params.max_iter, penalty=params.penalty)
        lr.fit(train_x, train_y.values.ravel())
        '''
        train_y_pred = lr.predict(train_x)
        train_f1_score = f1_score(train_y, train_y_pred)
        #if train_f1_score<0.65:
        #    logger.error(f"Current models train data f1 score is {train_f1_score} < 0.65. Model is not a good try for further experiments.")
        test_y_pred = lr.predict(test_x)
        test_f1_score = f1_score(test_y, test_y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        '''
        save_object(self.mt_config.model_name, lr)
        #joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))

