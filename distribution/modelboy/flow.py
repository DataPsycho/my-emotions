import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from .utils import tokenizer, version_by_number
import os
import joblib


class ModelBoy:
    def __init__(self, data_dir: str, model_dir: str):
        """
        An API interface for training a logistic classifier.
        with fixed parameter.
        :parameter
            data_dir: root location of data directory
            model_dir: root location of model directory
        """
        self.data_dir = data_dir
        self.model_dir = model_dir

    def data_reader(self):
        """Load processed data and split in to train and test."""
        df = pd.read_csv(self.data_dir)
        return df

    @staticmethod
    def train_test_split(df, pct):
        """Split data in to train test set."""
        train_rows = int(df.shape[0]*(1-pct))
        x_train = df.loc[:train_rows, 'review_text'].values
        y_train = df.loc[:train_rows, 'pruned_rating'].values
        x_test = df.loc[train_rows:, 'review_text'].values
        y_test = df.loc[train_rows:, 'pruned_rating'].values
        return x_train, y_train, x_test, y_test

    @staticmethod
    def trainer(doc, label):
        """Train a classifier.
        :parameter
            doc: numpy array of documents
            label: pre labels of scores
        """
        tf_idf = TfidfVectorizer(
            strip_accents=None,
            lowercase=False,
            preprocessor=None,
            ngram_range=(1, 2),
            stop_words=None,
            tokenizer=tokenizer

        )
        param_space = {
            "random_state": 1,
            "solver": 'liblinear',
            "C": 100.0,
            "penalty": 'l2'
        }
        pipe = Pipeline([
            ('vect', tf_idf),
            ('clf', LogisticRegression(**param_space))
        ])
        pipe.fit(doc, label)
        return pipe

    def saver(self, model):
        """Save Model to Disk
        model: A defined or fitted model by trainer
        """
        files = [item for item in os.listdir(self.model_dir) if item != "temp"]
        try:
            if len(files) > 0:
                versions = [int(item.split("_")[1]) for item in files]
                new_version = "model_{}".format(max(versions) + 1)
                file_path = os.path.join(self.model_dir, new_version)
                os.mkdir(file_path)
                joblib.dump(model, os.path.join(file_path, "classifier.pkl"))
                print("Model Saved: {}".format(file_path))
            else:
                file_path = os.path.join(self.model_dir, "model_1")
                os.mkdir(file_path)
                joblib.dump(model, os.path.join(file_path, "classifier.pkl"))
                print("Model Saved: {}".format(file_path))
        except Exception as e:
            raise "Error Occurs: {}".format(e)


def loader(path, version=None):
    """Load a fitted or pre-defined model
    :parameter
        path: model root location
    """
    if version:
        model_dirs = os.listdir(path)
        if "model_".format(version) in model_dirs:
            model_path = os.path.join(path, "model_".format(version))
            model = joblib.load(os.path.join(model_path, "classifier.pkl"))
            return model
        else:
            print("Available models: {}".format(", ".join(model_dirs)))
            raise Exception("Model with that version do not exist.")
    else:
        latest_model = os.path.join(path, version_by_number(path))
        model = joblib.load(os.path.join(latest_model, "classifier.pkl"))
        return model



