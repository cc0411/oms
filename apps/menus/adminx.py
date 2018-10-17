# -*- coding: utf-8 -*-
from .models import Menu
import xadmin

class MenyAdmin(object):
    list_display =['name','path','icon','parent_menus']
    search_fields = []
    list_filter = []


xadmin.site.register(Menu,MenyAdmin)