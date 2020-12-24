# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\views.py
# Compiled at: 2016-11-15 11:36:48
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from microsip_api.comun.sic_db import get_conecctionname, first_or_none
from django.db import connections, router
from custom_db.procedures import procedures as sql_procedures
from django.core import management
import datetime, winsound, json
from .models import *
from .forms import *
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

@login_required(login_url='/login/')
def play_sound(request):
    access = request.GET['access']
    if access == '1':
        winsound.Beep(2500, 500)
    elif access == '0':
        for x in xrange(0, 3):
            winsound.Beep(300, 400)

    data = {'access': access}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def cliente_search(request, template_name='django_msp_controldeacceso/search.html'):
    access = True
    anticipation_message = ''
    clave = ''
    cliente = None
    empresa_nombre = str(Registry.objects.get(nombre='SIC_Controldeacceso_NombreEmpresa').valor)
    form = ClienteClaveSearchForm(request.POST or None)
    fecha_vencimiento = None
    fecha_ultimo_cargo = None
    many_enters = False
    maxima = None
    msg = ''
    vencido = False
    msg_saldo = ''
    msg_fecha = ''
    msg_fecha_vencimiento = ''
    enters = 0
    if form.is_valid():
        clave = form.cleaned_data['clave']
        try:
            cliente = ClienteClave.objects.get(clave=clave).cliente
        except Exception as e:
            access = False
            msg = 'No se encontro ningun CLIENTE con la clave %s.' % clave
        else:
            cliente_id = cliente.id
            using = router.db_for_write(Cliente)
            con = connections[using]
            c = con.cursor()
            c.execute('select b.dias_plazo from  clientes c left join condiciones_pago a\n                        on c.cond_pago_id = a.cond_pago_id left join plazos_cond_pag b on a.cond_pago_id = b.cond_pago_id\n                         where c.cliente_id = %s' % cliente_id)
            registro = c.fetchall()
            if registro:
                dias_plazo = registro[0][0]
            c.execute("select fecha_vencimiento,atraso,saldo_cargo,docto_cc_id from cargos_cliente(%s,'NOW','NOW','S','N');" % cliente.id)
            cargo = c.fetchall()
            if cargo:
                reg = max(cargo)
                fecha_vencimiento = reg[0]
                atraso = reg[1]
                c.execute("select saldo_fin_cxc from orsp_cl_aux_cli(%s,'01/01/2000',current_date,'N','N')" % cliente_id)
                saldo = c.fetchall()[0][0]
                docto_cc_id = reg[3]
                c.execute('select fecha from doctos_cc where docto_cc_id = %s;' % docto_cc_id)
                fecha_ultimo_cargo = c.fetchall()[0][0]
                msg_fecha = 'El ultimo cargo se generó con fecha: %s' % fecha_ultimo_cargo.strftime('%d/%b/%Y')
                msg_fecha_vencimiento = 'Se vence: %s' % fecha_vencimiento.strftime('%d/%b/%Y')
                if saldo > 0:
                    msg_saldo = 'Su cuenta no ha sido saldada completamente. Restan $%s' % saldo
                actual = datetime.datetime.now().date()
                if fecha_vencimiento < actual and atraso > 0:
                    vencido = True
                    msg_fecha_vencimiento = 'VENCIDO EL DIA: %s' % fecha_vencimiento.strftime('%d/%b/%Y')
            else:
                msg_fecha = 'No se han encontrado Cargos de este cliente'
                vencido = True
            c.execute('Select * from sic_registro_accesos where fecha= current_date and cliente =%s' % cliente_id)
            result = c.fetchall()
            if result:
                enters = len(result) + 1
                many_enters = True
                access = False
            if access:
                ins_access = 'S'
            else:
                ins_access = 'N'
            ins_date = datetime.date.today().strftime('%Y-%m-%d')
            ins_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            RegistroAcceso.objects.create(cliente=cliente_id, acceso=ins_access, fecha=ins_date, hora=ins_time)
            c.close()

    imagenes = ImagenSlide.objects.all()[0:5]
    context = {'form': form, 'cliente': cliente, 
       'msg': msg, 
       'access': access, 
       'clave': clave, 
       'empresa_nombre': empresa_nombre, 'anticipation_message': anticipation_message, 
       'many_enters': many_enters, 
       'enters': enters, 
       'imagenes': imagenes, 
       'range': range(len(imagenes)), 
       'vencido': vencido, 
       'msg_fecha_vencimiento': msg_fecha_vencimiento, 
       'msg_fecha': msg_fecha, 
       'msg_saldo': msg_saldo}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request, template_name='django_msp_controldeacceso/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    parent = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
    if request.user.is_superuser and parent:
        if not Registry.objects.filter(nombre='SIC_Controldeacceso_NombreEmpresa').exists():
            Registry.objects.create(nombre='SIC_Controldeacceso_NombreEmpresa', tipo='V', padre=parent, valor='')
        using = router.db_for_write(Cliente)
        c = connections[using].cursor()
        c.execute(sql_procedures['SIC_CLIENTES_ACCESO'])
        c.execute('EXECUTE PROCEDURE SIC_CLIENTES_ACCESO;')
        c.execute('DROP PROCEDURE SIC_CLIENTES_ACCESO;')
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/acceso/preferencias')


