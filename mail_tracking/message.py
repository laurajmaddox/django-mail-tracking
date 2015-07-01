from django.core.mail import EmailMultiAlternatives


class TrackedEmailMessage(EmailMultiAlternatives):
    """
    Subclass of EmailMultiAlternatives for creating tracked EmailMessages
    """
    def __init__(self, html_message, *args, **kwargs):
        super(TrackedEmailMessage, self).__init__(*args, **kwargs)

        self.alternatives = [(html_message, 'text/html')]


