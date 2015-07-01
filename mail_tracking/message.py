from bs4 import BeautifulSoup

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class TrackedEmailMessage(EmailMultiAlternatives):
    """
    Subclass of EmailMultiAlternatives for creating tracked EmailMessages
    """ 
    def _add_tracking_beacon(self, html_message):
        """
        Add tracking beacon img tag with campaign and message identifiiers
        to email's HTML body
        """
        soup = BeautifulSoup(html_message)

        beacon_url = '/'.join([
            settings.MAIL_TRACKING_URL, 'TODOcampaign', 'TODOmsg'
        ])

        soup.body.append(
            soup.new_tag(
                'img', height='0', width='0', id='email_beacon', src=beacon_url
            )
        )

        return str(soup)
