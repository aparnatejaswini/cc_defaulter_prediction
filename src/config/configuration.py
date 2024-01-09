from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig, \
                                     DataValidationConfig, \
                                            DataTransformationConfig, \
                                            ModelTrainerConfig, \
                                            ModelEvaluationConfig, \
                                            ModelDeploymentConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            downloaded_data_file=config.downloaded_data_file,
            train_test_split_ratio=config.train_test_split_ratio,
            train_file=config.train_file,
            test_file=config.test_file
        )

        return data_ingestion_config
    

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema

        create_directories([config.root_dir, config.valid_data_dir, config.invalid_data_dir, config.data_drift_report_dir])

        data_validation_config=DataValidationConfig(
            root_dir=config.root_dir,
            valid_data_dir=config.valid_data_dir,
            invalid_data_dir=config.invalid_data_dir,
            data_drift_report_dir=config.data_drift_report_dir,
            valid_train_file_path=config.valid_train_file_path,
            valid_test_file_path=config.valid_test_file_path,
            invalid_train_file_path=config.invalid_train_file_path,
            invalid_test_file_path=config.invalid_test_file_path,
            drift_report_file_path=config.drift_report_file_path,
            drift_report_page_path=config.drift_report_page_path,
            validation_status=config.validation_status,
            all_schema=schema
        )

        return data_validation_config
    


    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        schema = self.schema
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            validated_raw_data=config.validated_raw_data,
            transformed_train_file= config.transformed_train_file,
            transformed_test_file= config.transformed_test_file,
            selected_features=config.selected_features,
            preprocess_obj=config.preprocess_obj,
            all_schema=schema
        )

        return data_transformation_config
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params
        target_column = self.schema.target_column

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            model_params = config.model_params,
            params = params,
            target_column = target_column
        )

        return model_trainer_config
    

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params
        target_column = self.schema.target_column

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            #model_path = config.model_path,
            all_params=params,
            metric_file_name = config.metric_file_name,
            target_column = target_column,
            mlflow_uri="https://dagshub.com/aparnatejaswini/cc_defaulter_prediction.mlflow"
,
           
        )

        return model_evaluation_config
    

    def get_model_deployment_config(self) -> ModelDeploymentConfig:
        config = self.config.model_deployment
        target_column = self.schema.target_column

        create_directories([config.root_dir])

        model_trainer_config = ModelDeploymentConfig(
            root_dir=config.root_dir,
            #train_data_path= config.train_data_path,
            #test_data_path=config.test_data_path,
            target_column = target_column, 
            selected_model = config.selected_model,
            metrics_file = config.metrics_file,
            model_dir = config.model_dir
        )

        return model_trainer_config