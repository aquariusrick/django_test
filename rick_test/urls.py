from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('test_app.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^facebook_test', 'facebook_test', name='facebook_test'),
)

urlpatterns += patterns('',
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^admin/', include(admin.site.urls)),
)