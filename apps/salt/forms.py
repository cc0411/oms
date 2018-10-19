# -*- coding: utf-8 -*-

from django import forms


class MinionInstallForm(forms.Form):
    username = forms.CharField(max_length=24,required=True)
    password = forms.CharField(max_length=32,required=True)
    ip = forms.GenericIPAddressField(required=True)
    minion_id = forms.CharField(required=False)
    port = forms.IntegerField()