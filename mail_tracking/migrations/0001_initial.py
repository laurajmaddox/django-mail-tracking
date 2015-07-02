# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedCampaign',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrackedCampaignEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('clicks', models.IntegerField(default=0)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=256)),
                ('opens', models.IntegerField(default=0)),
                ('recipients', models.IntegerField(default=0)),
                ('unsubscribes', models.IntegerField(default=0)),
                ('campaign', models.ForeignKey(to='mail_tracking.TrackedCampaign')),
            ],
        ),
    ]
