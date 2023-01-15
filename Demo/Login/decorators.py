from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render, HttpResponseRedirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.groups.filter(name='ADMIN_USER').exists():
                return HttpResponseRedirect(reverse('Manager:adminDashboard'))
            elif user.groups.filter(name='APP_USER').exists():
                return HttpResponseRedirect(reverse('Manager:userDashboard'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
