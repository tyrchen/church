# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
import requests
from settings import API_SERVER

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class Team(models.Model):
    class Meta:
        app_label = 'church'
        db_table = 'church_team'
        verbose_name = 'Team'
        ordering = ['created']

    name = models.CharField('Team Name', max_length=24, unique=True)
    slug = models.CharField('Team Slug', max_length=24, unique=True)
    members = models.CharField('Team Members', max_length=2048, default='', help_text='Please enter member alias, '
                                                                                      'seperated by comma')
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    def update_remote_team(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = API_SERVER + '/directory/teams/%s.json' % self.slug
        data = {'name': self.name, 'members': self.members}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)

        self.update_remote_team()

        return super(Team, self).save(force_insert, force_update, using, update_fields)
