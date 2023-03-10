# library doc string
"""
Churn library for Full process of churn prediction.

Author: Ahmed Aladdin
Creation Data: 5/3/2023
"""

# import libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import plot_roc_curve, classification_report


os.environ["QT_QPA_PLATFORM"] = "offscreen"


def import_data(pth):
    """
    returns dataframe for the csv found at pth

    input:
            pth: a path to the csv
    output:
            dataframe: pandas dataframe
    """
    # Read the datafile
    dataframe = pd.read_csv(pth, index_col=0)

    dataframe["Churn"] = dataframe["Attrition_Flag"].apply(
        lambda val: 0 if val == "Existing Customer" else 1
    )
    return dataframe


def perform_eda(dataframe):
    """
    perform eda on dataframe and save figures to images folder
    input:
            dataframe: pandas dataframe

    output:
            None
    """
    # Perform EDA

    column_names = ["Churn", "Customer_Age", "Marital_Status", "Total_Trans", "Heatmap"]
    for column_name in column_names:
        plt.figure(figsize=(20, 10))
        if column_name == "Churn":
            dataframe.Churn.hist()
        elif column_name == "Customer_Age":
            dataframe.Customer_Age.hist()
        elif column_name == "Marital_Status":
            dataframe.Marital_Status.value_counts("normalize").plot(kind="bar")
        elif column_name == "Total_Trans":
            sns.displot(dataframe.Total_Trans_Ct)
        elif column_name == "Heatmap":
            sns.heatmap(dataframe.corr(), annot=False, cmap="Dark2_r", linewidths=2)
        plt.savefig(f"eda_results/{column_name}.jpg")
        plt.close()


def encoder_helper(dataframe, category_lst):
    """
    helper function to turn each categorical column into a new column with
    propotion of churn for each category - associated with cell 15 from the notebook

    input:
            dataframe: pandas dataframe
            category_lst: list of columns that contain categorical features
    output:
            dataframe: pandas dataframe with new columns for
    """
    # Calc Churn mean value for each cat_col
    for category_name in category_lst:
        category_lst = []
        category_groups = dataframe.groupby(category_name).mean()["Churn"]
        for val in dataframe[category_name]:
            category_lst.append(category_groups.loc[val])
        dataframe[f"{category_name}_Churn"] = category_lst
    return dataframe


def perform_feature_engineering(dataframe):
    """
    input:
              dataframe: pandas dataframe
              response: string of response name [optional argument that could be used for
                naming variables or index y column]

    output:
              x_train: X training data
              x_test: X testing data
              y_train: y training data
              y_test: y testing data
    """
    keep_cols = [
        "Customer_Age",
        "Dependent_count",
        "Months_on_book",
        "Total_Relationship_Count",
        "Months_Inactive_12_mon",
        "Contacts_Count_12_mon",
        "Credit_Limit",
        "Total_Revolving_Bal",
        "Avg_Open_To_Buy",
        "Total_Amt_Chng_Q4_Q1",
        "Total_Trans_Amt",
        "Total_Trans_Ct",
        "Total_Ct_Chng_Q4_Q1",
        "Avg_Utilization_Ratio",
        "Gender_Churn",
        "Education_Level_Churn",
        "Marital_Status_Churn",
        "Income_Category_Churn",
        "Card_Category_Churn",
    ]
    y_data = dataframe["Churn"]
    x_data = pd.DataFrame()

    x_data[keep_cols] = dataframe[keep_cols]
    # train test split
    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data, test_size=0.3, random_state=42
    )

    return x_train, x_test, y_train, y_test


