# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/0P/01-dajngo/PAP2/paponline/usuarios/views.py
# Compiled at: 2018-02-01 13:51:23
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

def not_found_404(request):
    return render(request, 'not_found_404.html', {'not_found_404': 'not_found'})


@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    context = {'usuario': usuario}
    return render(request, 'privado.html', context)


def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            formulario = AuthenticationForm(request.POST)
            if formulario.is_valid:
                usuario = request.POST['username']
                clave = request.POST['password']
                acceso = authenticate(username=usuario, password=clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request, acceso)
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/login')
        else:
            formulario = AuthenticationForm()
        context = {'formulario': formulario}
        return render(request, 'usuarios/ingresar.html', context)


@login_required(login_url='/ingresar')
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


class cambiarContrasena(PasswordChangeView):
    template_name = 'usuarios/cambiarContrasena.html'