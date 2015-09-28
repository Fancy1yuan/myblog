from django.conf.urls import patterns, url
from views import index, detail, not_found, contact, about, test, Register

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^detail/$', detail, name='article_detail'),
                       url(r'^404/$', not_found),
                       url(r'^contact/$', contact, name='contact'),
                       url(r'^about/$', about, name='about'),
                       url(r'^test/$', test),
                       url(r'^register/$', Register.as_view(), name='register'),
        )