# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from church.utils.const import MATCH_TEXT
from church.views.groups import GroupView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^%s/$' % MATCH_TEXT, GroupView.as_view(), name='group'),
                       )
