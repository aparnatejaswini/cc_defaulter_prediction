## Credit Card Defaulter Prediction

### Problem Statement
A Taiwan-based credit card issuer wants to better predict the likelihood of default for its customers, as well as identify the key drivers that determine this likelihood. This would inform the issuer’s decisions on who to give a credit card to and what credit limit to provide. It would also help the issuer have a better understanding of their current and potential customers, which would inform their future strategy, including their planning of offering targeted credit products to their customers.


### Tech Stack Used
1. Cassandra
2. Python
3. Machine learning algorithms
4. FastAPI
5. Docker
6. AWS


Steps followed for training:
1. Retrieved data from URL/Cassandra database.
   Used StratifiedSplit to split data into train and test sets.
2. Univariate analysis.
3. Bivaraiate analysis.
4. Data quality and validation checks and data distribution checks using evidentlyAI.
5. Feature engineering.
6. Feature selection with Recursive Feature Elimination using CrossValidation.
7. Standardization of features.
8. Built models using GridsearchCV.
9. Retrieved best params from gridsearchcv and set the params for the respective model.
10. Trained models on training data, tested the models on testdata.
11. Used mlflow for experiment tracking.
12. Chose the best model based on F1-Score.
13. Combined train and test datasets and trained choosen model on whole data.
14. Saved model.


Steps followed for predicting data:
Assumption: User uploads a system generated file to predict which of its credit card customers may default for the next month.
1. User uploaded file is saved and goes through data quality, validation and distribution checks.
2. If uploaded file does not pass through validation checks user will be informed that the file do not pass validation checks. Information will be recorded in logs for further enquiry.
3. If data validation is successful, preprocess object will be loaded and applied to transform data.
4. Saved model will be loaded and used to predict whether customer will default or not.
5. File with uploaded data and predictions will be available for the user to download.
