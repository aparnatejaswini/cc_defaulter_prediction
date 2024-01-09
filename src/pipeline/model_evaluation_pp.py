from src.config.configuration import ConfigurationManager
from src.components.evluate_model import ModelEvaluation
from src.logger import logger

STAGE_NAME = "Model evaluation stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_trainer_config = config.get_model_trainer_config()
        model_evaluation_config = ModelEvaluation(me_config=model_evaluation_config, mt_config=model_trainer_config)
        model_evaluation_config.log_into_mlflow()