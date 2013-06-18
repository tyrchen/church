# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import json
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import requests
from settings import API_SERVER

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class TeamView(TemplateView):
    template_name = 'church/team.html'

    def get_users(self, team):
        return requests.get(API_SERVER + '/directory/teams/%s.json' % team).json()

    def get_pr_list(self, uid):
        return requests.get(API_SERVER + '/gnats/%s.json' % uid).json()

    def get_context_data(self, **kwargs):
        team = self.kwargs['text']

        users = self.get_users(team)

        data = []
        for user in users['members']:
            issues = self.get_pr_list(user['uid'])
            data.append({'user': user, 'issues': issues})

        context = super(TeamView, self).get_context_data(**kwargs)

        context['data'] = data
        context['team'] = team

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamView, self).dispatch(*args, **kwargs)


class TeamProgressView(TemplateView):
    template_name = 'church/progress.html'

    def get_context_data(self, **kwargs):
        team = self.kwargs['text']
        day = self.kwargs['text1']
        data = requests.get(API_SERVER + '/gnats/progresses/%s/%s.json' % (team, day)).json()

        context = super(TeamProgressView, self).get_context_data(**kwargs)

        context['team'] = team

        if data:
            d = data[0]
            context['day'] = d['day'].split('T')[0]
            context['items'] = d['updates'].values()

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamProgressView, self).dispatch(*args, **kwargs)


class TeamRecentProgressView(TemplateView):
    template_name = 'church/recent_progress.html'

    def get_context_data(self, **kwargs):
        team = self.kwargs['text']
        data = requests.get(API_SERVER + '/gnats/progresses/%s/recent.json' % team).json()

        context = super(TeamRecentProgressView, self).get_context_data(**kwargs)

        items = []
        context['team'] = team
        for item in data:
            items.append({'day': item['day'].split('T')[0], 'updates': item['updates'].values()})

        context['items'] = items
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamRecentProgressView, self).dispatch(*args, **kwargs)