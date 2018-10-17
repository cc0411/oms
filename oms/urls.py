"""oms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve
from oms.settings import MEDIA_ROOT
from users.views import LoginView,LogoutView,IndexView
import xadmin
urlpatterns = [
    url(r'^xadmin/',xadmin.site.urls),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^host/',include('assets.urls',namespace='host')),
    url(r'^salt/',include('salt.urls',namespace='salt')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT }),
]
