from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    downloaded_data_file: Path
    train_test_split_ratio: int
    train_file: Path
    test_file: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir:Path
    valid_data_dir: Path
    invalid_data_dir: Path
    data_drift_report_dir: Path
    valid_train_file_path: Path
    valid_test_file_path: Path
    invalid_train_file_path: Path
    invalid_test_file_path: Path
    drift_report_file_path: Path # since data_drift_dataset_report.save_json(str) method exprects a string
    drift_report_page_path: Path
    validation_status: Path
    all_schema: dict

    


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    validated_raw_data: Path
    transformed_train_file: Path
    transformed_test_file: Path
    selected_features: list
    preprocess_obj: Path
    all_schema:dict

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    model_params: Path
    params: dict
    target_column: str
    

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    #model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str


@dataclass(frozen=True)
class ModelDeploymentConfig:
    root_dir: Path
    #train_data_path: Path
    #test_data_path: Path
    selected_model: Path
    metrics_file: Path 
    model_dir: Path
    target_column: str