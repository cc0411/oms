from django.shortcuts import render
from django.views.generic import View,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Assets,BusinessUnit,Tag,IDC
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.urls import reverse_lazy
from . import forms
# Create your views here.


class HostListView(LoginRequiredMixin,View):
    def get(self,request):
        current_page = 'server'
        current_menu = 'asset'
        all_hosts = Assets.objects.all().order_by('-ctime')
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_hosts = all_hosts.filter(Q(wip__icontains=search_keywords)|Q(nip__icontains=search_keywords))
        sort = request.GET.get('sort','')
        if sort:
            all_hosts = all_hosts.order_by("-{0}".format(sort))


        server_nums = all_hosts.count()
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_hosts,10,request=request)
        servers = p.page(page)
        return  render(request,'host.html',{'all_servers':servers,
                                            'server_nums':server_nums,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            'sort':sort,
                                            'search_keywords':search_keywords})
class IDCListView(LoginRequiredMixin,View):
    def get(self,request):
        current_page = 'idc'
        current_menu = 'asset'
        all_idcs = IDC.objects.all().order_by('-ctime')
        idc_nums = all_idcs.count()
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_idcs,1,request=request)
        idcs = p.page(page)
        return  render(request,'idc.html',{'all_idcs':idcs,
                                            'idc_nums':idc_nums,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            })
class TagListView(LoginRequiredMixin,View):
    def get(self,request):
        current_page = 'tag'
        current_menu = 'asset'
        all_roles = Tag.objects.all().order_by('-ctime')
        role_nums = all_roles.count()
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_roles,1,request=request)
        roles = p.page(page)
        return  render(request,'role.html',{'all_roles':roles,
                                            'role_nums':role_nums,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            })

class ServerAddView(LoginRequiredMixin,CreateView):
    model = Assets
    form_class = forms.ServerForm
    template_name = 'host_add.html'
    success_url = reverse_lazy('host:host')