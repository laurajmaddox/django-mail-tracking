import os

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

    def test_tracked_email_init(self):
        """
        Test that TrackedEmailMessage is initialized with an HTML message body
        """
        self.message = TrackedEmailMessage(html_message=self.html_message)
        
        self.assertEqual(
            self.html_message, self.message.alternatives[0][0],
            msg='TrackedEmailMessage does not contain provided HTML message'
        )

    def test_email_send(self):
        """
        Test successful send() for TrackedEmailMessage
        """
        TrackedEmailMessage(
            subject='Test Subject', body='Test plain text body',
            from_email='test@fromdomain.com', to=['test@todomain.com'],
            html_message=self.html_message
        ).send()

        # Test that one message was sent
        self.assertEqual(
            len(mail.outbox), 1, msg='Mail not sent, or sent more than once'
        )
