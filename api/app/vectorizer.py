from modelboy.utils import tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(
    strip_accents=None,
    lowercase=False,
    preprocessor=None,
    ngram_range=(1, 2),
    stop_words=None,
    tokenizer=tokenizer
)