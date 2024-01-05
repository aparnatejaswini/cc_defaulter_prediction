import os
import pandas as pd
import urllib.request as request
from src.logger import logger
from src.utils.common import get_size
from pathlib import Path
from src.entity.config_entity import (DataIngestionConfig)
#from src.config.connect_database import CassandraConnect
#from src.constants import EnvironmentVariable
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    """
    This class shall be used for 
    - Retrieve data from database
    - Drop columns mentioned in schema file 
    - To split data as train and test sets for training.

    written by: Aparna T Parkala
    Version:1.0
    """
    def __init__(self, config: DataIngestionConfig):#, env_var:EnvironmentVariable):
        self.config = config
        '''
        self.env_var = env_var
        try:
            self.cas_connect = CassandraConnect(env_var=self.env_var)
            self.session = self.cas_connect.session
        except Exception as e:
            logger.exception(e)
            
        '''
    
    def download_file(self):
        try:
            if not os.path.exists(self.config.downloaded_data_file):
                filename, headers = request.urlretrieve(
                    url = self.config.source_url,
                    filename = self.config.downloaded_data_file
                )
                logger.info(f"{filename} download! with following info: \n{headers}")
            else:
                logger.info(f"File already exists of size: {get_size(Path(self.config.root_dir))} at location {Path(self.config.downloaded_data_file)} in {os.path.dirname(self.config.downloaded_data_file)}")
        except Exception as e:
            logger.exception(e)


    def export_file_as_df(self):

        df = pd.read_excel(self.config.downloaded_data_file, header=0)
        df.drop(index=0, axis=0, inplace=True)
        df.rename(columns={'Unnamed: 0':'ID'}, inplace=True)
        df.columns = df.columns.str.lower()
        for col in df.columns:
            df[col] = df[col].astype('int')
        df.reset_index(drop=True, inplace=True)
        logger.info(f"Downloaded file exported as a dataframe {df.head()}")
        return df
    '''
    def save_file_to_db(self)->None:
        """
        input: data_file_path, table_name, keyspace_name, db_name
        inserts data from data_file_path into keyspace_name.table_name
        output: returns None
        """
        try:
            df = pd.read_excel(self.config.downloaded_data_file, skiprows=0)
            df.drop(index=0, axis=0, inplace=True)
            df.rename(columns={'Unnamed: 0':'ID'}, inplace=True)
            df.columns = df.columns.str.lower()
            df = df.reindex(sorted(df.columns), axis=1)
            session = self.session
            session.execute(f"use {self.env_var.KEYSPACE_NAME}").one()
            session.execute(f'create table IF NOT EXISTS {self.env_var.TABLE_NAME} ( "ID" int primary key, \
                                                                        "X1" int, \
                                                                        "X2" int, \
                                                                        "X3" int, \
                                                                        "X4" int, \
                                                                        "X5" int, \
                                                                        "X6" int, \
                                                                        "X7" int, \
                                                                        "X8" int, \
                                                                        "X9" int, \
                                                                        "X10" int, \
                                                                        "X11" int, \
                                                                        "X12" int, \
                                                                        "X13" int, \
                                                                        "X14" int, \
                                                                        "X15" int, \
                                                                        "X16" int, \
                                                                        "X17" int, \
                                                                        "X18" int, \
                                                                        "X19" int, \
                                                                        "X20" int, \
                                                                        "X21" int, \
                                                                        "X22" int, \
                                                                        "X23" int, \
                                                                        "Y" int )')
            logger.info(f"{self.env_var.TABLE_NAME} Table created in Database: {self.env_var.DATABASE_NAME}, Keyspace: {self.env_var.KEYSPACE_NAME}")
            for i in df.values:
                session.execute(f"Insert into {self.env_var.TABLE_NAME}(id, x1, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x2, x20, x21, x22, x23, x3, x4, x5, x6, x7, x8, x9, y) VALUES{tuple(i)}")
            logger.info(f" records were inserted into {self.env_var.KEYSPACE_NAME}.{self.env_var.TABLE_NAME} in {self.env_var.DATABASE_NAME} database")
        except Exception as e:
            logger.exception(e)
        

    def export_table_as_df(self)->(pd.DataFrame):
        """
        input: table_name, keyspace_name, db_name
        Exports table as A DATAFRAME
        output: dataframe
        """
        try:
            session = self.session
            row = session.execute(f"SELECT * FROM {self.env_var.KEYSPACE_NAME}.{self.env_var.TABLE_NAME}")
            df = pd.DataFrame(row)
            logger.info(f"records were exported from {self.env_var.KEYSPACE_NAME}.{self.env_var.TABLE_NAME} in {self.env_var.DATABASE_NAME} database to a dataframe")
            return df
        except Exception as e:
            logger.exception(e)
        '''
    

    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        """
            This method accesses downloaded data and splits data file into train and test sets.
            Uses stratified shuffle split since dataset is imbalanced.
            saves train and test files in data ingestion artifact train and test file paths.
        """
        try:
            
            #split dataframe into train an test files
            logger.info("Splitting data into train and test sets")
            split = StratifiedShuffleSplit(n_splits=1, test_size=self.config.train_test_split_ratio, random_state=33)
            strat_train_set = None
            strat_test_set = None
            for train_idx, test_idx in split.split(dataframe, dataframe.iloc[:,-1]):
                strat_train_set = dataframe.loc[train_idx]
                strat_test_set = dataframe.loc[test_idx]
            logger.info("Performed Stratified Shuffle split on the dataframe")
            logger.info(f"Exporting train and test file path.")
            strat_train_set.to_csv(self.config.train_file, index=False, header=True)
            strat_test_set.to_csv(self.config.test_file, index=False, header=True)
            logger.info(f"Exported train and test file path.")
        except Exception as e:
            logger.exception(e)

  