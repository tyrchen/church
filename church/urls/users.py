# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from church.utils.const import MATCH_TEXT
from church.views.users import UserView, UserAddWorkingPRView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^%s/$' % MATCH_TEXT, UserView.as_view(), name='user'),
                       url(r'^%s/add-pr/$' % MATCH_TEXT, UserAddWorkingPRView.as_view(), name="user_add_working_pr"),
                       )
