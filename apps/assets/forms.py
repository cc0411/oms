# -*- coding: utf-8 -*-
from django.forms import  ModelForm,fields,widgets
from assets import models

class ServerForm(ModelForm):
    class Meta:
        model = models.Assets
        #fields = '__all__'
        exclude = ['ctime',]
        error_message ={
            'hostname': {'required': '主机名不能为空',},
            'wip': {'required': '外网地址不能为空', 'invalid': 'IP地址格式错误'},
            'nip': {'required': '内网地址不能为空', 'invalid': 'IP地址格式错误'},
            'system_type': {'required': '系统类型不能为空'},


        }
        widgets = {
            'hostname': widgets.TextInput(attrs={'class': 'form-control',}),
            'server_type':widgets.Select(attrs={'class':'form-control'}),
            'idc': widgets.Select(attrs={'class': 'form-control'}),
            'business_unit': widgets.Select(attrs={'class': 'form-control'}),
            'mip': widgets.TextInput(attrs={'class': 'form-control', }),
            'nip': widgets.TextInput(attrs={'class': 'form-control',}),
            'wip': widgets.TextInput(attrs={'class': 'form-control',}),
            'sn': widgets.TextInput(attrs={'class': 'form-control', }),
            'cpu_model': widgets.TextInput(attrs={'class': 'form-control', }),
            'kennel': widgets.TextInput(attrs={'class': 'form-control', }),
            'cpu_num': widgets.TextInput(attrs={'class': 'form-control',}),
            'role': widgets.SelectMultiple(attrs={'class': 'form-control', }),
            'memory': widgets.TextInput(attrs={'class': 'form-control',}),
            'disk': widgets.TextInput(attrs={'class': 'form-control',}),
            'instance_id': widgets.TextInput(attrs={'class': 'form-control',}),
            'system_type': widgets.TextInput(attrs={'class': 'form-control',}),
            'desc': widgets.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'hostname': '*  必填项目,名字唯一,主机名这里请不要写IP',

        }