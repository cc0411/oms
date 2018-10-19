# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import MinionListView,KeyAccptedView,KeyDeniedView,KeyUnacceptedView
urlpatterns = [
    url(r'^minion/$',MinionListView.as_view(),name='minion'),
    url(r'^key/accpted/$',KeyAccptedView.as_view(),name='key_accpted'),
    url(r'^key/unaccpted/$',KeyUnacceptedView.as_view(),name='key_unaccpted'),
    url(r'^key/denied/$',KeyDeniedView.as_view(),name='key_denied'),

]