from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Stunum
from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import getscore


@login_required
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            message = '用户名或密码错误！'
    return render(request, 'login.html', locals())

def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required
def password(request):
    if request.method == 'POST':
        password = request.POST['password']
        u = User.objects.get(username = request.user.username)
        u.set_password(password)
        u.save()
        return redirect('/')
    return render(request, 'password.html', locals())
