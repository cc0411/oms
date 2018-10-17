# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import MinionListView
urlpatterns = [
    url(r'^minion/$',MinionListView.as_view(),name='minion'),

]