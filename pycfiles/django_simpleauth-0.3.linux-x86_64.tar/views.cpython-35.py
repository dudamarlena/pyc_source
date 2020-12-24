# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratheek/msc/pythons/lib/python3.5/site-packages/simpleauth/views.py
# Compiled at: 2017-02-09 08:23:06
# Size of source mod 2**32: 1751 bytes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .forms import StartForm
from .models import Users

def start(request):
    if request.method == 'POST':
        start_form = StartForm(request.POST)
        if start_form.is_valid():
            data = start_form.save(commit=False)
            try:
                user_object = Users.objects.get(username=data.username)
            except Users.DoesNotExist:
                return render(request, 'simpleauth/fourohfour.html', {'user': data.username, 'title': 'BAD USER'})

            if data.password == user_object.password:
                users = Users.objects.values('username')
                return render(request, 'simpleauth/inside.html', {'users': users})
            msg = 'INVALID LOGIN ! PLEASE CHECK !'
            return render(request, 'simpleauth/outside.html', {'msg': msg, 'title': 'Invalid User'})
    else:
        start_form = StartForm()
    return render(request, 'simpleauth/index.html', {'start_form': start_form})


def register(request):
    if request.method == 'POST':
        reg_form = StartForm(request.POST)
        if reg_form.is_valid():
            reg_form.save(commit=True)
            return render(request, 'simpleauth/thanks.html', {})
    else:
        reg_form = StartForm()
    return render(request, 'simpleauth/register.html', {'reg_form': reg_form})