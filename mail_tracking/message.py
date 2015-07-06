from bs4 import BeautifulSoup

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

    def _add_tracking_beacon(self, html_content):
        """
        Add tracking beacon image tag with campaign/email identifiiers to 
        an HTML email body
        """
        soup = BeautifulSoup(html_content)

        beacon_url = '/'.join([
            settings.MAIL_TRACKING_URL, str(self.campaign.id),
            str(self.campaign_email.id)
        ])

        soup.body.append(
            soup.new_tag(
                'img', height='0', width='0', id='email_beacon', src=beacon_url
        ))

        return str(soup)


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

    def attach_alternative(self, content, mimetype):
        if mimetype == 'text/html':
            content = self._add_tracking_beacon(content)

        super(TrackedEmailMessage, self).attach_alternative(content, mimetype)

