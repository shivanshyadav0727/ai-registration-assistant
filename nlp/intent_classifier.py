import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .preprocessing import TextPreprocessor


class IntentClassifier:
    """
    Hybrid intent classifier.

    1. Exact pattern matching handles known phrases reliably.
    2. TF-IDF + Logistic Regression handles new/unseen sentences.
    """

    def __init__(self, intents_file=None):

        if intents_file is None:
            intents_file = Path(__file__).parent / "intents.json"

        with open(intents_file, "r", encoding="utf-8") as file:
            self.intents = json.load(file)

        self.preprocessor = TextPreprocessor()

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True
        )

        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

        self._build_pattern_lookup()
        self._train()

    def _normalize(self, text):
        """Normalize text for exact pattern matching."""
        text = text.lower().strip()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)

        return text

    def _build_pattern_lookup(self):
        """Create lookup table for exact pattern matches."""
        self.pattern_lookup = {}

        for intent, data in self.intents.items():

            if intent == "unknown":
                continue

            for pattern in data["patterns"]:

                normalized = self._normalize(pattern)

                if normalized:
                    self.pattern_lookup[normalized] = intent

    def _train(self):
        """Train the ML classifier."""
        texts = []
        labels = []

        for intent, data in self.intents.items():

            if intent == "unknown":
                continue

            for pattern in data["patterns"]:

                processed = self.preprocessor.preprocess(pattern)

                if processed:
                    texts.append(processed)
                    labels.append(intent)

        if not texts:
            raise ValueError("No training patterns found in intents.json")

        features = self.vectorizer.fit_transform(texts)

        self.model.fit(features, labels)

    def predict(self, text):
        """Return the predicted intent."""
        intent, confidence = self.predict_with_confidence(text)

        return intent

    def predict_with_confidence(self, text):
        """
        Predict intent and confidence.

        Exact matches receive confidence 1.0.
        Otherwise ML prediction is used.
        """

        if not isinstance(text, str) or not text.strip():
            return "unknown", 0.0

        normalized_text = self._normalize(text)

        # -------------------------------------------------
        # STEP 1: Exact pattern matching
        # -------------------------------------------------

        if normalized_text in self.pattern_lookup:

            intent = self.pattern_lookup[normalized_text]

            return intent, 1.0

        # -------------------------------------------------
        # STEP 2: ML classification
        # -------------------------------------------------

        processed = self.preprocessor.preprocess(text)

        if not processed:
            return "unknown", 0.0

        features = self.vectorizer.transform([processed])

        probabilities = self.model.predict_proba(features)[0]

        best_index = probabilities.argmax()

        intent = self.model.classes_[best_index]

        confidence = float(probabilities[best_index])

        # -------------------------------------------------
        # STEP 3: Confidence threshold
        # -------------------------------------------------

        if confidence < 0.35:
            return "unknown", confidence

        return intent, confidence