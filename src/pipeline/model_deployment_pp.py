from src.config.configuration import ConfigurationManager
from src.components.deploy_model import ModelDeployment
from src.logger import logger



STAGE_NAME = "Model Deployment stage"

class ModelDeploymentTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_deployment_config = config.get_model_deployment_config()
        data_transformation_config = config.get_data_transformation_config()
        model_trainer_config = ModelDeployment(md_config=model_deployment_config, dt_config=data_transformation_config)
        model_trainer_config.train()
