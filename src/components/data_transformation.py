from src.logger import logger
from src.entity.config_entity import DataTransformationConfig, DataValidationConfig
from src.utils.common import save_object
from sklearn.base import TransformerMixin
#from imblearn.combine import SMOTETomek
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from pathlib import Path

import numpy as np
import pandas as pd
import sys


class FeatureGenerator(TransformerMixin):
    
    '''
    This class shall be used to
    - generate a new feature
    Upon calling fit_transform or transform method this column generates new dataframe columns
    '''
    def __init__(self):
      
        try:
            self.bill_amt1_ix = "x12"
            self.bill_amt2_ix = "x13"
            self.bill_amt3_ix = "x14"
            self.bill_amt4_ix = "x15"
            self.bill_amt5_ix = "x16"
            self.bill_amt6_ix = "x17"
            self.limit_bal_ix = "x1"
            self.pay_amt1_ix = "x18"
            self.pay_amt2_ix = "x19"
            self.pay_amt3_ix = "x20"
            self.pay_amt4_ix = "x21"
            self.pay_amt5_ix = "x22"
            self.pay_amt6_ix = "x23"
            

        except Exception as e:
            print(e)


    def fit(self, X):
        return self

    def transform(self, X):
    
        X['avg_bill_amt'] = (X[self.bill_amt1_ix]+X[self.bill_amt2_ix]+X[self.bill_amt3_ix] \
                                     +X[self.bill_amt4_ix]+X[self.bill_amt5_ix]+X[self.bill_amt6_ix])/6
        X['avg_leverage_ratio'] = (X[self.bill_amt1_ix]+X[self.bill_amt2_ix]+X[self.bill_amt3_ix] \
                                       +X[self.bill_amt4_ix]+X[self.bill_amt5_ix]+X[self.bill_amt6_ix])/(6*X[self.limit_bal_ix])
        X['avg_pay_amt'] = (X[self.pay_amt1_ix]+X[self.pay_amt2_ix]+X[self.pay_amt3_ix] \
                                      +X[self.pay_amt4_ix]+X[self.pay_amt5_ix]+X[self.pay_amt6_ix])/6
        X['avg_bill_to_pay'] = (X[self.bill_amt1_ix]+X[self.bill_amt2_ix]+X[self.bill_amt3_ix] \
                                       +X[self.bill_amt4_ix]+X[self.bill_amt5_ix]+X[self.bill_amt6_ix])/ \
                                        ((X[self.pay_amt1_ix]+X[self.pay_amt2_ix]+X[self.pay_amt3_ix] \
                                       +X[self.pay_amt4_ix]+X[self.pay_amt5_ix]+X[self.pay_amt6_ix])+1)

        return X


