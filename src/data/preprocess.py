import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.utils.exceptions import CustomException
from src.utils.logger import logging
from src.utils.utils import save_model_or_data, load_model_and_data
from dataclasses import dataclass

@dataclass
class Preprocessing_config:
    processed_data_path: str = os.path.join('data/processed','processed.pkl')

class Preprocess:
    def __init__(self):
        self.preprocessing_config = Preprocessing_config()
    
    def transform(self, train_set:str, test_set:str):
        """
        This method preprocess the already splitted datasets.
        
        Args:-
            train_set: holds the path of the train set.
            test_set: holds the path of the test set. 
        
        return:
            processed datasets(train & test) in pickle form.
         
        """
        try:
            train_data = pd.read_csv(train_set)
            test_data = pd.read_csv(test_set)
            
            logging.info('Train and Test datasets are read.')
            
            dependent_variable = 'math score'
            
            numerical_features = train_data.select_dtypes(exclude='object').columns.drop('math score')
            categorical_features = train_data.select_dtypes(include='object').columns
            
            
            numeric_pipeline = Pipeline([("imputer",SimpleImputer(strategy="median")),('scaler',StandardScaler())])
            categorical_pipeline = Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),('ohe',OneHotEncoder())])
            
            ct = ColumnTransformer([('numeric_trans',numeric_pipeline,numerical_features),
                                    ('categoric_trans',categorical_pipeline,categorical_features)])
            
            
            y_train = np.array(train_data['math score'])
            y_test = np.array(test_data['math score'])
            
            X_train_df = train_data.drop('math score', axis=1)
            X_test_df = test_data.drop('math score', axis=1)
            
            
            X_train_trans = ct.fit_transform(X_train_df)
            X_test_trans = ct.transform(X_test_df)
            
            logging.info('X_train and X_test sets are transformed.')
            
            save_model_or_data(ct,self.preprocessing_config.processed_data_path)
            
            return (X_train_trans, X_test_trans, y_train, y_test) 
        
        except Exception as e:
            raise CustomException(e, sys)
       
        
        
        
        
        
