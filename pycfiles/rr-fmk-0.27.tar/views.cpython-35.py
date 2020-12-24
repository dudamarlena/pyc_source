# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/_P/02-django/PAP/pap/usuarios/views.py
# Compiled at: 2017-12-07 13:51:33
# Size of source mod 2**32: 2064 bytes
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


def ingresar--- This code section failed: ---

 L.  23         0  LOAD_FAST                'request'
                3  LOAD_ATTR                user
                6  LOAD_ATTR                is_anonymous
                9  CALL_FUNCTION_0       0  '0 positional, 0 named'
               12  POP_JUMP_IF_TRUE     25  'to 25'

 L.  25        15  LOAD_GLOBAL              HttpResponseRedirect
               18  LOAD_STR                 '/'
               21  CALL_FUNCTION_1       1  '1 positional, 0 named'
               24  RETURN_END_IF    
             25_0  COME_FROM            12  '12'

 L.  26        25  LOAD_FAST                'request'
               28  LOAD_ATTR                method
               31  LOAD_STR                 'POST'
               34  COMPARE_OP               ==
               37  POP_JUMP_IF_FALSE   171  'to 171'

 L.  27        40  LOAD_GLOBAL              AuthenticationForm
               43  LOAD_FAST                'request'
               46  LOAD_ATTR                POST
               49  CALL_FUNCTION_1       1  '1 positional, 0 named'
               52  STORE_FAST               'formulario'

 L.  28        55  LOAD_FAST                'formulario'
               58  LOAD_ATTR                is_valid
               61  POP_JUMP_IF_FALSE   180  'to 180'

 L.  29        64  LOAD_FAST                'request'
               67  LOAD_ATTR                POST
               70  LOAD_STR                 'username'
               73  BINARY_SUBSCR    
               74  STORE_FAST               'usuario'

 L.  30        77  LOAD_FAST                'request'
               80  LOAD_ATTR                POST
               83  LOAD_STR                 'password'
               86  BINARY_SUBSCR    
               87  STORE_FAST               'clave'

 L.  31        90  LOAD_GLOBAL              authenticate
               93  LOAD_STR                 'username'
               96  LOAD_FAST                'usuario'
               99  LOAD_STR                 'password'
              102  LOAD_FAST                'clave'
              105  CALL_FUNCTION_512   512  '0 positional, 2 named'
              108  STORE_FAST               'acceso'

 L.  32       111  LOAD_FAST                'acceso'
              114  LOAD_CONST               None
              117  COMPARE_OP               is-not
              120  POP_JUMP_IF_FALSE   158  'to 158'

 L.  33       123  LOAD_FAST                'acceso'
              126  LOAD_ATTR                is_active
              129  POP_JUMP_IF_FALSE   168  'to 168'

 L.  34       132  LOAD_GLOBAL              login
              135  LOAD_FAST                'request'
              138  LOAD_FAST                'acceso'
              141  CALL_FUNCTION_2       2  '2 positional, 0 named'
              144  POP_TOP          

 L.  35       145  LOAD_GLOBAL              HttpResponseRedirect
              148  LOAD_STR                 '/'
              151  CALL_FUNCTION_1       1  '1 positional, 0 named'
              154  RETURN_VALUE     
            155_0  COME_FROM           129  '129'
              155  JUMP_ABSOLUTE       180  'to 180'
              158  ELSE                     '168'

 L.  40       158  LOAD_GLOBAL              HttpResponseRedirect
              161  LOAD_STR                 '/login'
              164  CALL_FUNCTION_1       1  '1 positional, 0 named'
              167  RETURN_END_IF    
            168_0  COME_FROM            61  '61'
              168  JUMP_FORWARD        180  'to 180'
              171  ELSE                     '180'

 L.  42       171  LOAD_GLOBAL              AuthenticationForm
              174  CALL_FUNCTION_0       0  '0 positional, 0 named'
              177  STORE_FAST               'formulario'
            180_0  COME_FROM           168  '168'

 L.  43       180  LOAD_STR                 'formulario'
              183  LOAD_FAST                'formulario'
              186  BUILD_MAP_1           1 
              189  STORE_FAST               'context'

 L.  44       192  LOAD_GLOBAL              render
              195  LOAD_FAST                'request'
              198  LOAD_STR                 'usuarios/ingresar.html'
              201  LOAD_FAST                'context'
              204  CALL_FUNCTION_3       3  '3 positional, 0 named'
              207  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 168


@login_required(login_url='/ingresar')
def salir(request):
    logout(request)
    return HttpResponseRedirect('/')


class cambiarContrasena(PasswordChangeView):
    template_name = 'usuarios/cambiarContrasena.html'