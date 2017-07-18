from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^users$', views.users),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^add_info$', views.add_info),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^all_interests$', views.all_interests),
]
