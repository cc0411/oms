from django.shortcuts import render,redirect
from django.views.generic import  View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile
from .forms import LoginForm
from django.core.urlresolvers import reverse
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        rediect_url = request.GET.get('next','')
        return render(request,'login.html',{"redirect_url":rediect_url})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            user = authenticate(username=user_name,password=pass_word)

            if user is not  None:
                login(request,user)
                redirect_url = request.POST.get('next','')
                if redirect_url:
                    return redirect(redirect_url)
                return  redirect(reverse('index'))
            else:
                return render(request,'login.html',{'msg':"用户名或者密码错误"})
        else:
            return render(request,'login.html',{"login_form":login_form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse("index"))

class IndexView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        return render(request,'index.html',{})


