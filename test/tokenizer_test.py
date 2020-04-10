import pandas as pd
from sklearn.linear_model import LogisticRegression
import os
import joblib
from modelboy.utils import tokenizer, version_by_date
from sklearn.feature_extraction.text import TfidfVectorizer


latest_data = version_by_date("./datalake/feed/", "csv")


def data_reader(path):
    """Load processed data and split in to train and test."""
    df = pd.read_csv(path)
    return df


df = data_reader(latest_data)


def train_test_split(df, pct):
    train_rows = int(df.shape[0]*(1-pct))
    x_train = df.loc[:train_rows, 'review_text'].values
    y_train = df.loc[:train_rows, 'pruned_rating'].values
    x_test = df.loc[train_rows:, 'review_text'].values
    y_test = df.loc[train_rows:, 'pruned_rating'].values
    return x_train, y_train, x_test, y_test


X_train, y_train, X_test, y_test = train_test_split(df, 0.7)

tf_idf = TfidfVectorizer(
    strip_accents=None,
    lowercase=False,
    preprocessor=None,
    ngram_range=(1, 2),
    stop_words=None,
    tokenizer=tokenizer
)

tf_idf.fit(X_train)

joblib.dump(tf_idf, os.path.join("./modellake/model_2/", "feature.pkl"))

vect = tf_idf.transform(X_train)

param_space = {
    "random_state": 1,
    "solver": 'liblinear',
    "C": 100.0,
    "penalty": 'l2',
}
clf = LogisticRegression(**param_space)

clf.fit(vect, y_train)

joblib.dump(clf, os.path.join("./modellake/model_2", "classifier.pkl"))

a_data = [X_test[1]]
transformed = tf_idf.transform(a_data)
clf.predict([a_data])

test_data = tf_idf.transform(X_test[:3])
clf.predict(test_data)

a_text = {"text": "The experience was very good, it is highly recommend"}
a_data = [a_text.get("text")]
test_data = tf_idf.transform(a_data)
class_id = int(clf.predict(test_data))
round(clf.predict_proba(test_data)[0][class_id]*100, 2)

int(class_id)