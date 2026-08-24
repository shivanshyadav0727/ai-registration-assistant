from enum import Enum


class RegistrationState(Enum):
    START = "start"
    ASK_NAME = "ask_name"
    ASK_EMAIL = "ask_email"
    ASK_FIELD = "ask_field"
    ASK_EXPERIENCE = "ask_experience"
    CONFIRM = "confirm"
    COMPLETED = "completed"


class RegistrationStateMachine:

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = RegistrationState.START

        self.user_data = {
            "name": None,
            "email": None,
            "field": None,
            "experience": None
        }

    def start_registration(self):
        self.state = RegistrationState.ASK_NAME
        return (
            "Great! I'll help you register for the internship. "
            "Please provide your full name."
        )

    def get_state(self):
        return self.state.value

    def set_data(self, key, value):
        if key in self.user_data:
            self.user_data[key] = value

    def get_data(self):
        return self.user_data.copy()

    def next_state(self):
        transitions = {
            RegistrationState.START: RegistrationState.ASK_NAME,
            RegistrationState.ASK_NAME: RegistrationState.ASK_EMAIL,
            RegistrationState.ASK_EMAIL: RegistrationState.ASK_FIELD,
            RegistrationState.ASK_FIELD: RegistrationState.ASK_EXPERIENCE,
            RegistrationState.ASK_EXPERIENCE: RegistrationState.CONFIRM,
            RegistrationState.CONFIRM: RegistrationState.COMPLETED,
            RegistrationState.COMPLETED: RegistrationState.COMPLETED
        }

        self.state = transitions[self.state]
        return self.state

    def get_prompt(self):
        prompts = {
            RegistrationState.START:
                "Would you like to register for the internship?",

            RegistrationState.ASK_NAME:
                "Please provide your full name.",

            RegistrationState.ASK_EMAIL:
                "Thank you. Now please provide your email address.",

            RegistrationState.ASK_FIELD:
                "What is your field of study?",

            RegistrationState.ASK_EXPERIENCE:
                "What is your programming experience level? "
                "For example: beginner, intermediate, advanced, or expert.",

            RegistrationState.CONFIRM:
                "Please confirm that your registration details are correct.",

            RegistrationState.COMPLETED:
                "Your registration has been completed successfully."
        }

        return prompts[self.state]

    def is_complete(self):
        return self.state == RegistrationState.COMPLETED

    def has_all_data(self):
        return all(
            value is not None
            for value in self.user_data.values()
        )