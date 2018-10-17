# -*- coding: utf-8 -*-

from .models import  SaltKeyList,MinionList,SaltCmdInfo

import xadmin

class KeyListAdmin(object):
    list_display =['minion_id','certification_status','utime']
    search_fields =['minion_id','certification_status','utime']
    list_filter =['minion_id','certification_status','utime']

class MinionListAdmin(object):
    list_display =['minion_id','ip','minion_version']
    search_fields = []
    list_filter = []

class CmdAdmin(object):
    list_display = []
    search_fields = []
    list_filter = []

xadmin.site.register(SaltKeyList,KeyListAdmin)
xadmin.site.register(MinionList,MinionListAdmin)
xadmin.site.register(SaltCmdInfo,CmdAdmin)