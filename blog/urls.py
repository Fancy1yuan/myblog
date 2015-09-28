from django.conf.urls import patterns, url
from views import index, detail, not_found, contact, about

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^detail/$', detail),
                       url(r'^404/$', not_found),
                       url(r'^contact/$', contact),
                       url(r'^about/$', about),
        )