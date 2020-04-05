# import spacy
import os
from datetime import datetime as dt
import re
# nlp = spacy.load('en_core_web_md')


# def tokenizer_lemma(sentence: str):
#     """Make token of Lemma from actual word
#     :parameter
#         sentence: single document of string
#     """
#     return [token.lemma_ for token in nlp(sentence)]


def tokenizer(text):
    """Removing http link and non word character at the beginning"""
    emoticons = re.findall(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = (re.sub(r'[\W]+', ' ', text.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return text.split()


def version_by_date(path: str, extension: str):
    """Select the latest file form a dictionary.
    :parameter
        path: root path
        extension: file extension
    """
    file_pattern = "." + extension
    dir_list = [
        item.split("_")[1] for item in os.listdir(path) if "version" in item
    ]
    versions = [
        dt.strptime(item.replace(file_pattern, ""), '%Y-%m-%d').date()
        for item in dir_list
    ]
    latest_version = "version_{}.{}".format(max(versions), extension)
    return os.path.join(path, latest_version)


def version_by_number(path):
    """Select the latest file form a dictionary.
    :parameter
        path: root path
    """
    dir_list = [
        item.split("_")[1] for item in os.listdir(path) if "model" in item
    ]
    if len(dir_list) > 0:
        versions = [int(item) for item in dir_list]
        latest_version = "model_{}".format(max(versions))
        return latest_version
    else:
        raise Exception("There is no model")


