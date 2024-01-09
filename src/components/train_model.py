import pandas as pd
from pathlib import Path
from src.logger import logger
from src.utils.common import save_object, save_json
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from src.entity.config_entity import ModelTrainerConfig, DataTransformationConfig
import os



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
        
        #list of classification models
        models = {
            "LogisticRegression": LogisticRegression(),#(class_weight='balanced'),
            "SVM": SVC(),#(class_weight='balanced'),
            "DecisionTree": DecisionTreeClassifier(),#(class_weight='balanced'),
            "RandomForest": RandomForestClassifier(),#(class_weight='balanced'),
            "ExtraTree": ExtraTreesClassifier()#(class_weight='balanced'),
        }

        hyper_params={}
        for model_name in models:
            model = models[model_name]
            logger.info(params)
            param = params[model_name]
            skf = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)
            gs = GridSearchCV(model,param,cv=skf, verbose=1)
            gs.fit(train_x,train_y.values.ravel())
            hyper_params[model_name]= gs.best_params_
            model.set_params(**gs.best_params_)
            logger.info(f'{model_name} model parameters: {model.set_params(**gs.best_params_)}, {model.get_params()}')
            model.fit(train_x,train_y.values.ravel())
            
            #model.fit(X_train, y_train)  # Train model

            #y_test_pred = model.predict(test_y)

            #test_model_score = f1_score(y_test, y_test_pred)

            model_path = os.path.join(self.mt_config.root_dir,model_name+".pkl")
            save_object(model_path,model)  
        save_json(Path(self.mt_config.model_params), hyper_params) 

       