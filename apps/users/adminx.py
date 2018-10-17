# -*- coding: utf-8 -*-

import xadmin
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView,BaseSetting)

class GlobalSettings(object):
    site_title = "运维管理系统后台"
    site_footer ="corp 2018"
# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)