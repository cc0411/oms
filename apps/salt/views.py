from django.shortcuts import render,redirect
from django.views import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SaltKeyList,MinionList,SaltCmdInfo
# Create your views here.

class MinionListView(View):
    def get(self,request):
        current_page = 'salt'
        current_menu = 'minion'
        all_minions = MinionList.objects.all().order_by('-ctime')
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_minions = all_minions.filter(Q(minion_id__icontains=search_keywords)|Q(ip__icontains=search_keywords))
        sort = request.GET.get('sort','')
        if sort:
            all_minions = all_minions.order_by("-{0}".format(sort))


        minion_nums = all_minions.count()
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_minions,10,request=request)
        minions = p.page(page)
        return  render(request,'minions_list.html',{'all_minions':minions,
                                            'minion_nums':minion_nums,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            'sort':sort,
                                            'search_keywords':search_keywords})



class MinionKeyView(View):
    def get(self,request):
        current_page = 'salt'
        current_menu = 'keys'
        accepted_count = SaltKeyList.objects.filter(certification_status='accepted').count()
        unaccepted_count= SaltKeyList.objects.filter(certification_status='unaccepted').count()
        denied_count = SaltKeyList.objects.filter(certification_status='denied').count()
        rejected_count = SaltKeyList.objects.filter(certification_status='rejected').count()
        if request.GET.get('status') is None:
            return None
        if request.GET.get('status') == 'accepted':
            all_keys = SaltKeyList.objects.filter(certification_status='accepted')
        elif request.GET.get('status') == 'unaccepted':
            all_keys =SaltKeyList.objects.filter(certification_status='unaccepted')
        elif request.GET.get('status') =='denied':
            all_keys = SaltKeyList.objects.filter(certification_status='denied')
        elif request.GET.get('status') =='rejected':
            all_keys = SaltKeyList.objects.filter(certification_status='rejected')

        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_keys = all_keys.filter(minion_id__icontains=search_keywords)
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_keys,10,request=request)
        keys = p.page(page)
        return  render(request,'minions_keys.html',{'all_minions':keys,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            'search_keywords':search_keywords,
                                            'accepted_count':accepted_count,
                                            'unaccepted_count':unaccepted_count,
                                            'denied_count':denied_count,
                                            'rejected_count':rejected_count})