def classification_report_image(args):
    """
    produces classification report for training and testing results and stores report as image
    in images folder
    input:
            y_train: training response values
            y_test:  test response values
            y_train_preds_lr: training predictions from logistic regression
            y_train_preds_rf: training predictions from random forest
            y_test_preds_lr: test predictions from logistic regression
            y_test_preds_rf: test predictions from random forest

    output:
             None
    """
    y_train = args[0]
    y_test = args[1]
    y_train_preds_lr = args[2]
    y_train_preds_rf = args[3]
    y_test_preds_lr = args[4]
    y_test_preds_rf = args[5]
    clf_reports = {
        "random-forest": {
            "train": classification_report(y_train, y_train_preds_rf, output_dict=True),
            "test": classification_report(y_test, y_test_preds_rf, output_dict=True),
        },
        "logistic-regression": {
            "train": classification_report(y_train, y_train_preds_lr, output_dict=True),
            "test": classification_report(y_test, y_test_preds_lr, output_dict=True),
        },
    }
    for model_name in list(clf_reports.keys()):
        for split in ["train", "test"]:
            title = f"clf-report-{model_name}-{split}"
            axes = plt.axes()
            sns.heatmap(
                pd.DataFrame(clf_reports[model_name][split]).iloc[:-1, :].T,
                annot=True,
                ax=axes,
            )
            axes.set_title(title)
            plt.savefig(f"reports/{title}.jpg")
            plt.close()


def feature_importance_plot(model, x_data):
    """
    creates and stores the feature importances in pth
    input:
            model: model object containing feature_importances_
            x_data: pandas dataframe of X values
            output_pth: path to store the figure

    output:
             None
    """
    importances = model.best_estimator_.feature_importances_
    indices = np.argsort(importances)[::-1]
    names = [x_data.columns[i] for i in indices]

    plt.figure(figsize=(20, 5))
    plt.title("Feature Importance")
    plt.ylabel("Importance")
    plt.bar(range(x_data.shape[1]), importances[indices])
    plt.xticks(range(x_data.shape[1]), names, rotation=90)
    plt.savefig("reports/Feature_Importance.jpg")
    plt.close()


def train_models(x_train, x_test, y_train, y_test):
    """
    train, store model results: images + scores, and store models
    input:
              x_train: X training data
              x_test: X testing data
              y_train: y training data
              y_test: y testing data
    output:
              None
    """
    # grid search
    rfc = RandomForestClassifier(random_state=42)
    # Use a different solver if the default 'lbfgs' fails to converge
    # Reference:
    # https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
    lrc = LogisticRegression(solver="lbfgs", max_iter=3000)
    param_grid = {
        "n_estimators": [200, 500],
        "max_features": ["auto", "sqrt"],
        "max_depth": [4, 5, 100],
        "criterion": ["gini", "entropy"],
    }

    cv_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
    cv_rfc.fit(x_train, y_train)
    lrc.fit(x_train, y_train)

    y_train_preds_rf = cv_rfc.best_estimator_.predict(x_train)
    y_test_preds_rf = cv_rfc.best_estimator_.predict(x_test)

    y_train_preds_lr = lrc.predict(x_train)
    y_test_preds_lr = lrc.predict(x_test)

    classification_report_image(
        [
            y_train,
            y_test,
            y_train_preds_lr,
            y_train_preds_rf,
            y_test_preds_lr,
            y_test_preds_rf,
        ]
    )
    lrc_plot = plot_roc_curve(lrc, x_test, y_test)
    plt.close()
    plt.figure(figsize=(15, 8))
    axes = plt.gca()
    plot_roc_curve(cv_rfc.best_estimator_, x_test, y_test, ax=axes, alpha=0.8)
    lrc_plot.plot(ax=axes, alpha=0.8)
    plt.savefig("reports/plot_roc_curve.jpg")

    feature_importance_plot(cv_rfc, x_test)

    joblib.dump(cv_rfc.best_estimator_, "models/rfc_model.pkl")
    joblib.dump(lrc, "models/logistic_model.pkl")


if __name__ == "__main__":
    data_df = import_data("data/bank_data.csv")
    perform_eda(data_df)
    encoded_data_df = encoder_helper(
        data_df,
        [
            "Gender",
            "Education_Level",
            "Marital_Status",
            "Income_Category",
            "Card_Category",
        ],
    )
    x_train_, x_test_, y_train_, y_test_ = perform_feature_engineering(encoded_data_df)
    train_models(x_train_, x_test_, y_train_, y_test_)
