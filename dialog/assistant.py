from dialog.state_machine import RegistrationStateMachine, RegistrationState
from dialog.responses import ResponseManager
from nlp.entity_extractor import EntityExtractor
from nlp.faq_handler import FAQHandler
from registration.validator import RegistrationValidator
from registration.store import RegistrationStore


class RegistrationAssistant:
    """Complete conversational registration assistant."""

    def __init__(self):
        self.state_machine = RegistrationStateMachine()
        self.responses = ResponseManager()
        self.extractor = EntityExtractor()
        self.faq = FAQHandler()
        self.validator = RegistrationValidator()
        self.store = RegistrationStore()

    def start(self):
        """Start a fresh registration."""

        self.state_machine.reset()
        self.state_machine.start_registration()

        return (
            self.responses.greeting()
            + "\n\n"
            + self.responses.ask_name()
        )

    def process(self, user_input):
        """Process one user message."""

        if not user_input or not user_input.strip():
            return self.responses.fallback()

        text = user_input.strip()

        # FAQ can be asked at any point in the conversation.
        faq_answer = self.faq.find_answer(text)

        if faq_answer:
            return faq_answer

        # --------------------------------
        # CONFIRMATION
        # --------------------------------

        if self.state_machine.state == RegistrationState.CONFIRM:

            answer = text.lower()

            if answer in [
                "yes",
                "y",
                "confirm",
                "confirmed",
                "correct"
            ]:

                data = self.state_machine.get_data()

                if self.store.email_exists(data.get("email")):

                    existing = self.store.find_by_email(
                        data.get("email")
                    )

                    return (
                        "This email is already registered.\n"
                        f"Existing registration ID: "
                        f"{existing.get('registration_id')}\n"
                        "Please use a different email address."
                    )

                record, error = self.store.save(data)

                if error:
                    return error

                self.state_machine.next_state()

                return self.responses.registration_success(
                    record["registration_id"]
                )

            if answer in [
                "no",
                "n",
                "incorrect",
                "not correct"
            ]:

                self.state_machine.reset()

                return (
                    self.responses.cancellation()
                    + "\n\n"
                    + self.responses.ask_name()
                )

            return "Please answer yes or no."

        # --------------------------------
        # COMPLETED
        # --------------------------------

        if self.state_machine.state == RegistrationState.COMPLETED:

            return (
                "Your registration has already been completed. "
                "Please start a new registration if required."
            )

        # --------------------------------
        # ENTITY EXTRACTION
        # --------------------------------

        entities = self.extractor.extract_all(text)

        # --------------------------------
        # NAME
        # --------------------------------

        if self.state_machine.state == RegistrationState.ASK_NAME:

            name = entities.get("name")

            if not name and self._looks_like_name(text):
                name = text.strip().title()

            valid, _ = self.validator.validate_name(name)

            if not valid:
                return self.responses.invalid_name()

            self.state_machine.set_data("name", name)
            self.state_machine.next_state()

            return self.responses.ask_email()

        # --------------------------------
        # EMAIL
        # --------------------------------

        if self.state_machine.state == RegistrationState.ASK_EMAIL:

            email = entities.get("email")

            valid, _ = self.validator.validate_email(email)

            if not valid:
                return self.responses.invalid_email()

            if self.store.email_exists(email):

                existing = self.store.find_by_email(email)

                return (
                    "This email is already registered.\n"
                    f"Existing registration ID: "
                    f"{existing.get('registration_id')}\n"
                    "Please provide a different email address."
                )

            self.state_machine.set_data("email", email)
            self.state_machine.next_state()

            return self.responses.ask_field()

        # --------------------------------
        # FIELD
        # --------------------------------

        if self.state_machine.state == RegistrationState.ASK_FIELD:

            field = entities.get("field")

            if not field:
                field = text.strip()

            valid, _ = self.validator.validate_field(field)

            if not valid:
                return self.responses.invalid_field()

            self.state_machine.set_data("field", field)
            self.state_machine.next_state()

            return self.responses.ask_experience()

        # --------------------------------
        # EXPERIENCE
        # --------------------------------

        if self.state_machine.state == RegistrationState.ASK_EXPERIENCE:

            experience = entities.get("experience")

            valid, _ = self.validator.validate_experience(
                experience
            )

            if not valid:
                return self.responses.invalid_experience()

            self.state_machine.set_data(
                "experience",
                experience
            )

            self.state_machine.next_state()

            return self.responses.confirmation(
                self.state_machine.get_data()
            )

        return self.responses.fallback()

    def _looks_like_name(self, text):
        """Check whether plain text looks like a person's name."""

        words = text.split()

        if not 1 <= len(words) <= 4:
            return False

        for word in words:

            clean_word = word.replace("-", "")

            if not clean_word.isalpha():
                return False

        return True

    def get_data(self):
        return self.state_machine.get_data()

    def get_state(self):
        return self.state_machine.get_state()