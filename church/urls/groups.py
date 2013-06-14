# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from church.utils.const import MATCH_TEXT, MATCH_TEXT1
from church.views.groups import GroupView, GroupProgressView, GroupRecentProgressView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^%s/$' % MATCH_TEXT, GroupView.as_view(), name='group'),
                       url(r'^%s/recent/$' % MATCH_TEXT, GroupRecentProgressView.as_view(), name='recent_progress'),
                       url(r'^%s/%s/$' % (MATCH_TEXT, MATCH_TEXT1), GroupProgressView.as_view(), name='progress'),
                       )
