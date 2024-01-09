from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(di_config = data_ingestion_config, dv_config=data_validation_config)
        data_validation.initiate_data_validation()







