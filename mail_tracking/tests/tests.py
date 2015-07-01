import os
from bs4 import BeautifulSoup

from django.core import mail
from django.test import TestCase

from mail_tracking.message import TrackedEmailMessage


class TrackedEmailMessageTests(TestCase):
    """
    Tests for TrackedEmailMessage class initialization and methods
    """
    @classmethod
    def setUpTestData(cls):
        cls.html_message = open(os.path.join(os.path.dirname(__file__), 'test_data/email_body.html')).read()
        cls.tracked_email = TrackedEmailMessage(
            subject='Test Subject', body='Test plain text body',
            from_email='test@fromdomain.com', to=['test@todomain.com'],
        )

    def test_add_beacon(self):      
        soup = BeautifulSoup(
            self.tracked_email._add_tracking_beacon(self.html_message)
        )
        beacon = soup.find('img', id='email_beacon')

        # Verify that a beacon img tag is present
        self.assertIsNotNone(beacon, msg="No beacon img tag found in HTML message")
