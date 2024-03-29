## Credit Card Defaulter Prediction

### Problem Statement
A Taiwan-based credit card issuer wants to better predict the likelihood of default for its customers, as well as identify the key drivers that determine this likelihood. This would inform the issuer’s decisions on who to give a credit card to and what credit limit to provide. It would also help the issuer have a better understanding of their current and potential customers, which would inform their future strategy, including their planning of offering targeted credit products to their customers.


### Tech Stack/Infrastructure Used
1. Cassandra
2. Python
3. Machine learning algorithms
4. FastAPI
5. Docker
6. AWS


### Steps followed for training:
1. **Data ingested** from URL/Cassandra database. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/data_ingestion.py)
2. **Split** the data into train and test sets.
3. **Explored data** for missing values, duplicates and outliers. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/notebook/ccdp-EDA.ipynb)
4. Univariate analysis.
5. Bivariate analysis.
6. Data quality and validation checks and data distribution checks using evidentlyAI. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/data_validation.py)
7. **Feature engineering**. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/data_transformation.py)
8. **Standardization** of features.
9. **Feature selection** with Recursive Feature Elimination using CrossValidation.
10. **Selected models** appropriate for classification problems.
11. **Trained models** on training data. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/train_model.py)
12. Tuned **hyper parameters** using GridSearchCV.
13. Used **mlflow** for **experiment tracking**. [link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/evluate_model.py)
14. **Evaluated best model** based on F1-Score. 
15. Combined train and test datasets and trained chosen model on whole data.[link](https://github.com/aparnatejaswini/cc_defaulter_prediction/blob/main/src/components/deploy_model.py)
16. Saved model.
17. **Deployed model** on AWS EC2 instance.


### Steps followed for prediction:
**Input:** User uploads a file to predict which of its credit card customers may default for the next month.
1. User uploaded file is saved and goes through data quality, validation, and distribution checks.
2. If the uploaded file does not pass through validation checks user will be informed that the file did not pass validation checks. Information will be recorded in logs for further inquiry.
3. If data validation is successful, a preprocess object will be loaded and applied to transform data.
4. The saved model will be loaded and used to predict whether the customer will default or not.
5. A file with uploaded data and predictions will be available for the user to download.
