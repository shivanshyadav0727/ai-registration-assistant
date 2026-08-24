import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TextPreprocessor:
    """Preprocess user text for intent classification."""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def clean_text(self, text):
        """Clean, tokenize, remove stop words, and lemmatize text."""
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s]", " ", text)

        tokens = nltk.word_tokenize(text)

        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words
        ]

        return tokens

    def preprocess(self, text):
        """Return processed tokens as a single string."""
        return " ".join(self.clean_text(text))