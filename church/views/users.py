# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from dateutil.parser import parse
import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
import requests
from settings import API_SERVER

__author__ = 'tchen'
logger = logging.getLogger(__name__)

last_updater_ignore = ['gnats', 'slt-builder']

class UserView(TemplateView):
    template_name = 'church/user.html'

    def get_user(self, uid):
        return requests.get(API_SERVER + '/directory/employees/%s.json' % uid).json()

    def action_required(self, item):
        updater = item.get('last_updater', '')
        modified = parse(item['modified_at']).replace(tzinfo=None)
        now = datetime.now()
        if updater not in last_updater_ignore and updater != item['dev_owner'] and (now - modified).days < 5 and \
                item['responsible'] == item['dev_owner']:
            return True
        return False

    def get_pr_list(self, uid):
        data = requests.get(API_SERVER + '/gnats/%s.json' % uid).json()
        action_required_issues = []
        new_issues = []
        working_issues = []
        info_issues = []
        done_issues = []

        for item in data:

            if self.action_required(item):
                action_required_issues.append(item)
            elif item['state'] == 'open':
                new_issues.append(item)
            elif item['responsible'] == uid:
                working_issues.append(item)
            elif item['state'] == 'feedback' or item['state'] == 'monitored':
                done_issues.append(item)
            else:
                info_issues.append(item)

        return [
            ('Action Required Iusses', action_required_issues),
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
        context['total'] = sum(map(lambda x: len(x[1]), issue_lists))

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


class UserAddWorkingPRView(View):
    url = 'http://scrapy.jcnrd.us/schedule.json'

    def post(self, request, *args, **kwargs):
        items = request.POST.get('items')
        if request.user.username == self.kwargs['text']:
            items = map(lambda x: x.strip(), items.split(','))

            for item in items:
                payload = {'project': 'gnats', 'spider': 'worker_pr', 'uid': request.user.username, 'number': item}
                requests.post(self.url, payload)

            return HttpResponse(json.dumps({'status': 'ok'}))

        return HttpResponseBadRequest('Cannot update PR %s' % items)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserAddWorkingPRView, self).dispatch(*args, **kwargs)
