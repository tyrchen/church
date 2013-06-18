# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import requests
from settings import API_SERVER

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class UserView(TemplateView):
    template_name = 'church/user.html'

    def get_user(self, uid):
        return requests.get(API_SERVER + '/directory/employees/%s.json' % uid).json()

    def get_pr_list(self, uid):
        data = requests.get(API_SERVER + '/gnats/%s.json' % uid).json()
        new_issues = []
        working_issues = []
        info_issues = []
        done_issues = []

        for item in data:
            if item['state'] == 'open':
                new_issues.append(item)
            elif item['responsible'] == uid:
                working_issues.append(item)
            elif item['state'] == 'feedback' or item['state'] == 'monitored':
                done_issues.append(item)
            else:
                info_issues.append(item)

        return [
            ('Open Issues', new_issues),
            ('Working Issues', working_issues),
            ('Info Issues', info_issues),
            ('Done Issues (Monitored, Feedback)', done_issues)
        ]

    def get_context_data(self, **kwargs):
        uid = self.kwargs['text']

        issue_lists = self.get_pr_list(uid)
        user = self.get_user(uid)

        context = super(UserView, self).get_context_data(**kwargs)

        context['issue_lists'] = issue_lists
        context['engineer'] = user

        return context

    def post(self, request, *args, **kwargs):
        uid = self.kwargs['text']
        user = self.get_user(uid)
        number = request.POST.get('pk')
        if request.user.username == uid:
            name = request.POST.get('name')
            value = request.POST.get('value')
            url = API_SERVER + '/gnats/issues/%s.json' % number
            data = {'name': name, 'value': value}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.put(url, data=json.dumps(data), headers=headers)
            if r.status_code == 200:
                if name == 'comment':
                    # user updated the comment, so we add a progress record
                    progress_url = API_SERVER + '/gnats/progresses/%s.json' % number
                    data = {'uid': uid, 'progress': value, 'team': user['team']}
                    r = requests.post(progress_url, data=json.dumps(data), headers=headers)
                return HttpResponse('{}')
            else:
                return HttpResponseBadRequest('Cannot update PR %s' % number)

        return HttpResponseBadRequest('Cannot update PR %s' % number)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserView, self).dispatch(*args, **kwargs)


