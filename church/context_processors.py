# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from church.models import Team

__author__ = 'tchen'
logger = logging.getLogger(__name__)

from django.contrib.sites.models import Site


def site(request):
    import church
    from django.conf import settings
    return {
        'site': Site.objects.get_current(),
        'version': church.__version__,
        'groups': Team.objects.all()
    }
