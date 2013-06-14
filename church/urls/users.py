# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from church.utils.const import MATCH_TEXT
from church.views.users import UserView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^%s/$' % MATCH_TEXT, UserView.as_view(), name='user'),
                       )
