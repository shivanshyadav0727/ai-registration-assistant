class ResponseManager:
    """Generate responses for the registration conversation."""

    def greeting(self):
        return (
            "Hello! Welcome to the AI & Data Science Internship "
            "Registration Assistant. I can guide you through the "
            "registration process."
        )

    def ask_name(self):
        return "Please provide your full name."

    def ask_email(self):
        return "Thank you. Now please provide your email address."

    def ask_field(self):
        return "What is your field of study?"

    def ask_experience(self):
        return (
            "What is your programming experience level? "
            "Please choose beginner, intermediate, advanced, or expert."
        )

    def confirmation(self, data):
        return (
            "\nPlease confirm your registration details:\n"
            f"Name: {data.get('name')}\n"
            f"Email: {data.get('email')}\n"
            f"Field: {data.get('field')}\n"
            f"Experience: {data.get('experience')}\n\n"
            "Are these details correct? (yes/no)"
        )

    def registration_success(self, registration_id):
        return (
            f"\nRegistration successful!\n"
            f"Your registration ID is: {registration_id}\n"
            "Thank you for registering for the internship."
        )

    def invalid_name(self):
        return "That doesn't look like a valid name. Please enter your full name."

    def invalid_email(self):
        return "That email address is not valid. Please enter a valid email."

    def invalid_field(self):
        return "Please provide a valid field of study."

    def invalid_experience(self):
        return (
            "Please enter one of these experience levels: "
            "beginner, intermediate, advanced, or expert."
        )

    def cancellation(self):
        return (
            "Registration cancelled. "
            "You can start a new registration whenever you're ready."
        )

    def fallback(self):
        return (
            "I'm not sure I understood that. "
            "Please provide the information requested."
        )