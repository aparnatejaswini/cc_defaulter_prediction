from src.config.configuration import ConfigurationManager
from src.components.data_validation_predict import DataValidationPredict
from src.utils.common import load_object
from src.logger import logger
import pandas as pd
import os

class Predict_pipeline():
    def __init__(self) -> None:
        pass


    def predict_pipeline(self,user_file_path, UPLOAD_DIR):

        config = ConfigurationManager()
        dv_config = config.get_data_validation_config()
        dt_config = config.get_data_transformation_config()
        data_validation = DataValidationPredict(dv_config=dv_config,dt_config=dt_config)
        data_validation.initiate_data_validation(user_file_path)
        with open(dv_config.validation_status, 'r') as dv:
            validation_status=dv.readlines()[0]
            logger.info(f"prediciton_pipeline module: {validation_status}")
        logger.info(f'before if: {validation_status}')
        
        if validation_status == 'True':
            logger.info("inside if block")
            user_df = pd.read_csv(user_file_path)
            md_config = config.get_model_deployment_config()
            preprocessor = load_object(dt_config.preprocess_obj)
            column_names = preprocessor[1:].named_steps['preprocessor'].get_feature_names_out()
            df = pd.DataFrame(preprocessor.transform(user_df).toarray(), columns=column_names)
            with open(dt_config.selected_features, 'r') as dt:
                selected_columns = dt.readlines()[0].split(',')
            #print(selected_columns)
            model = load_object(md_config.selected_model)
            result_df = df[selected_columns]
            y_pred = model.predict(result_df)
            #print(y_pred)
            user_df['y'] = y_pred
            user_df.drop(columns=['avg_bill_amt', 'avg_leverage_ratio', 'avg_pay_amt', 'avg_bill_to_pay'], inplace=True)
            predict_file_path ="{}_predicted.csv".format(os.path.basename(user_file_path).split('.')[0])
            logger.info(predict_file_path)
            predicted_file_path = os.path.join(UPLOAD_DIR, predict_file_path)
            logger.info(predicted_file_path)

            #print(user_df.head())
            user_df.to_csv(predicted_file_path, index=False)
            return predicted_file_path

        else:
            logger.info('Data did not meet validation checks.')
            return "Data did not meet validation checks."

        