class DataTransformation():
    """
    This class shall be used to 
    - transform existing train data and test data
    - to create a preprocessed object for further use.
    returns data transformation artifact which contains transformed train and test file paths and preprocessed object file path.
    written by: Aparna T Parkala
    Version:1.0
    """
    def __init__(self, dv_config:DataValidationConfig, dt_config:DataTransformationConfig):
        try:
            logger.info(f"{'='*20} Data Transformation log started. {'='*20}")
            self.dv_config = dv_config
            self.dt_config = dt_config
        except Exception as e:
            logger.exception(e)


    @classmethod
    def data_transformer_object(cls, numeric_features, categorical_features)->Pipeline:
        '''
        input: list of numerical features and categorical features
        applies transformers on given data
        returns: preprocessed object
        '''
        try:
            # Create transformers
            categorical_transformer = OneHotEncoder()
            feature_generator = FeatureGenerator()
    
            # Create transformers
            numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
            categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

            # Create a column transformer
            preprocessor = ColumnTransformer(
                transformers=[
                            ('num', numeric_transformer, numeric_features),
                            ('cat', categorical_transformer, categorical_features)
                            ])

            # Create the pipeline
            pipeline = Pipeline(steps=[('feature generator', feature_generator),('preprocessor', preprocessor)])
            return pipeline
        
        except Exception as e:
            logger.exception(e)


    def initiate_data_transformation(self,):
        try:
            train_df = pd.read_csv(self.dv_config.valid_train_file_path)
            test_df = pd.read_csv(self.dv_config.valid_test_file_path)
            validated_raw_data=pd.concat([train_df, test_df]).drop(columns='y')
            validated_raw_data.to_csv(self.dt_config.validated_raw_data, index=False)
            #split feature and target columns
            drop_columns = self.dv_config.all_schema['drop_columns']
            target_column=self.dv_config.all_schema['target_column']
            train_df.drop(columns = drop_columns, inplace=True)
            test_df.drop(columns = drop_columns, inplace=True)
            feature_train_df = train_df.drop(columns=target_column, axis=1)
            target_train_df = train_df[target_column]
            feature_test_df = test_df.drop(columns=target_column, axis=1)
            target_test_df = test_df[target_column]

            #Applying feature engineering and data transformations
            numeric_features = self.dt_config.all_schema['numerical_features'].split(' ') + self.dt_config.all_schema['engineered_features'].split(' ')
            categorical_features = self.dt_config.all_schema['categorical_features'].split(' ')
            preprocessed_obj = self.data_transformer_object(numeric_features, categorical_features)
            transformed_feature_train_df = preprocessed_obj.fit_transform(feature_train_df)
            transformed_feature_test_df = preprocessed_obj.transform(feature_test_df)
            column_names = preprocessed_obj[1:].named_steps['preprocessor'].get_feature_names_out()
            X_train_transformed_df = pd.DataFrame(transformed_feature_train_df.toarray(), columns = column_names)
            x_test_transformed_df = pd.DataFrame(transformed_feature_test_df.toarray(), columns = column_names)
            logger.info("Feature transformation completed")
            logger.info(X_train_transformed_df.head())

            #Feature Selection
            clf = LogisticRegression(class_weight='balanced', max_iter=400)
            cv = StratifiedKFold(3, shuffle=True, random_state=42)
            rfecv_lr = RFECV(
                estimator=clf,
                step=0.05,
                cv=cv,
                scoring='f1',
                min_features_to_select=1,
                n_jobs=2, verbose=1
            )
            rfecv_lr.fit(X_train_transformed_df, target_train_df)
            logger.info(f"Optimal number of features: {rfecv_lr.n_features_}")
            '''
            #Applying smote
            smt = SMOTETomek(sampling_strategy="auto")
            f_train_df, t_train_df = smt.fit_resample( transformed_feature_train_df, 
                                                        target_train_df
                                                    )
            f_test_df, t_test_df = smt.fit_resample( transformed_feature_test_df, 
                                                        target_test_df
                                                    )
            '''
            
            feature_importance = pd.DataFrame({'features': rfecv_lr.get_feature_names_out(), 'importance': rfecv_lr.estimator_.coef_[0]}) \
                            .sort_values(by = 'importance', ascending=False)
            feature_importance = feature_importance[feature_importance['importance']>0]
            logger.info(f"Selected features are: {list(feature_importance.features)}")
            with open(self.dt_config.selected_features, 'w') as f:
                f.write(','.join(list(feature_importance.features)))
            X_train_fs1_df = X_train_transformed_df[feature_importance['features']]
            x_test_fs1_df = x_test_transformed_df[feature_importance['features']]
            train_pd = pd.concat([X_train_fs1_df, target_train_df], axis=1)
            test_pd = pd.concat([x_test_fs1_df, target_test_df], axis=1)
            train_pd.to_csv(self.dt_config.transformed_train_file, index=False, header=True)
            test_pd.to_csv(self.dt_config.transformed_test_file, index=False, header=True)
            
            logger.info(f"file path type: {type(self.dt_config.preprocess_obj)}")
            save_object(Path(self.dt_config.preprocess_obj), preprocessed_obj)
            logger.info(f"Data transformation complete.")

        except Exception as e:
            logger.exception(e)