from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
#from src.components.data_validation import DataValidationPredict
from src.constants import EnvironmentVariable
from src.logger import logger


# "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)#, env_var=EnvironmentVariable())
            data_ingestion.download_file()
            df=data_ingestion.export_file_as_df()
            #df = data_ingestion.export_table_as_df()
            data_ingestion.split_data_as_train_test(dataframe=df)
        except Exception as e:
            logger.exception(e)

'''
# "Data Validation stage"
class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidationPredict(config=data_validation_config)
            data_validation.initiate_data_validation()
        except Exception as e:
            logger.exception(e)
'''