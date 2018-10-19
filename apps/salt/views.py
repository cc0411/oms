from django.shortcuts import render,redirect
from django.views import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from .salt_api import SaltAPI
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SaltKeyList,MinionList,SaltCmdInfo
# Create your views here.
from .forms import MinionInstallForm
from django.http import JsonResponse
import  json



class MinionListView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
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



class KeyAccptedView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        current_page = 'keys'
        current_menu = 'accepted'
        accepted_count = SaltKeyList.objects.filter(certification_status='accepted').count()
        unaccepted_count= SaltKeyList.objects.filter(certification_status='unaccepted').count()
        denied_count = SaltKeyList.objects.filter(certification_status='denied').count()
        rejected_count = SaltKeyList.objects.filter(certification_status='rejected').count()
        all_keys = SaltKeyList.objects.filter(certification_status='accepted')

        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_keys = all_keys.filter(minion_id__icontains=search_keywords)
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page =1

        p = Paginator(all_keys,10,request=request)
        keys = p.page(page)
        return  render(request,'minions_accepted.html',{'all_keys':keys,
                                            'current_menu':current_menu,
                                            'current_page':current_page,
                                            'search_keywords':search_keywords,
                                            'accepted_count':accepted_count,
                                            'unaccepted_count':unaccepted_count,
                                            'denied_count':denied_count,
                                            'rejected_count':rejected_count})

class KeyUnacceptedView(LoginRequiredMixin, View):
        login_url = '/login/'
        redirect_field_name = 'next'

        def get(self, request):
            current_page = 'keys'
            current_menu = 'unaccepted'
            accepted_count = SaltKeyList.objects.filter(certification_status='accepted').count()
            unaccepted_count = SaltKeyList.objects.filter(certification_status='unaccepted').count()
            denied_count = SaltKeyList.objects.filter(certification_status='denied').count()
            rejected_count = SaltKeyList.objects.filter(certification_status='rejected').count()
            all_keys = SaltKeyList.objects.filter(certification_status='unaccepted')

            search_keywords = request.GET.get('keywords', '')
            if search_keywords:
                all_keys = all_keys.filter(minion_id__icontains=search_keywords)
            try:
                page = request.GET.get('page', '1')
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_keys, 10, request=request)
            keys = p.page(page)
            return render(request, 'minions_accepted.html', {'all_keys': keys,
                                                             'current_menu': current_menu,
                                                             'current_page': current_page,
                                                             'search_keywords': search_keywords,
                                                             'accepted_count': accepted_count,
                                                             'unaccepted_count': unaccepted_count,
                                                             'denied_count': denied_count,
                                                             'rejected_count': rejected_count})


class KeyDeniedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        current_page = 'keys'
        current_menu = 'denied'
        accepted_count = SaltKeyList.objects.filter(certification_status='accepted').count()
        unaccepted_count = SaltKeyList.objects.filter(certification_status='unaccepted').count()
        denied_count = SaltKeyList.objects.filter(certification_status='denied').count()
        rejected_count = SaltKeyList.objects.filter(certification_status='rejected').count()
        all_keys = SaltKeyList.objects.filter(certification_status='denied')

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_keys = all_keys.filter(minion_id__icontains=search_keywords)
        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_keys, 10, request=request)
        keys = p.page(page)
        return render(request, 'minions_accepted.html', {'all_keys': keys,
                                                         'current_menu': current_menu,
                                                         'current_page': current_page,
                                                         'search_keywords': search_keywords,
                                                         'accepted_count': accepted_count,
                                                         'unaccepted_count': unaccepted_count,
                                                         'denied_count': denied_count,
                                                         'rejected_count': rejected_count})


class MinionInstallView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        return  render(request,'minion_install.html')
    def post(self,request):
        minion_instalform = MinionInstallForm(request.POST)
        if minion_instalform.is_valid():
            ip = request.POST.get('ip','')
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            port = request.POST.get('port',22)
            minion_id = request.POST.get('minion_id',ip)
            try:
                with open(r'/etc/salt/roster','w')  as roster:
                    roster.write('\n%s:\n  host: %s\n  user: %s\n  passwd: %s\n  port: %s\n' % (ip, ip, username, password, port))
                    print('主机信息写入成功')
            except Exception as e:
                print('写入失败')
                return JsonResponse({'result':'主机信息写入失败','status':False})
            else:
                params = {'client': 'ssh', 'tgt': ip, 'tgt_type': 'glob', 'fun': 'test.ping'}
                try:
                    salt = SaltAPI()
                    rpost =salt.public(json=params)
                except Exception as e:
                    return JsonResponse({'result':'接口有问题','status':False})
                else:
                    if 'Permission denied' in  json.dumps(rpost.json()):
                        return JsonResponse({'result':'用户名或者密码错误','status':False})
                    elif 'Connection refused' in json.dumps(rpost.json()):
                        return JsonResponse({'result':'无法连接','status':False})
                    elif '"return": true' in json.dumps(rpost.json()):
                        try:
                            minion_post = salt.install_minion_api(tgt=ip,arg='init.minion_install')
                        except Exception as e:
                            return JsonResponse({'result':'部署失败','status':False})
                        else:
                            return JsonResponse({'result':'部署成功','status':True})
                    else:
                        return JsonResponse({'result':'无法连接master','status':False})


class CmdView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'cmd.html')
    def post(self,request):
        pass













