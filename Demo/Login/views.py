from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.


def basePage(request):
    return render(request, 'Login_App/basePage.html')


# @unauthenticated_user
def userLogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='ADMIN_USER').exists():
                    return HttpResponseRedirect(reverse('Manager:adminDashboard'))
                elif user.groups.filter(name='APP_USER').exists():
                    return HttpResponseRedirect(reverse('Manager:userDashboard'))
    return render(request, 'Login_App/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login:login'))


def user_reg(request):
    if request.method == 'POST':
        form = MainUserForm(request.POST)
        user_form = appUserForm(request.POST)

        if form.is_valid() and user_form.is_valid():
            userObj = form.save()
            group = Group.objects.get(name='APP_USER')
            userObj.groups.add(group)

            app_user = user_form.save(commit=False)
            app_user.user = userObj
            app_user.save()

            messages.success(request, 'Account was created.')
            return redirect('/')
        else:
            messages.info(request, 'Something went wrong')
    else:
        form = MainUserForm()
        user_form = appUserForm(request.POST)

    context = {'form': form,
               'user_form': user_form,
               'title': 'User Registration',
               'heading': 'User registration for view payment and statement info'}

    return render(request, 'Login_App/userReg.html', context)


def admin_user_reg(request):
    if request.method == 'POST':
        form = MainUserForm(request.POST)
        admin_form = AdminForm(request.POST)

        if form.is_valid() and admin_form.is_valid():
            userObj = form.save()
            group = Group.objects.get(name='ADMIN_USER')
            userObj.groups.add(group)

            app_user = admin_form.save(commit=False)
            app_user.user = userObj
            app_user.save()

            messages.success(request, 'Account was created.')
            return redirect('/')
        else:
            messages.info(request, 'Something went wrong')
    else:
        form = MainUserForm()
        admin_form = AdminForm(request.POST)

    context = {'form': form,
               'user_form': admin_form,
               'title': 'Admin Register',
               'heading': 'Admin registration'}

    return render(request, 'Login_App/userReg.html', context)
