from django.shortcuts import render
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
        current_menu = 'minionkey'
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



