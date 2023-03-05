# Predict Customer Churn
- Project **Predict Customer Churn** of ML DevOps Engineer Nanodegree Udacity
## Project Description
In this project, we will use machine learning techniques to build a churn prediction model based on historical data of customer behavior and interactions. We will explore different features that may influence customer churn, We will also compare different machine learning algorithms and evaluate their performance on various metrics.
## Files and data description
- The training data provided in `data/bank_data.csv` which used to train and vaidate our models
- EDA plots that discribe the data features exist on `eda_results` directory:
    - [Churn.jpg](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/eda_results/Churn.jpg)
    - [Customer_Age](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/eda_results/Customer_Age.jpg)
    - [Heatmap](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/eda_results/Heatmap.jpg)
    - [Matrial_Status](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/eda_results/Marital_Status.jpg)
    - [Total_trans](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/eda_results/Total_Trans.jpg)
- Models metricies and plots saved on `reports` directory:
    - [Feature_Importance](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/Feature_Importance.jpg)
    - [clf-report-logistic-regression-test](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/clf-report-logistic-regression-test.jpg)
    - [clf-report-logistic-regression-train](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/clf-report-logistic-regression-train.jpg)
    - [clf-report-random-forest-test](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/clf-report-random-forest-test.jpg)
    - [clf-report-random-forest-train](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/clf-report-random-forest-train.jpg)
    - [plot_roc_curve](https://github.com/ahmedAlaa24494/Predict-Customer-Churn/blob/main/reports/plot_roc_curve.jpg)

- Running logs saved on `logs` directory.
## Running Files
- ### Cone the repo
---
- ### Install dependencies
```
pip install -r requirements.txt
```
--- 
- ### _Check Pep8 principles using pylint_
```
pylint churn_library.py  && pylint churn_script_logging_and_tests.py
```
---
- ### test and log the full process
```
python3 churn_script_logging_and_tests.py
```
---
- ### Train models
```
python3 churn_library.py
```