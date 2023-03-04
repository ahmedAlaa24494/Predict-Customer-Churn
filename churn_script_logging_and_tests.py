import pytest
import os
import sys
import glob
import joblib
import logging
import churn_library as cl

logging.basicConfig(
    filename="logs/churn_library.log",
    level=logging.INFO,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


@pytest.fixture(name="data")
def data():
    """
    fixture function to return the data raw
    """
    try:
        dataframe = cl.import_data("data/bank_data.csv")
        logging.info("Raw dataframe fixture creation: SUCCESS")
    except FileNotFoundError as err:
        logging.error("Raw dataframe fixture creation: The file wasn't found")
        raise err

    return dataframe


@pytest.fixture(name="encoded_data")
def encoded_data(data):
    """
    encoded dataframe fixture - returns the encoded dataframe on some specific column
    """
    try:
        dataframe_encoded = cl.encoder_helper(
            data,
            [
                "Gender",
                "Education_Level",
                "Marital_Status",
                "Income_Category",
                "Card_Category",
            ]
        )
        logging.info("Encoded dataframe fixture creation: SUCCESS")
    except KeyError as err:
        logging.error(
            "Encoded dataframe fixture creation: Not existent column to encode"
        )
        raise err
    return dataframe_encoded


def test_import():
    """
    test data import - this example is completed for you to assist with the other test functions
    """
    try:
        dataframe = cl.import_data("data/bank_data.csv")
        logging.info("Testing import_data: SUCCESS")
    except FileNotFoundError as err:
        logging.error("Testing import_eda: The file wasn't found")
        raise err

    try:
        assert dataframe.shape[0] > 0
        assert dataframe.shape[1] > 0
    except AssertionError as err:
        logging.error(
            "Testing import_data: The file doesn't appear to have rows and columns"
        )
        raise err


def test_eda(data):
    """
    test perform eda function
    """
    cl.perform_eda(data)
    for image_name in [
        "Churn",
        "Customer_Age",
        "Marital_Status",
        "Total_Trans",
        "Heatmap",
    ]:
        assert os.path.isfile(f"eda_results/{image_name}.jpg")
        logging.info(f"Succesfully loaded %s.png" % image_name)


def test_encoder_helper(encoded_data):
    """
    test encoder helper
    """
    assert encoded_data.shape[0] > 0
    assert encoded_data.shape[1] > 0
    for column in [
        "Gender",
        "Education_Level",
        "Marital_Status",
        "Income_Category",
        "Card_Category",
    ]:
        assert column in encoded_data


def test_perform_feature_engineering(encoded_data):
    """
    test perform_feature_engineering
    """
    try:
        x_train, x_test, y_train, y_test = cl.perform_feature_engineering(
            encoded_data
        )

        logging.info("Feature sequence fixture creation: SUCCESS")
    except BaseException:
        logging.error("Feature sequences fixture creation: Sequences length mismatch")
        raise
    try:
        assert len(x_train) == len(y_train)
        assert len(x_test) == len(y_test)
        logging.info("Testing feature_engineering: SUCCESS")
    except AssertionError as err:
        logging.error("Testing feature_engineering: Sequences length mismatch")
        raise err


def test_train_models(encoded_data):
    """
    test train_models
    """
    x_train, x_test, y_train, y_test = cl.perform_feature_engineering(
        encoded_data
    )

    cl.train_models(x_train, x_test, y_train, y_test)
    try:
        joblib.load("models/rfc_model.pkl")
        joblib.load("models/logistic_model.pkl")
        logging.info("Testing testing_models: SUCCESS")
    except FileNotFoundError as err:
        logging.error("Failed Test couldn't find model artifacts")
        raise err
    for image_name in [
        "clf-report-logistic-regression-test",
        "clf-report-logistic-regression-train",
        "clf-report-random-forest-test",
        "clf-report-random-forest-train",
        "Feature_Importance",
    ]:
        try:
            with open("reports/%s.jpg" % image_name, "r"):
                logging.info("Testing testing_models (report generation): SUCCESS")
        except FileNotFoundError as err:
            logging.error(
                "Testing testing_models (report generation): generated images missing"
            )
            raise err


if __name__ == "__main__":
    for directory in ["logs", "eda_resutls", "reports", "models"]:
        files = glob.glob("%s/*" % directory)
        for file in files:
            os.remove(file)
    sys.exit(pytest.main(["-s"]))
