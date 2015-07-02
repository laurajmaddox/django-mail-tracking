from django.db import models
from django.utils import timezone


class TrackedCampaign(models.Model):
    """
    Model for a campaign encompassing one or more tracked emails
    """
    name = models.CharField(max_length=256)
    creation = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(blank=True, null=True)


class TrackedCampaignEmail(models.Model):
    """
    Model for a tracked email within a campaign
    """
    campaign = models.ForeignKey(TrackedCampaign)
    clicks = models.IntegerField(default=0)
    creation = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=256)
    opens = models.IntegerField(default=0)
    recipients = models.IntegerField(default=0)
    unsubscribes = models.IntegerField(default=0)
