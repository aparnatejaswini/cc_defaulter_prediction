from src.logger import logger
from src.pipeline.data_ingestion_pp import DataIngestionTrainingPipeline
from src.pipeline.data_validation_pp import DataValidationTrainingPipeline
from src.pipeline.data_transformation_pp import DataTransformationPipeline
from src.pipeline.model_trainer_pp import ModelTrainerTrainingPipeline
from src.pipeline.model_evaluation_pp import ModelEvaluationTrainingPipeline
from src.pipeline.model_deployment_pp import ModelDeploymentTrainingPipeline

class Train_Pipeline():
    is_pipeline_running=False
    def __init__(self) -> None:
         pass
    
    def run_pipeline(self):
        Train_Pipeline.is_pipeline_running=True
        '''
        STAGE_NAME = "Data Ingestion stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            data_ingestion = DataIngestionTrainingPipeline()
            data_ingestion.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e

        STAGE_NAME = "Data Validation stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            data_validation = DataValidationTrainingPipeline()
            data_validation.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e

        STAGE_NAME = "Data Transformation stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            data_transformation = DataTransformationPipeline()
            data_transformation.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e

        
        STAGE_NAME = "Model Trainer stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            train_model = ModelTrainerTrainingPipeline()
            train_model.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e
        

        STAGE_NAME = "Model evaluation stage"
        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
            evaluate_model = ModelEvaluationTrainingPipeline()
            evaluate_model.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e


        '''
        STAGE_NAME = "Model deployment stage"

        try:
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
            model_deployment = ModelDeploymentTrainingPipeline()
            model_deployment.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        except Exception as e:
                logger.exception(e)
                raise e
        