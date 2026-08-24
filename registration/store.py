import json
from pathlib import Path
from datetime import datetime


class RegistrationStore:
    """Store and manage internship registration records."""

    def __init__(self, file_path=None):

        if file_path is None:
            project_root = Path(__file__).resolve().parent.parent
            data_directory = project_root / "data"

            data_directory.mkdir(exist_ok=True)

            self.file_path = data_directory / "registrations.json"

        else:
            self.file_path = Path(file_path)

        self._initialize_file()

    def _initialize_file(self):
        """Create the JSON file if it does not exist."""

        if not self.file_path.exists():

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file, indent=4)

    def _load(self):
        """Load all registrations."""

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except (json.JSONDecodeError, FileNotFoundError):

            return []

    def _write(self, registrations):
        """Write registrations to JSON."""

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                registrations,
                file,
                indent=4
            )

    def get_all(self):
        """Return all registrations."""

        return self._load()

    def find_by_email(self, email):
        """Find a registration by email."""

        if not email:
            return None

        email = email.strip().lower()

        registrations = self._load()

        for registration in registrations:

            saved_email = registration.get(
                "email",
                ""
            ).strip().lower()

            if saved_email == email:
                return registration

        return None

    def email_exists(self, email):
        """Check whether an email is already registered."""

        return self.find_by_email(email) is not None

    def _generate_registration_id(self, registrations):
        """Generate the next registration ID safely."""

        highest_number = 0

        for registration in registrations:

            registration_id = registration.get(
                "registration_id",
                ""
            )

            if registration_id.startswith("REG-"):

                try:

                    number = int(
                        registration_id.replace(
                            "REG-",
                            ""
                        )
                    )

                    highest_number = max(
                        highest_number,
                        number
                    )

                except ValueError:
                    pass

        return f"REG-{highest_number + 1:04d}"

    def save(self, registration):
        """
        Save a registration.

        Returns:
            record, error

        Example:
            record, error = store.save(data)
        """

        registrations = self._load()

        email = registration.get("email")

        if self.email_exists(email):

            existing = self.find_by_email(email)

            return None, (
                f"This email is already registered with "
                f"registration ID {existing.get('registration_id')}."
            )

        record = registration.copy()

        record["registration_id"] = (
            self._generate_registration_id(
                registrations
            )
        )

        record["registered_at"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        registrations.append(record)

        self._write(registrations)

        return record, None