from django.test import TestCase

from mail_tracking.message import TrackedEmailMessage
from mail_tracking.models import TrackedCampaign, TrackedCampaignEmail


class TrackedEmailMessageTests(TestCase):
    """
    Tests for TrackedEmailMessage object creation and methods
    """
    def setUp(self):
        campaign = TrackedCampaign.objects.create(name='Set Up Campaign')
        campaign_email = TrackedCampaignEmail.objects.create(
            campaign=campaign, name='Set Up Email'
        )

        self.email_message = TrackedEmailMessage(
            campaign=campaign, campaign_email=campaign_email,
            subject='', body='', from_email='from@test.com', to=['to@test.com']
        )

    def test_set_campaign(self):
        """
        Test setting campaign attribute with a TrackedCampaign instance
        """
        # Test providing a TrackedCampaign instance
        campaign = TrackedCampaign.objects.create(name='Test Campaign 1')
        self.email_message._set_campaign(campaign)

        self.assertIs(campaign, self.email_message.campaign)

        # Test providing the name for a new campaign
        self.email_message._set_campaign('Test Campaign String')

        self.assertEqual('Test Campaign String', self.email_message.campaign.name)
        self.assertEqual('Test Campaign String',
            TrackedCampaign.objects.get(name='Test Campaign String').name
        )

    def test_set_email(self):
        """
        Test setting campaign_email attribute with a TrackedCampaignEmail instance
        """
        # Test providing a TrackedCampaignEmail instance
        campaign = TrackedCampaign.objects.create(name='Test Campaign')
        campaign_email = TrackedCampaignEmail.objects.create(
            campaign=campaign, name='Test Campaign Email'
        )
        self.email_message._set_campaign_email(campaign_email)

        self.assertIs(campaign_email, self.email_message.campaign_email)

        # Test providing the name for a new campaign email_message
        self.email_message._set_campaign_email('Test Campaign Email String')

        self.assertEqual(
            'Test Campaign Email String', self.email_message.campaign_email.name)
        self.assertEqual(
            'Test Campaign Email String', TrackedCampaignEmail.objects.get(
                name='Test Campaign Email String', campaign__name='Set Up Campaign'
            ).name
        )
