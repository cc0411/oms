# -*- coding: utf-8 -*-

from .models import  Assets,RemoteUser,BusinessUnit,IDC,Tag

import xadmin

class AssetAdmin(object):
    list_display =['hostname','server_type','wip','nip','cpu_info','memory','disk','ctime']
    search_fields =['wip','nip']
    list_filter =['ctime','server_type']

class RemoteUserAdmin(object):
    list_display =['username','password','name',]
    search_fields =['name',]
    list_filter =['name',]
class BusinessUnitAdmin(object):
    list_display =['parent_unit','name']
    search_fields =['name']
    list_filter =['name']
class IdcAdmin(object):
    list_display =['name','ctime']
    search_fields = ['name','ctime']
    list_filter = ['name','ctime']

class TagAdmin(object):
    list_display = ['name','ctime']
    search_fields = ['name','ctime']
    list_filter = ['name','ctime']

xadmin.site.register(Assets,AssetAdmin)
xadmin.site.register(BusinessUnit,BusinessUnitAdmin)
xadmin.site.register(RemoteUser,RemoteUserAdmin)
xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(IDC,IdcAdmin)