from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blog_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<title>[^/]+)/$',
        views.post_page, name='post_page'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.index_day, name='index_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.index_month, name='index_month'),
    url(r'^(?P<year>\d{4})/$', views.index_year, name='index_year'),
]
