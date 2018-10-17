# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import HostListView,IDCListView,TagListView,ServerAddView
urlpatterns = [
    url(r'^host/$',HostListView.as_view(),name='host'),
    url(r'^idc/$',IDCListView.as_view(),name='idc'),
    url(r'^role/$',TagListView.as_view(),name='role'),
    url(r'^host_add/$',ServerAddView.as_view(),name='host_add'),
]