class ClienteListView(ListView):
    context_object_name = 'clientes'
    model = Cliente
    template_name = 'django_msp_controldeacceso/clientes.html'
    paginate_by = 15

    def get_queryset(self):
        return Cliente.objects.all().order_by('nombre')


@login_required(login_url='/login/')
def ClienteManageView(request, id=None, template_name='django_msp_controldeacceso/cliente.html'):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.POST:
        form = ClienteManageForm(request.POST or None, request.FILES, instance=cliente)
    else:
        form = ClienteManageForm(instance=cliente)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/acceso/clientes/')
    else:
        c = {'form': form, 'cliente_nombre': cliente.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def PreferenciasManageView(request, template_name='django_msp_controldeacceso/preferences.html'):
    form_initial = {'enterprise_name': Registry.objects.get(nombre='SIC_Controldeacceso_NombreEmpresa').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=form_initial)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def log_view(request, template_name='django_msp_controldeacceso/log.html'):
    context = {}
    result = []
    cliente = None
    tipo = 0
    titulo = None
    form = LogSearch(request.POST or None)
    if form.is_valid():
        fecha = form.cleaned_data['fecha']
        cliente = form.cleaned_data['cliente']
        if not fecha and cliente:
            result = list(RegistroAcceso.objects.filter(cliente=cliente.id).order_by('fecha').values_list('acceso', 'fecha', 'hora'))
            titulo = cliente.nombre
            tipo = 1
        if fecha and not cliente:
            result = list(RegistroAcceso.objects.filter(fecha=fecha).order_by('fecha').values_list('cliente', 'acceso', 'hora'))
            result_temp = []
            for r in result:
                c_nombre = Cliente.objects.get(id=r[0]).nombre
                r += (c_nombre,)
                result_temp.append(r)

            result = result_temp
            titulo = fecha.strftime('%d de %b de %Y')
            tipo = 2
        if fecha and cliente:
            result = list(RegistroAcceso.objects.filter(fecha=fecha, cliente=cliente.id).order_by('fecha').values_list('acceso', 'hora'))
            titulo = cliente.nombre + ' con fecha ' + fecha.strftime('%d-%b-%Y')
            tipo = 3
    contexto = {'form': form, 'result': result, 
       'n_res': len(result), 
       'titulo': titulo, 
       'tipo': tipo}
    return render_to_response(template_name, contexto, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ImagenManageView(request, id=None, template_name='django_msp_controldeacceso/imagen.html'):
    if id:
        imagen = get_object_or_404(ImagenSlide, pk=id)
    else:
        imagen = ImagenSlide()
    if request.POST:
        form = ImagenManageForm(request.POST or None, request.FILES, instance=imagen)
    else:
        form = ImagenManageForm(instance=imagen)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/acceso/imagenes/')
    else:
        c = {'form': form}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


class ImagenListView(ListView):
    context_object_name = 'imagenes'
    model = ImagenSlide
    template_name = 'django_msp_controldeacceso/imagenes.html'
    paginate_by = 15

    def get_queryset(self):
        return ImagenSlide.objects.all().order_by('id')


def eliminarimagen(request, id=None):
    data = {}
    id_a = id
    imagen_a_eliminar = ImagenSlide.objects.get(id=id_a)
    imagen_a_eliminar.delete()
    return HttpResponseRedirect('/acceso/imagenes/')