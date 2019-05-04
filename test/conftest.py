import pytest
import os
import sys
import email

HERE = os.path.dirname(__name__) or "test"
EMAILS_FOLDER = os.path.join(HERE, "emails")

# modify the path to import every module
sys.path.append(".")
sys.path.append(HERE)
sys.path.append(os.path.join(HERE, ".."))

class Emails:
    """Collection of emails"""

    def __getitem__(self, email_name):
        """Return the email with a given name."""
        email_path = os.path.join(EMAILS_FOLDER, email_name + ".eml")
        with open(email_path, "rb") as file:
            return email.message_from_bytes(file.read())

@pytest.fixture
def emails():
    return Emails()

@pytest.fixture
def calendar():
    import mailboxcalendar
    return mailboxcalendar.MailboxCalendar()

