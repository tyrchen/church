# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

import logging
logger = logging.getLogger(__name__)

__author__ = 'tchen'


register = template.Library()

@register.inclusion_tag('church/ttags/issue_table.html')
def issue_table(title, issues, uid, show_responsible=False):
    return {
        'title': title,
        'items': issues,
        'uid': uid,
        'total': len(issues),
        'show_responsible': show_responsible
    }

@register.inclusion_tag('church/ttags/progress_table.html')
def progress_table(day, items):
    title = '%s updates:' % day
    return {
        'title': title,
        'items': items,
    }
