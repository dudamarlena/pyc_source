# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/rr/usuarios/views.py
# Compiled at: 2018-04-05 10:40:45
# Size of source mod 2**32: 6938 bytes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from rr.usuarios.forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

class UseNativoMixin(AccessMixin):
    __doc__ = 'Verifica que el usuario no sea de Google.'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])
        print(user.username)
        if user.username == user.email:
            return render(request, 'registration/password_reset_not_possible.html')
        else:
            return (super().dispatch)(request, *args, **kwargs)


class Reiniciar_pass(PasswordResetView):
    success_url = reverse_lazy('login:password_reset_done')


class Reiniciar_pass_ConfirmView(UseNativoMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('usuarios:password_reset_complete')


@login_required(login_url='/login')
def change_password(request):
    print(request.user.__dict__)
    if request.user.email == request.user.username:
        print('volvemoss')
        return render(request, 'usuarios/user_google.html')
    else:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada correctamente!')
                return redirect('login:change_password')
            messages.error(request, 'Por favor corrija los siguientes errores')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'usuarios/change_password.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta de ' + current_site.domain
            message = render_to_string('account_activation_email.html', {'user':user, 
             'domain':current_site.domain, 
             'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(), 
             'token':account_activation_token.make_token(user)})
            user.email_user(subject, message)
            return redirect('usuarios:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.cliente.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'usuarios/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'usuarios/mail_enviado.html')


def not_found_404(request):
    return render(request, 'not_found_404.html', {'not_found_404': 'not_found'})


@login_required(login_url='/login')
def privado(request):
    usuario = request.user
    context = {'usuario': usuario}
    return render(request, 'privado.html', context)


def loginGoogle(request):
    usuario = request.POST['U3']
    email = request.POST['U3']
    clave = request.POST['Eea']
    acceso = authenticate(username=usuario, password=clave)
    print(acceso)
    if acceso is not None:
        login(request, acceso)
        return JsonResponse({'login': 'ok'})
    try:
        user = User.objects.create_user(username=usuario, first_name=(request.POST['ofa']),
          last_name=(request.POST['wea']),
          email=email,
          password=clave)
        loginGoogle(request)
        return JsonResponse({'login': 'ok'})
    except Exception as identifier:
        print('error')


def ingresar(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            formulario = AuthenticationForm(request.POST)
            if formulario.is_valid:
                if request.POST['username'] == 'google':
                    return loginGoogle(request)
        elif formulario.is_valid:
            print('por oto ladoo')
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


@login_required(login_url='/login')
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


def google(request):
    return HttpResponse('google')