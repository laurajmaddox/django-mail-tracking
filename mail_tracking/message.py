from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from mail_tracking.models import TrackedCampaign, TrackedCampaignEmail


class TrackedEmailMessage(EmailMultiAlternatives):
    """
    Subclass of Django's EmailMultiAlternative for tracked campaign emails
    """
    def __init__(self, campaign, campaign_email, *args, **kwargs):
        """
        Extends intialization with identifying campaign information
        for creating tracking URLs

        campaign and campaign_email can be an existing instance or 
        'name' argument string for creating a new instance
        """
        super(TrackedEmailMessage, self).__init__(*args, **kwargs)

        self._set_campaign(campaign)
        self._set_campaign_email(campaign_email)


    def _set_campaign(self, campaign):
        """
        Sets the campaign attribute with a TrackedCampaign
        """
        if isinstance(campaign, str):
            campaign = TrackedCampaign.objects.create(name=campaign)

        campaign.save()

        self.campaign = campaign

    def _set_campaign_email(self, campaign_email):
        """
        Sets the campaign email attribute with a TrackedCampaignEmail
        """
        if isinstance(campaign_email, str):
            campaign_email = TrackedCampaignEmail.objects.create(
                campaign=self.campaign, name=campaign_email
            )

        campaign_email.save()

        self.campaign_email = campaign_email

