from src.logger import logger
from src.utils.common import read_yaml
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric, DataDriftTable
from pathlib import Path

import json
import pandas as pd
import sys
import os
import shutil
import re

class DataValidationPredict():
    """
    This class shall be used to perform all the validation checks done on training data.
    It takes input from DataIngestionArtifact, DataValidationConfig , TrainingPipelineConfig

    - checks if source file path exists
    - validates file name
    - validates Number of columns
    - validates column names
    - validates domain values of categorical variables
    - Checks for data drift
    
    upon successful completion of all above validation checks, model predictions are generated for the given file.
    -generates data drift report file
    -generates data drift report page

    written by: Aparna T Parkala
    Version:1.0
    """
    def __init__(self,di_config:DataIngestionConfig, dv_config: DataValidationConfig):
        self.di_config = di_config
        self.dv_config = dv_config



    def check_if_file_exists(self, file_path:Path)->bool:
        """
        This method checks for presence of train and test files.
        Args: file_path : Path variable
        Returns a boolean value
        """
        try:
            logger.info(f"Checking  if path {file_path} exists....")
            file_exists = False
            file_exists = os.path.exists(file_path)
            if file_exists:
                msg = f"File at [{file_path}] is available."
                logger.info(msg)
            else:
                msg = f"File at [{file_path}] is not available."
                logger.info(msg)                
            return file_exists
        except Exception as e:
            logger.exception(e)
    '''
    def validate_file_name(self, file_path) ->bool:
        """
        returns a boolean value.
        True indicates file name validated successfully.
        False indicates file name validation unsuccessful.
        """
        try:
            file_name_validated = False
            pattern = re.compile(r"^CreditCard[A-Za-z]{5}\_\d{8}\_\d{6}\.csv")
            if pattern.match(os.path.basename(file_path)):
                logger.info("File Name Validated Successfully.")
                file_name_validated = True
            else:
                logger.info("File Name format is not validated. Moving file to invalid data Folder")
            return file_name_validated
        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    '''

    def validate_dataset_schema(self,file_path)->bool:
        """
        This method checks if given file has similar schema as given to us by data owner.
        - checks for file_name pattern
        - checks Number of columns
        - checks column names
        - checks domain values of columns
        Args: file_path : Path variable
        Returns a boolean value
        """
        try:
            validation_status=False

            logger.info("Reading Values from schema....")
            ##reading data schema file
            schema_config = self.dv_config.all_schema

            #Validate fie name
            #file_name_validated = self.validate_file_name(file_path=file_path)

            #Validate No.of Columns
            num_cols_validated = False
            df = pd.read_csv(file_path)
            if df.shape[1] == schema_config['NoOfColumns']:
                num_cols_validated=True
                logger.info("Number of columns validated.")
            else:
                logger.info(f"Number of columns in file does not match with schema, moving file to invalid data folder\n\
                                    columns in schema {schema_config['NoOfColumns']}\n\
                                    columns in file {df.shape[1]}")

            #Validate column names
            column_names = set(schema_config['ColumnNames'].keys())#-set(schema_config['target_column'])
            col_names_validated = False
            if set(df.columns) == column_names:
                col_names_validated = True
                logger.info("Column names validated successfully.")
            else:
                logger.info("Column names do not match with schema file, moving file to invalid data folder")
        
            
            #check domain values
            cat_col_domain_value_validated = set()
            for key in schema_config['categorical_columns'].keys():
                if set(df[key].unique()).issubset(set(schema_config['domain_values'][key].keys())):
                    cat_col_domain_value_validated.add(True)
                    logger.info(f"Domain values of key {key} is validated successfully.")
                else:
                    cat_col_domain_value_validated.add(False)
                    logger.info(f"Domain values of key {key} is not validated.\n\
                        Domain values of key {key} in schema file is {schema_config['domain_values'][key].keys()}\n\
                        Domain values of key {key} in given file is {df[key].unique()}\n\
                            Moving file to invalid data folder")
            if False in cat_col_domain_value_validated:
                domain_val_validated = False
            else:
                domain_val_validated = True

            #Check if entire column has missing values
            null_val_col_validated = set()
            logger.info("Checking if entire column has missing values")
            for col in column_names:
                if df[col].isnull().sum()!=len(df[col]):
                    null_val_col_validated.add(True)
                    logger.info(f"column: {col} validated successfully.")
                else:
                    null_val_col_validated.add(False)
                    logger.info(f"file doesn't have any values in column {col}\n\
                                    Data validation unsuccessful. moving data to invalid data folder.")
            if False in null_val_col_validated:
                null_col_validated = False
            else:
                null_col_validated = True

            #logger.info(f"{file_name_validated} and {num_cols_validated} and {col_names_validated} \
             #                       and {domain_val_validated} and {null_col_validated}")
            #validation_status = file_name_validated and num_cols_validated and col_names_validated \
            #                        and domain_val_validated and null_col_validated
            logger.info(f"{num_cols_validated} and {col_names_validated} \
                                    and {domain_val_validated} and {null_col_validated}")
            validation_status = num_cols_validated and col_names_validated \
                                    and domain_val_validated and null_col_validated

            return validation_status

        except Exception as e:
            raise logger.exception(e)
        
    def get_and_save_data_drift_report(self,train_file_path, test_file_path):
        """
        Generate and save data drift report 
        returns report
        """
        try:
            data_drift_dataset_report = Report(metrics=[
                DatasetDriftMetric(),
                DataDriftTable(),    
            ])
            prev_data = pd.read_csv(train_file_path)
            new_data = pd.read_csv(test_file_path)
            data_drift_dataset_report.run(reference_data=prev_data, current_data=new_data)
            #report_file_path = os.path.join(self.upload_dir, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
            #report_page_file_path = os.path.join(self.upload_dir, DATA_VALIDATION_DRIFT_REPORT_PAGE_FILE_NAME)
            #report_dir = os.path.dirname(report_file_path)
            #os.makedirs(self.config.drift_report_file_path, exist_ok=True)
            #logger.info(os.path.exists(self.config.data_drift_report_dir))
            #logger.info(f"{report_file_path}, {report_page_file_path}")
            #if not os.path.exists(self.config.drift_report_file_path)
            #logger.info(type(self.dv_config.drift_report_file_path))
            #logger.info(type(self.dv_config.drift_report_page_path))   
            #logger.info(os.access(self.dv_config.drift_report_file_path, os.W_OK))         
            data_drift_dataset_report.save_json(self.dv_config.drift_report_file_path)
            data_drift_dataset_report.save_html(self.dv_config.drift_report_page_path)
            logger.info("saving dataset drift report")
        except Exception as e:
            logger.exception(e)

    
    def is_data_drift_found(self,train_file_path, test_file_path)->bool:
        """
        checks if data drift exists
        returns boolean value
        """
        try:
            logger.info("Checking for DataDrift..")
            self.get_and_save_data_drift_report(train_file_path, test_file_path)
            #self.save_data_drift_report_page(file_path)
            #logger.info(type(Path(self.dv_config.drift_report_file_path)))
            report_status = read_yaml(Path(self.dv_config.drift_report_file_path))
            logger.info(report_status.metrics[0].result.dataset_drift)
            data_drift = report_status.metrics[0].result.dataset_drift
            return data_drift
            #report_path = os.path.join(self.upload_dir, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
            #with open(report_path) as jobj:
            #    jdict = json.load(jobj)['metrics']['DatasetDriftMetric']['dataset_drift']
            #return jdict['metrics']['DatasetDriftMetric']['dataset_drift']
        except Exception as e:
            logger.exception(e)

    def initiate_data_validation(self,):        
        try:
            train_file_path = self.di_config.train_file
            test_file_path = self.di_config.test_file
            validation_status=True
            if (self.check_if_file_exists(train_file_path) & self.check_if_file_exists(test_file_path)):
                if (self.validate_dataset_schema(file_path=train_file_path) & self.validate_dataset_schema(file_path=test_file_path)):      
                    if self.is_data_drift_found(train_file_path, test_file_path):
                        logger.info("Data Validation unsuccessful. Data Drift Found.. Exiting program....")
                        sys.exit("Data Validation unsuccessful.. Data Drift detected. Exiting... See logs for more information.")
                    else:
                        logger.info("Data Drift not detected. Data Drift check completed successfully.")
                        logger.info("Data set validations completed successfully.")
                        validation_status=True        
                    
                else:
                    logger.info("Data Validation unsuccessful. ")
                    validation_status=False
            else:
                    msg = f" File does not Exists. Exiting the program... "
                    logger.info(msg)
                    validation_status=False
                    sys.exit("Data Validation unsuccessful. File not found. See logs for more information.")

            if validation_status:
                logger.info(f"Data validation successful. Moving files to {self.dv_config.valid_data_dir}")
                shutil.move(train_file_path, self.dv_config.valid_train_file_path)
                shutil.move(test_file_path, self.dv_config.valid_test_file_path)
            else:
                logger.info(f"Data validation unsuccessful. Moving files to {self.dv_config.invalid_data_dir}")
                shutil.move(test_file_path, self.dv_config.invalid_test_file_path)
                shutil.move(train_file_path, self.dv_config.invalid_train_file_path)
            with open(self.dv_config.validation_status, 'w') as f:
                f.write(f"Validation status: {validation_status}")
            #self.dv_config.validation_status = validation_status
            
        except Exception as e:
            logger.exception(e)
    