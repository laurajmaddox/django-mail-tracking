import os
from bs4 import BeautifulSoup

from django.test import TestCase

from mail_tracking.message import TrackedEmailMessage
from mail_tracking.models import TrackedCampaign, TrackedCampaignEmail


class TrackedEmailMessageTests(TestCase):
    """
    Tests for TrackedEmailMessage object creation and methods
    """
    def setUp(self):
        dummy_campaign = TrackedCampaign.objects.create(name='Set Up Campaign')

        dummy_campaign_email = TrackedCampaignEmail.objects.create(
            campaign=dummy_campaign, name='Set Up Email'
        )

        self.dummy_email_message = TrackedEmailMessage(
            campaign=dummy_campaign, campaign_email=dummy_campaign_email,
            subject='', body='', from_email='from@test.com', to=['to@test.com']
        )

        self.html_content = open(
            os.path.join(os.path.dirname(__file__), 'test_data/email_body.html')
        ).read()


    def test_init_instances(self):
        """
        Test passing instances of TrackedCampaign and 
        TrackedCampaignEmail to __init__
        """
        campaign = TrackedCampaign.objects.create(name='Set Up Campaign')

        campaign_email = TrackedCampaignEmail.objects.create(
            campaign=campaign, name='Set Up Email'
        )

        self.email_message = TrackedEmailMessage(
            campaign=campaign, campaign_email=campaign_email,
            subject='', body='', from_email='from@test.com', to=['to@test.com']
        )

        self.assertIs(campaign, self.email_message.campaign)
        self.assertIs(campaign_email, self.email_message.campaign_email)


    def test_init_strings(self):
        """
        Test passing name strings for new instances of TrackedCampaign
        and TrackedCampaignEmail to __init__
        """
        self.email_message = TrackedEmailMessage(
            campaign='Test Campaign String', 
            campaign_email='Test Campaign Email String', subject='', body='',
            from_email='from@test.com', to=['to@test.com']
        )

        self.assertEqual(
            'Test Campaign String', self.email_message.campaign.name
        )
        self.assertEqual(
            'Test Campaign Email String', self.email_message.campaign_email.name
        )

    def test_non_html_alternative(self):
        """
        Test that non-HTML alterantives remain unaltered
        """
        self.dummy_email_message.attach_alternative(
            self.html_content, 'text/plain'
        )
        self.assertEqual(
            (self.html_content, 'text/plain'), 
            self.dummy_email_message.alternatives[0]
        )               

    def test_add_tracking_beacon(self):
        """
        Test that a tracking beacon is added to an HTML alternative with
        the corect URL domain and tracking parameters
        """
        with self.settings(MAIL_TRACKING_URL='http://www.testdomain.com'):
            self.dummy_email_message.attach_alternative(
                self.html_content, 'text/html'
            )

            soup = BeautifulSoup(self.dummy_email_message.alternatives[0][0])

            test_beacon_url = '/'.join([
                'http://www.testdomain.com',
                str(self.dummy_email_message.campaign.id),
                str(self.dummy_email_message.campaign_email.id)
            ])

            beacon_tag = soup.find('img', id='email_beacon', src=test_beacon_url)

            self.assertEqual(test_beacon_url, beacon_tag['src'])
