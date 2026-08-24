import re


class RegistrationValidator:
    """Validate student registration information."""

    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    ALLOWED_EXPERIENCE = {
        "beginner",
        "intermediate",
        "advanced",
        "expert"
    }

    def validate_name(self, name):
        """Validate student name."""

        if not name:
            return False, "Name is required."

        name = name.strip()

        if len(name) < 2:
            return False, "Name must contain at least 2 characters."

        if len(name) > 100:
            return False, "Name is too long."

        if not re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", name):
            return False, "Name should contain letters only."

        return True, "Valid name."

    def validate_email(self, email):
        """Validate email address."""

        if not email:
            return False, "Email address is required."

        email = email.strip()

        if not re.fullmatch(self.EMAIL_PATTERN, email):
            return False, "Please provide a valid email address."

        return True, "Valid email."

    def validate_field(self, field):
        """Validate field of study."""

        if not field:
            return False, "Field of study is required."

        if len(field.strip()) < 2:
            return False, "Please provide a valid field of study."

        return True, "Valid field."

    def validate_experience(self, experience):
        """Validate programming experience."""

        if not experience:
            return False, "Programming experience is required."

        experience = experience.lower().strip()

        if experience not in self.ALLOWED_EXPERIENCE:
            return False, (
                "Experience must be beginner, intermediate, "
                "advanced, or expert."
            )

        return True, "Valid experience."

    def validate_registration(self, data):
        """Validate complete registration data."""

        errors = {}

        valid, message = self.validate_name(data.get("name"))
        if not valid:
            errors["name"] = message

        valid, message = self.validate_email(data.get("email"))
        if not valid:
            errors["email"] = message

        valid, message = self.validate_field(data.get("field"))
        if not valid:
            errors["field"] = message

        valid, message = self.validate_experience(
            data.get("experience")
        )
        if not valid:
            errors["experience"] = message

        return len(errors) == 0, errors