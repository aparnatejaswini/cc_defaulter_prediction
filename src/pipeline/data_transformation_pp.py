from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src.logger import logger


STAGE_NAME = "Data Transformation stage"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_transformation_config = config.get_data_transformation_config()
            with open(data_validation_config.validation_status, 'r') as f:
                validation_status = f.readline()
                logger.info(type(validation_status))

            if bool(validation_status)==True:
                data_transformation = DataTransformation(dt_config=data_transformation_config, dv_config=data_validation_config)
                data_transformation.initiate_data_transformation()
            else:
                raise Exception(f"You data schema is not valid. You can find data at {data_validation_config.invalid_data_dir}")

        except Exception as e:
            logger.exception(e)







