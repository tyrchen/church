from django.conf.urls import patterns, include, url

from django.contrib import admin
from church.utils import const
from church.views.common import IndexView, SigninView, SignoutView, DocFileView, HelpFileView

admin.autodiscover()

urlpatterns = patterns('',
                       url('^$', IndexView.as_view(), name="home"),
                       url('^signin/$', SigninView.as_view(), name='signin'),
                       url('^signout/$', SignoutView.as_view(), name='signout'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^users/', include('church.urls.users')),
                       url(r'^groups/', include('church.urls.teams'))
                       )

urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^help/%s/$' % const.MATCH_TEXT, HelpFileView.as_view(), name='help'),
                        url(r'^doc/%s/$' % const.MATCH_TEXT, DocFileView.as_view(), name='doc')
                        )