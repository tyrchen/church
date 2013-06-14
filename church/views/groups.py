# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import requests
from settings import API_SERVER

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class GroupView(TemplateView):
    template_name = 'church/group.html'

    def get_users(self, group):
        return requests.get(API_SERVER + '/directory/groups/%s.json' % group).json()

    def get_pr_list(self, uid):
        return requests.get(API_SERVER + '/gnats/%s.json' % uid).json()


    def get_context_data(self, **kwargs):
        group = self.kwargs['text']

        users = self.get_users(group)

        data = []
        for user in users['members']:
            issues = self.get_pr_list(user['uid'])
            data.append({'user': user, 'issues': issues})

        context = super(GroupView, self).get_context_data(**kwargs)

        context['data'] = data

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupView, self).dispatch(*args, **kwargs)


