import json
from pathlib import Path


class FAQHandler:

    def __init__(self, faq_file=None):

        if faq_file is None:
            faq_file = (
                Path(__file__).resolve().parent
                / "faq.json"
            )

        self.faq_file = Path(faq_file)
        self.faqs = self._load_faqs()

    def _load_faqs(self):

        with open(
            self.faq_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def find_answer(self, user_input):

        text = user_input.lower().strip()

        for faq in self.faqs.values():

            for pattern in faq["patterns"]:

                if pattern in text:
                    return faq["response"]

        return None