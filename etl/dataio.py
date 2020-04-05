import gzip
import json
import pandas as pd
import numpy as np
import re


def parse(read_path, write_path):
    """Parse gz to json"""
    raw_data = []
    g = gzip.open(read_path, 'r')
    for line in g:
        raw_data.append(eval(line))
    with open(write_path, "w+") as f:
        f.write(json.dumps(raw_data))
    return print("File Parsed successfully")


def prune_rating(rating):
    """Turn five class to 3 major class"""
    if rating < 3:
        return 0
    elif rating > 3:
        return 2
    else:
        return 1


def preprocessor(text):
    """Removing http link and non word character at the beginning"""
    emoticons = re.findall(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = (re.sub(r'[\W]+', ' ', text.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return text


def create_balanced_data(read_path, write_path):
    """Build a balanced data set for ML"""
    colname = {
        "reviewerID": "_id",
        "asin": "asin",
        "reviewerName": "reviewer_name",
        "helpful": "helpful",
        "reviewText": "review_text",
        "overall": "overall",
        "summary": "summary",
        "unixReviewTime": "unix_review_time",
        "reviewTime": "review_time"
    }

    df = pd.read_json(read_path).rename(columns=colname)
    null_flag = df["review_text"].isnull().any()
    # Remove Null values if any
    if null_flag:
        df = df[df['review_text'].notna()]
    df["text_len"] = df["review_text"].apply(lambda x: len(x))
    # Remove rows with text length 0
    df = df[df["text_len"] != 0]
    # Pre-process the Text
    df["review_text"] = df["review_text"].apply(preprocessor)
    # Compute the frequency to dictionary
    df["pruned_rating"] = df["overall"].apply(lambda x: prune_rating(x))
    frequency = df.groupby(["pruned_rating"]).size().to_dict()
    max_class = max(frequency, key=frequency.get)
    max_value = frequency.get(max_class)
    # Up sample the class with lower frequency
    up_sample_list = []
    for key, value in frequency.items():
        if key == max_class:
            up_sample_list.append(df[df["pruned_rating"] == key])
        else:
            up_sample_list.append(
                df[df["pruned_rating"] == key]
                .sample(max_value, replace=True, random_state=103)
            )
    np.random.seed(103)
    up_sampled_df = pd.concat(up_sample_list)
    up_sampled_df = up_sampled_df.reset_index(drop=True)
    up_sampled_df = up_sampled_df.reindex(
        np.random.permutation(up_sampled_df.index)
    )
    up_sampled_df[["_id", "review_text", "pruned_rating"]].to_csv(
        write_path,
        index=False,
        encoding='utf-8'
    )
    return print("Data for Modeling is created successfully !")




