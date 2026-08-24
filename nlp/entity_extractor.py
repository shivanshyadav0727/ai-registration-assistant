import re


class EntityExtractor:
    """Extract registration information from user messages."""

    EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

    EXPERIENCE_LEVELS = {
        "beginner": [
            "beginner",
            "basic",
            "novice",
            "new to programming",
            "no experience"
        ],
        "intermediate": [
            "intermediate",
            "moderate",
            "some experience"
        ],
        "advanced": [
            "advanced",
            "strong experience",
            "experienced"
        ],
        "expert": [
            "expert",
            "professional",
            "highly experienced"
        ]
    }

    FIELD_KEYWORDS = {
        "Computer Science": [
            "computer science",
            "cs",
            "computer science student"
        ],
        "Data Science": [
            "data science",
            "data scientist"
        ],
        "Information Technology": [
            "information technology",
            "information tech"
        ],
        "Engineering": [
            "engineering",
            "engineer"
        ],
        "Software Development": [
            "software development",
            "software developer",
            "software engineering"
        ]
    }

    def extract_email(self, text):
        """Extract an email address."""
        match = re.search(self.EMAIL_PATTERN, text)

        if match:
            return match.group(0)

        return None

    def extract_name(self, text):
        """Extract a person's name."""

        patterns = [
            r"\bmy name is\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,3})",
            r"\bi am\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,3})",
            r"\bi'm\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,3})",
            r"\bname is\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,3})"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                name = match.group(1).strip()

                name = re.split(
                    r"\s+(?:and|my|i|email|mail|gmail)\b",
                    name,
                    flags=re.IGNORECASE
                )[0]

                return name.strip().title()

        return None

    def extract_field(self, text):
        """Extract field of study."""

        text_lower = text.lower()

        for field, keywords in self.FIELD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return field

        return None

    def extract_experience(self, text):
        """Extract programming experience level."""

        text_lower = text.lower()

        for level, keywords in self.EXPERIENCE_LEVELS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level

        return None

    def extract_all(self, text):
        """Extract all supported entities."""

        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "field": self.extract_field(text),
            "experience": self.extract_experience(text)
        }

    def remove_empty(self, entities):
        """Remove entities that were not found."""

        return {
            key: value
            for key, value in entities.items()
            if value is not None
        }