from django.conf.urls import patterns, url
from views import index, ArticleView, ArticlePublish, not_found, contact, about, test, RegisterView, cus_login, cus_logout, page_not_found

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^article/$', ArticleView.as_view(), name='article_detail'),
                       url(r'^articlepublish/$', ArticlePublish.as_view(), name='article_publish'),
                       url(r'^404/$', not_found),
                       url(r'^contact/$', contact, name='contact'),
                       url(r'^about/$', about, name='about'),
                       url(r'^test/$', test),
                       url(r'^register/$', RegisterView.as_view(), name='register'),
                       url(r'^login/$', cus_login, name='login'),
                       url(r'^logout/$', cus_logout, name='logout'),
                       url(r'^.*/$', page_not_found, name='not_found')
        )


