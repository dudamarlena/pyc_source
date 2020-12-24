# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\config\views.py
# Compiled at: 2020-04-09 11:54:37
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import management
from microsip_api.comun.sic_db import first_or_none
from .forms import *

@login_required(login_url='/login/')
def conexiones_View(request, template_name='config/conexiones/conexiones.html'):
    """ Lista de conexiones a carpetas ( Microsip Datos ). """
    c = {'conexiones': ConexionDB.objects.all()}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def conexion_manageView(request, id=None, template_name='config/conexiones/conexion.html'):
    """ Lista de conexiones """
    message = ''
    initial_form = None
    if id:
        conexion = get_object_or_404(ConexionDB, pk=id)
    else:
        conexion = ConexionDB()
        initial_form = {'nombre': 'local', 
           'tipo': 'L', 
           'servidor': 'localhost', 
           'carpeta_datos': 'C:\\Microsip datos', 
           'usuario': 'SYSDBA'}
    form = ConexionManageForm(request.POST or None, instance=conexion, initial=initial_form)
    if form.is_valid():
        grupo = form.save()
        return HttpResponseRedirect('/conexiones/')
    else:
        c = {'form': form}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def delete_conexion(request, id=None):
    """ Lista de conexiones """
    conexion = ConexionDB.objects.get(pk=id)
    conexion.delete()
    return HttpResponseRedirect('/conexiones/')


@login_required(login_url='/login/')
def select_db(request, template_name='config/select_db.html'):
    """ Para seleccionar base de datos con la que se desea trabjar """
    form = SelectDBForm(request.POST or None, usuario=request.user, conexion_activa=request.session['conexion_activa'])
    message = ''
    conexion_activa = request.session['conexion_activa']
    if form.is_valid():
        conexion = form.cleaned_data['conexion'].replace(' ', '_')
        request.session['selected_database'] = conexion
        return HttpResponseRedirect('/')
        call_command('runserver')
    else:
        request.session['selected_database'] = ''
    c = {'form': form, 'message': message}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def ingresar(request):
    """ logea un usuario """
    message = ''
    formulario = CustomAuthenticationForm(request.POST or None)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if formulario.is_valid():
            usuario = authenticate(username=request.POST['username'], password=request.POST['password'])
            if usuario.is_active:
                login(request, usuario)
                conexion_db = request.POST['conexion_db']
                request.session['conexion_activa'] = ''
                if conexion_db != '':
                    request.session['conexion_activa'] = int(conexion_db)
                basedatos = first_or_none(DatabaseSucursal.objects.filter(name='clasificadores'))
                if basedatos and usuario.last_name == 'clasificadores':
                    conexion = basedatos.empresa_conexion.replace(' ', '_')
                    request.session['selected_database'] = conexion
                    return HttpResponseRedirect('/')
                return HttpResponseRedirect('/select_db/')
            else:
                return render_to_response('noactivo.html', context_instance=RequestContext(request))
        return render_to_response('config/login.html', {'form': formulario, 'message': message}, context_instance=RequestContext(request))


def logoutUser(request):
    """ Deslogea un usuario """
    try:
        del request.session['selected_database']
        del request.session['conexion_activa']
    except KeyError:
        pass

    logout(request)
    return HttpResponseRedirect('/')