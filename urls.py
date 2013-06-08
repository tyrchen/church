from django.conf.urls import patterns, include, url

from django.contrib import admin
from church.utils import const
from church.views.common import StaticFileView, IndexView, SigninView, SignoutView

admin.autodiscover()

urlpatterns = patterns('',
                       url('^$', IndexView.as_view(), name="home"),
                       url('^signin/$', SigninView.as_view(), name='signin'),
                       url('^signout/$', SignoutView.as_view(), name='signout'),
                       url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^help/%s/$' % const.MATCH_TEXT, StaticFileView.as_view(), name='help')
                        )