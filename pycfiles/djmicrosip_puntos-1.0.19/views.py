# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_puntos\djmicrosip_puntos\views.py
# Compiled at: 2015-08-19 12:25:55
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q, Sum
from .forms import *
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from microsip_api.comun.sic_db import get_conecctionname, first_or_none, next_id
from django.db import connections
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from monthdelta import monthdelta
from datetime import date, timedelta
from django.contrib.auth.decorators import user_passes_test

def get_vigencia(cliente_id):
    fecha_actual = date.today()
    fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
    cliente = Cliente.objects.get(pk=cliente_id)
    vigencia_inicio_periodo = cliente.vigencia_fecha_inicio
    vigencia_fin_periodo = cliente.vigencia_fecha_fin
    vigencia_frecuencia = None
    if not vigencia_inicio_periodo:
        vigencia_inicio_periodo = Registry.objects.get(nombre='SIC_Puntos_VigenciaInicioPeriodoFecha').get_value()
        vigencia_fin_periodo = Registry.objects.get(nombre='SIC_Puntos_VigenciaFinPeriodoFecha').valor or ''
        vigencia_frecuencia_tipo = Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuenciaTipo').get_value()
        vigencia_frecuencia = Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuencia').valor or ''
        vigencia_inicio_periodo = datetime.strptime(vigencia_inicio_periodo or fecha_actual_str, '%Y-%m-%d').date()
        vigencia_fin_periodo = datetime.strptime(vigencia_fin_periodo or fecha_actual_str, '%Y-%m-%d').date()
    vigencia_inicio = vigencia_inicio_periodo
    vigencia_fin = vigencia_fin_periodo
    if vigencia_frecuencia:
        contador = 1
        ciclo = True
        while ciclo:
            a_sumar = contador * int(vigencia_frecuencia)
            if vigencia_frecuencia_tipo == 'M':
                fecha_temporal = vigencia_inicio_periodo + monthdelta(a_sumar)
            elif vigencia_frecuencia_tipo == 'D':
                fecha_temporal = vigencia_inicio_periodo + timedelta(days=a_sumar)
            elif vigencia_frecuencia_tipo == 'S':
                fecha_temporal = vigencia_inicio_periodo + timedelta(weeks=a_sumar)
            elif vigencia_frecuencia_tipo == 'A':
                fecha_temporal = vigencia_inicio_periodo + timedelta(days=a_sumar * 365)
            if fecha_temporal <= fecha_actual:
                vigencia_inicio = fecha_temporal
            else:
                vigencia_fin = fecha_temporal
                ciclo = False
            contador += 1

        if vigencia_fin > vigencia_fin_periodo:
            vigencia_fin = vigencia_fin_periodo
            if vigencia_inicio > vigencia_fin_periodo:
                vigencia_inicio = vigencia_fin_periodo + timedelta(days=1)
    if not vigencia_fin:
        vigencia_fin = fecha_actual
    return (
     vigencia_inicio, vigencia_fin)


def get_fecha_de_corte(cliente_id):
    fecha_corte = Cliente.objects.get(pk=cliente_id).fecha_corte
    if fecha_corte:
        return fecha_corte
    corte_dia = Registry.objects.get(nombre='SIC_PUNTOS_CORTE_DIA').get_value()
    corte_mes = Registry.objects.get(nombre='SIC_PUNTOS_CORTE_MES').get_value()
    corte_anio = Registry.objects.get(nombre='SIC_PUNTOS_CORTE_ANIO').get_value()
    if corte_dia and corte_dia != '0' and corte_dia != '':
        corte_dia = int(corte_dia)
    if (not corte_mes or corte_mes == '0' or corte_mes == '') and (not corte_anio or corte_anio == '0' or corte_anio == '') and corte_dia > datetime.now().day:
        corte_dia = datetime.now().day
    if not corte_mes or corte_mes == '0' or corte_mes == '':
        corte_mes = datetime.now().month
    if not corte_anio or corte_anio == '0' or corte_anio == '':
        corte_anio = datetime.now().year
    dias_de_mes = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 30, '9': 30, '10': 31, '11': 30, '12': 31}
    if int(corte_anio) % 4 == 0:
        dias_de_mes['2'] = 29
    else:
        dias_de_mes['2'] = 28
    if corte_dia > dias_de_mes[str(corte_mes)]:
        corte_dia = dias_de_mes[str(corte_mes)]
    return datetime.strptime('%s%s%s' % (corte_dia, corte_mes, corte_anio), '%d%m%Y').date()


@login_required(login_url='/login/')
def cliente_searchView(request, template_name='djmicrosip_puntos/clientes/cliente_search.html'):
    message = ''
    cliente = Cliente()
    dinero_en_puntos = 0
    total_puntos = 0
    total_dinero_electronico = 0
    if request.method == 'POST':
        form = ClienteClaveSearchForm(request.POST)
        if form.is_valid():
            try:
                cliente = ClienteClave.objects.get(clave=form.cleaned_data['cliente']).cliente
                fecha_inicio, fecha_fin = get_vigencia(cliente.id)
                ventas = PuntoVentaDocumento.objects.filter(fecha__lte=fecha_fin, fecha__gte=fecha_inicio, tipo='V', cliente_tarjeta=cliente).filter(Q(estado='N') | Q(estado='D')).aggregate(total_puntos=Sum('puntos'), total_dinero_elect=Sum('dinero_electronico'), total_dinero_descontar=Sum('dinero_a_descontar'))
                sql = "\n                    select sum(sic_puntos_pago), sum(sic_dinero_electronico_pago) from doctos_pv dpv\n                    join claves_clientes cc on cc.clave_cliente = dpv.clave_cliente\n                    where\n                        dpv.fecha <= '%s' and\n                        dpv.fecha >= '%s' and\n                        dpv.tipo_docto = 'V' and (dpv.estatus = 'N' or dpv.estatus = 'D' ) and\n                        cc.cliente_id = %s\n                " % (fecha_fin, fecha_inicio, cliente.id)
                using = router.db_for_write(ClienteClave)
                c = connections[using].cursor()
                c.execute(sql)
                ventas_pagos = c.fetchall()
                ventas['total_puntos_pago'] = ventas_pagos[0][0]
                ventas['total_dinero_electronico_pago'] = ventas_pagos[0][1]
                c.close()
                ventas['total_puntos'] = ventas['total_puntos'] or 0
                ventas['total_puntos_pago'] = ventas['total_puntos_pago'] or 0
                ventas['total_dinero_elect'] = ventas['total_dinero_elect'] or 0
                ventas['total_dinero_electronico_pago'] = ventas['total_dinero_electronico_pago'] or 0
                ventas['total_dinero_descontar'] = ventas['total_dinero_descontar'] or 0
                ventas_puntos = ventas['total_puntos'] - ventas['total_puntos_pago']
                ventas_dinero_electronico = ventas['total_dinero_elect'] - ventas['total_dinero_electronico_pago'] - ventas['total_dinero_descontar']
                devoluciones = PuntoVentaDocumento.objects.filter(fecha__lte=fecha_fin, fecha__gte=fecha_inicio, tipo='D', estado='N', cliente_tarjeta=cliente).aggregate(total_puntos=Sum('puntos'), total_dinero_electronico=Sum('dinero_electronico'))
                devoluciones['total_puntos'] = devoluciones['total_puntos'] or 0
                devoluciones['total_dinero_electronico'] = devoluciones['total_dinero_electronico'] or 0
                total_puntos = ventas_puntos - devoluciones['total_puntos']
                total_dinero_electronico = ventas_dinero_electronico - devoluciones['total_dinero_electronico']
                valor_puntos = cliente.valor_puntos or 0
                if cliente.hereda_valorpuntos and cliente.tipo_cliente and cliente.tipo_tarjeta == 'P':
                    valor_puntos = cliente.tipo_cliente.valor_puntos
                dinero_en_puntos = valor_puntos * total_puntos
            except ObjectDoesNotExist:
                cliente = Cliente()
                message = 'No se encontro un cliente con esta clave, intentalo de nuevo.'

    else:
        form = ClienteClaveSearchForm()
    c = {'form': form, 'cliente': cliente, 'total_puntos': total_puntos, 'total_dinero_electronico': total_dinero_electronico, 'message': message, 'dinero_en_puntos': dinero_en_puntos}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


class InitialConfiguration(object):

    def __init__(self, using):
        self.errors = []
        self.using = using

    def is_valid(self):
        from custom_db.core import sql_queries
        self.errors = []
        valid = True
        try:
            Registry.objects.get(nombre='SIC_PUNTOS_ARTICULO_PUNTOS_PREDET').get_value()
        except ObjectDoesNotExist:
            self.errors.append('Por favor inicializa la configuracion de la aplicacion dando  <a href="/puntos/preferencias/actualizar_tablas/">click aqui</a>')
        else:
            from_lleno = False
            try:
                from_lleno = Registry.objects.get(nombre='SIC_PUNTOS_CONFIG_FROM_LLENO').get_value() == '1'
            except ObjectDoesNotExist:
                self.errors.append('Por favor inicializa la configuracion de la aplicacion dando  <a href="/puntos/preferencias/actualizar_tablas/">click aqui</a>')

        if not from_lleno:
            self.errors.append('Es nesesario configurar la aplicacion en [ Herramientas > Preferencias. ] ')
        else:
            caja = Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value()
            caja = Caja.objects.get(pk=caja)
            cajero = Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL').get_value()
            cajero = Cajero.objects.get(pk=cajero)
            if not cajero.operar_cajas == 'T' and not CajeroCaja.objects.filter(cajero=cajero, caja=caja).exists():
                self.errors.append('La caja [%s] no puede ser operada por el cajero [%s] por favor corrigelo en [ Herramientas > preferencias. ] ' % (caja, cajero))
            try:
                Impuesto.objects.filter(tipo_iva='3')[0]
            except ObjectDoesNotExist:
                self.errors.append('Define almenos un impuesto al 0%')

        c = connections[self.using].cursor()
        c.execute(sql_queries.triggers_exist)
        triggers_en_db = c.fetchall()
        triggers_activos = False
        if len(triggers_en_db) == 2:
            triggers_activos = True
        c.close()
        if not triggers_activos:
            self.errors.append('El enlace de puntos con microsip no esta activo, Si se realizan ventas en microsip estas no afectaran los puntos o dinero electronico de los clientes.')
        if not self.errors == []:
            valid = False
        return valid


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_puntos/index.html'):
    using = get_conecctionname(request.session)
    initial_configuration = InitialConfiguration(using)
    c = {}
    if not initial_configuration.is_valid():
        c['errors'] = initial_configuration.errors
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/login/')
def InicializarPuntosArticulosView(request, template_name='djmicrosip_puntos/herramientas/inicializar_puntos.html'):
    if request.user.is_superuser:
        form = InicializarPuntosArticulosForm(request.POST or None)
        if form.is_valid():
            Articulo.objects.update(puntos=None, dinero_electronico=None, hereda_puntos=1)
            LineaArticulos.objects.update(puntos=None, dinero_electronico=None, hereda_puntos=1)
            GrupoLineas.objects.update(puntos=None, dinero_electronico=None)
            return HttpResponseRedirect('/puntos/articulos/')
        c = {'form': form}
    else:
        return HttpResponseRedirect('/puntos/articulos/')
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def articulo_manageview(request, id=None, template_name='djmicrosip_puntos/articulos/articulo.html'):
    """ Modificacion de puntos de un articulo """
    articulo = get_object_or_404(Articulo, pk=id)
    form = articulos_form(request.POST or None, instance=articulo)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/puntos/articulos/')
    else:
        c = {'form': form, 'articulo_nombre': articulo.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


class ArticuloListView(ListView):
    context_object_name = 'articulos'
    model = Articulo
    template_name = 'djmicrosip_puntos/articulos/articulos.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ArticuloListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        form = ArticuloSearchForm(self.request.GET)
        if form.is_valid():
            articulo = form.cleaned_data['articulo']
            nombre = form.cleaned_data['nombre']
            clave = form.cleaned_data['clave']
            articulos = Articulo.objects.all()
            if nombre:
                articulos = articulos.filter(nombre__contains=nombre)
            if clave:
                claves = ArticuloClave.objects.filter(clave=clave)
                if claves:
                    articulos = Articulo.objects.filter(pk=claves[0].articulo.id)
            if articulo:
                articulos = Articulo.objects.filter(pk=articulo.id)
        return articulos.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(ArticuloListView, self).get_context_data(**kwargs)
        context['form'] = ArticuloSearchForm(self.request.GET or None)
        return context


class LineaArticulosListView(ListView):
    context_object_name = 'lineas'
    model = LineaArticulos
    template_name = 'djmicrosip_puntos/articulos/lineas.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(LineaArticulosListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return LineaArticulos.objects.all().order_by('nombre')


class GrupoLineasListView(ListView):
    context_object_name = 'grupos'
    model = GrupoLineas
    template_name = 'djmicrosip_puntos/articulos/grupos.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(GrupoLineasListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return GrupoLineas.objects.all().order_by('nombre')


class ClienteListView(ListView):
    context_object_name = 'clientes'
    model = Cliente
    template_name = 'djmicrosip_puntos/clientes/clientes.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ClienteListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        form = ClienteSearchForm(self.request.GET)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            nombre = form.cleaned_data['nombre']
            clave = form.cleaned_data['clave']
            clientes = Cliente.objects.all()
            if nombre:
                clientes = clientes.filter(nombre__contains=nombre)
            if clave:
                claves = ClienteClave.objects.filter(clave=clave)
                if claves:
                    clientes = Cliente.objects.filter(pk=claves[0].cliente.id)
            if cliente:
                clientes = Cliente.objects.filter(pk=cliente.id)
        return clientes.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(ClienteListView, self).get_context_data(**kwargs)
        context['form'] = ClienteSearchForm(self.request.GET or None)
        return context


class ClienteTipoListView(ListView):
    context_object_name = 'tipos_cliente'
    model = ClienteTipo
    template_name = 'djmicrosip_puntos/clientes/tipos_clientes/tipos_cliente.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ClienteTipoListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return ClienteTipo.objects.all().order_by('nombre')


@login_required(login_url='/login/')
def LineaArticulosManageView(request, id=None, template_name='djmicrosip_puntos/articulos/linea.html'):
    """ Modificacion de puntos de un lineas """
    linea = get_object_or_404(LineaArticulos, pk=id)
    form = LineaArticulosForm(request.POST or None, instance=linea)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/puntos/lineas/')
    else:
        c = {'form': form, 'linea_nombre': linea.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def GrupoLineasManageView(request, id=None, template_name='djmicrosip_puntos/articulos/grupo.html'):
    """ Modificacion de puntos de un lineas """
    grupo = get_object_or_404(GrupoLineas, pk=id)
    form = GrupoLineasForm(request.POST or None, instance=grupo)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/puntos/grupos/')
    else:
        c = {'form': form, 'grupo_nombre': grupo.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ClienteManageView(request, id=None, template_name='djmicrosip_puntos/clientes/cliente.html'):
    """ Modificacion de puntos de un cliente """
    cliente = get_object_or_404(Cliente, pk=id)
    form = ClienteManageForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/puntos/clientes/')
    else:
        tipo_cliente = cliente.tipo_cliente or ''
        c = {'form': form, 'cliente_nombre': cliente.nombre, 'tipo_cliente': tipo_cliente}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ClienteTipoManageView(request, id=None, template_name='djmicrosip_puntos/clientes/tipos_clientes/tipo_cliente.html'):
    """ Modificacion de puntos de un cliente """
    cliente_tipo = get_object_or_404(ClienteTipo, pk=id)
    form = ClienteTipoForm(request.POST or None, instance=cliente_tipo)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/puntos/tipos_cliente/')
    else:
        c = {'form': form, 'cliente_tipo_nombre': cliente_tipo.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def if0ToNone(value):
    if value == '0':
        return None
    else:
        return value


@login_required(login_url='/login/')
def PreferenciasManageView(request, template_name='djmicrosip_puntos/herramientas/preferencias.html'):
    from custom_db.core import sql_queries
    msg = ''
    connection_name = get_conecctionname(request.session)
    c = connections[connection_name].cursor()
    c.execute(sql_queries.triggers_exist)
    triggers_en_db = c.fetchall()
    triggers_activos = False
    if len(triggers_en_db) == 2:
        triggers_activos = True
    c.close()
    puntos_initial = {'vigencia_inicio_periodo': Registry.objects.get(nombre='SIC_Puntos_VigenciaInicioPeriodoFecha').get_value(), 
       'vigencia_fin_periodo': Registry.objects.get(nombre='SIC_Puntos_VigenciaFinPeriodoFecha').valor or '', 
       'vigencia_frecuencia_tipo': Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuenciaTipo').get_value(), 
       'vigencia_frecuencia': Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuencia').valor or '', 
       'triggers_activos': triggers_activos, 
       'articulo_puntos': Registry.objects.get(nombre='SIC_PUNTOS_ARTICULO_PUNTOS_PREDET').get_value(), 
       'articulo_dinero_electronico': Registry.objects.get(nombre='SIC_PUNTOS_ARTICULO_DINERO_ELECT_PREDET').get_value(), 
       'caja_general': Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value(), 
       'cajero_general': Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL').get_value(), 
       'condicion_de_pago_contado': Registry.objects.get(nombre='SIC_CONDICION_PAGO_CONTADO').get_value(), 
       'cliente_eventual_pv': if0ToNone(Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').get_value()), 
       'articulo_general': if0ToNone(Registry.objects.get(nombre='ARTICULO_VENTAS_FG_PV_ID').get_value()), 
       'precio_con_impuestos': Registry.objects.get(nombre='SIC_Puntos_PrecioConImpuestos').get_value() == '1', 
       'porcentaje_menos_credito': Registry.objects.get(nombre='SIC_Puntos_PorcentajeMenosCredito').get_value() or 0, 
       'dar_dinero_alpagar': Registry.objects.get(nombre='SIC_Puntos_DarDineroEnPagos').get_value() == '1', 
       'limite_gastarporventa': Registry.objects.get(nombre='SIC_Puntos_LimiteAGastarPorVenta').get_value()}
    form = PreferenciasPuntosManageForm(request.POST or None, initial=puntos_initial)
    warrning = ''
    if form.is_valid():
        formulario_valido = Registry.objects.get(nombre='SIC_PUNTOS_CONFIG_FROM_LLENO')
        formulario_valido.valor = 1
        formulario_valido.save()
        enlace_activo = form.cleaned_data['triggers_activos']
        form.save(using=connection_name)
        msg = 'Datos guardados correctamente'
        if not enlace_activo:
            warrning = 'El enlace con microsip no esta activo si se realizan ventas en microsip estas no afectaran sus puntos o dinero electronico'
    c = {'form': form, 'msg': msg, 'warrning': warrning}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def generaVenta(cliente, puntos=0, dinero_electronico=0, aplicar_documento=True):
    cajero = Cajero.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL').get_value())
    caja = Caja.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value())
    clave_cliente = first_or_none(ClienteClave.objects.filter(cliente=cliente))
    cliente_clave = ''
    if clave_cliente:
        cliente_clave = clave_cliente.clave
    documento = PuntoVentaDocumento.objects.create(id=-1, caja=caja, cajero=cajero, cliente=cliente, almacen=caja.almacen, moneda=cliente.moneda, tipo='V', fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), clave_cliente=cliente_clave, tipo_cambio=1, aplicado='N', importe_neto=0.01, total_impuestos=0, importe_donativo=0, total_fpgc=0, descripcion='PARA APLICAR PUNTOSDINERO EXTRA', usuario_creador=cajero.usuario, fechahora_creacion=datetime.now(), puntos=puntos, dinero_electronico=dinero_electronico, cliente_tarjeta=cliente)
    articulo = Articulo.objects.get(pk=Registry.objects.get(nombre='ARTICULO_VENTAS_FG_PV_ID').get_value())
    PuntoVentaDocumentoDetalle.objects.create(id=-1, documento_pv=documento, articulo=articulo, unidades=1, unidades_dev=0, precio_unitario=0.01, precio_unitario_impto=0.0116, fpgc_unitario=0, porcentaje_descuento=0, precio_total_neto=0.01, porcentaje_comis=0, rol='N', posicion=1, puntos=puntos, dinero_electronico=dinero_electronico)
    PuntoVentaCobro.objects.create(id=-1, tipo='C', documento_pv=documento, forma_cobro=caja.predeterminado_forma_cobro, importe=0.01, tipo_cambio=1, importe_mon_doc=0.01)
    using = router.db_for_write(Cliente)
    impuesto_al_0 = Impuesto.objects.filter(tipo_iva='3')[0]
    c = connections[using].cursor()
    query = 'INSERT INTO impuestos_doctos_pv (docto_pv_id, impuesto_id, venta_neta, otros_impuestos, pctje_impuesto, importe_impuesto)         VALUES (%s, %s, 0.01, 0, 0, 0)'
    c.execute(query, [documento.id, int(impuesto_al_0.id)])
    c.close()
    management.call_command('syncdb', database=using, interactive=False)
    if aplicar_documento == True:
        documento.aplicado = 'S'
        documento.save()
    return documento


@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def GenerarTarjetasView(request, template_name='djmicrosip_puntos/herramientas/generar_tarjetas.html'):
    msg = ''
    connection_name = get_conecctionname(request.session)
    initial_configuration = InitialConfiguration(connection_name)
    form = GenerarTarjetasForm(request.POST or None)
    if form.is_valid():
        iniciar_en = form.cleaned_data['iniciar_en']
        prefijo = form.cleaned_data['prefijo']
        cantidad = form.cleaned_data['cantidad']
        tipo_tarjeta = form.cleaned_data['tipo_tarjeta']
        puntos = form.cleaned_data['puntos']
        dinero_electronico = form.cleaned_data['dinero_electronico']
        valor_puntos = form.cleaned_data['valor_puntos']
        if tipo_tarjeta == 'D':
            valor_puntos = 0
        claves = []
        rolclaves = ClienteClaveRol.objects.get(es_ppal='S')
        moneda_local = Moneda.objects.get(es_moneda_local='S')
        condicion_pago = CondicionPago.objects.get(pk=Registry.objects.get(nombre='SIC_CONDICION_PAGO_CONTADO').get_value())
        tipo_cliente = ClienteTipo.objects.get(nombre='TARJETA PROMOCION')
        cajero = Cajero.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL').get_value())
        caja = Caja.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value())
        documentos = []
        CajaMovimiento.objects.create(id=-1, fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), movimiento_tipo='A', caja=caja, usuario_creador=cajero.usuario)
        for numero in range(iniciar_en, iniciar_en + cantidad):
            clave = '%s%s' % (prefijo, '%09d' % numero)
            cliente = Cliente.objects.create(id=next_id('ID_CATALOGOS', connection_name), nombre=clave, moneda=moneda_local, condicion_de_pago=condicion_pago, tipo_cliente=tipo_cliente, tipo_tarjeta=tipo_tarjeta, hereda_valorpuntos=None, valor_puntos=valor_puntos, hereda_puntos_a=None)
            ClienteClave.objects.create(id=-1, clave=clave, cliente=cliente, rol=rolclaves)
            if puntos > 0 or dinero_electronico > 0:
                documento = generaVenta(cliente=cliente, puntos=puntos, dinero_electronico=dinero_electronico)
                documentos.append(documento)

        management.call_command('syncdb', database=connection_name, interactive=False)
        CajaMovimiento.objects.create(id=-1, fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), movimiento_tipo='C', caja=caja, usuario_creador=cajero.usuario)
        msg = 'Clientes generados correctamente.'
        form = GenerarTarjetasForm()
    c = {'form': form, 'msg': msg}
    if not initial_configuration.is_valid():
        c['errors'] = initial_configuration.errors
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def TransferirDineroView(request, template_name='djmicrosip_puntos/herramientas/dar_puntosdinero.html'):
    msg = ''
    connection_name = get_conecctionname(request.session)
    initial_configuration = InitialConfiguration(connection_name)
    form = DarDineroForm(request.POST or None)
    if form.is_valid():
        dinero_electronico = form.cleaned_data['dinero_electronico']
        cliente = form.cleaned_data['cliente']
        cajero = Cajero.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL').get_value())
        caja = Caja.objects.get(pk=Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value())
        impuesto_al_0 = Impuesto.objects.filter(tipo_iva='3')[0]
        clave_cliente = first_or_none(ClienteClave.objects.filter(cliente=cliente))
        clave = ''
        if clave_cliente:
            clave = clave_cliente.clave
        documentos = []
        CajaMovimiento.objects.create(id=-1, fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), movimiento_tipo='A', caja=caja, usuario_creador=cajero.usuario)
        generaVenta(cliente=cliente, dinero_electronico=dinero_electronico)
        fecha_hora_cierre = datetime.now()
        CajaMovimiento.objects.create(id=-1, fecha=fecha_hora_cierre, hora=fecha_hora_cierre.strftime('%H:%M:%S'), movimiento_tipo='C', caja=caja, fechahora_creacion=fecha_hora_cierre, usuario_creador=cajero.usuario)
        msg = 'Transferencia correcta.'
        form = DarDineroForm()
    c = {'form': form, 'msg': msg}
    if not initial_configuration.is_valid():
        c['errors'] = initial_configuration.errors
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def DatetimeToDays(date1):
    temp = datetime(1899, 12, 30)
    delta = date1 - temp
    return float(delta.days) + float(delta.seconds) / 86400


def ExecuteProcedures(procedures_dic):
    for procedure in procedures_dic:
        using = router.db_for_write(Cliente)
        c = connections[using].cursor()
        c.execute(procedures_dic[procedure])
        c.execute('EXECUTE PROCEDURE %s;' % procedure)
        c.execute('DROP PROCEDURE %s;' % procedure)
        c.close()


def activar_triggers():
    from custom_db.core import sql_queries
    using = router.db_for_write(Cliente)
    c = connections[using].cursor()
    c.execute(sql_queries.triggers_exist)
    triggers_en_db = c.fetchall()
    triggers_activos = False
    if len(triggers_en_db) == 2:
        triggers_activos = True
    c.close()
    return triggers_activos


@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser)
def UpdateDatabaseTable(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    if request.user.is_superuser:
        using = router.db_for_write(Cliente)
        from custom_db.core import procedures as core_procedures
        from custom_db.punto_venta import procedures as pv_procedures
        ExecuteProcedures(core_procedures.procedures)
        ExecuteProcedures(pv_procedures.procedures)
        c = connections[using].cursor()
        for procedure in core_procedures.procedures_fijos:
            c.execute(procedure['procedure'])
            c.execute('GRANT EXECUTE ON PROCEDURE %s TO SYSDBA;' % procedure['name'])
            c.execute('GRANT EXECUTE ON PROCEDURE %s TO USUARIO_MICROSIP;' % procedure['name'])

        c.close()
        from custom_db.core import sql_queries as core_sql_queries
        c = connections[using].cursor()
        for exception_activate in core_sql_queries.exceptions_activate:
            c.execute(core_sql_queries.exceptions_activate[exception_activate])

        c.close()
        from custom_db.punto_venta import sql_queries as pv_sql_queries
        c = connections[using].cursor()
        for procedure in pv_procedures.procedures_fijos:
            c.execute(procedure['procedure'])
            c.execute('GRANT EXECUTE ON PROCEDURE %s TO SYSDBA;' % procedure['name'])
            c.execute('GRANT EXECUTE ON PROCEDURE %s TO USUARIO_MICROSIP;' % procedure['name'])

        c.close()
        if activar_triggers():
            c = connections[using].cursor()
            for trigger in pv_sql_queries.triggers_activate:
                c.execute(pv_sql_queries.triggers_activate[trigger])

            c.close()
        from microsip_api.apps.metadatos.models import ReportBulilderField
        ReportBulilderField.objects.create_simple(using=using, table_name='DOCTOS_PV', field_name='SIC_DINEROADESCONTAR', field_alias='SIC Dinero a descontar', datatype='dtDouble')
        ReportBulilderField.objects.create_simple(using=using, table_name='DOCTOS_PV', field_name='SIC_DINERO_ELECTRONICO', field_alias='SIC Dinero Electronico', datatype='dtDouble')
        ReportBulilderField.objects.create_simple(using=using, table_name='DOCTOS_PV', field_name='SIC_DINERO_ELECTRONICO_PAGO', field_alias='SIC Dinero Electronico Pago', datatype='dtDouble')
        ReportBulilderField.objects.create_simple(using=using, table_name='DOCTOS_PV', field_name='SIC_CLIENTE_TARJETA', field_alias='SIC Cliente Dinero Id', datatype='dtInteger')
        from microsip_api.apps.config.models import ReportBuilderItem, ReportBuilderFolder
        folder = ReportBuilderFolder.objects.get(pk=19)
        from custom_db.punto_venta import report_builder
        for report_key in report_builder.reports.keys():
            reporte = first_or_none(ReportBuilderItem.objects.filter(name=report_key, folder=folder))
            if reporte:
                reporte.template = report_builder.reports[report_key]
                reporte.save(update_fields=['template'])
            else:
                ReportBuilderItem.objects.create(id=-1, folder=folder, name=report_key, item_size=1, modified=DatetimeToDays(datetime.now()), template=report_builder.reports[report_key])

        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if padre:
            if not Registry.objects.filter(nombre='ARTICULO_VENTAS_FG_PV_ID').exists():
                Registry.objects.create(nombre='ARTICULO_VENTAS_FG_PV_ID', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='CLIENTE_EVENTUAL_PV_ID').exists():
                Registry.objects.create(nombre='CLIENTE_EVENTUAL_PV_ID', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_PUNTOS_CAJA_GRAL').exists():
                Registry.objects.create(nombre='SIC_PUNTOS_CAJA_GRAL', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_PUNTOS_CAJERO_GRAL').exists():
                Registry.objects.create(nombre='SIC_PUNTOS_CAJERO_GRAL', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_PUNTOS_CONFIG_FROM_LLENO').exists():
                Registry.objects.create(nombre='SIC_PUNTOS_CONFIG_FROM_LLENO', tipo='V', padre=padre, valor='0')
            if not Registry.objects.filter(nombre='SIC_CONDICION_PAGO_CONTADO').exists():
                Registry.objects.create(nombre='SIC_CONDICION_PAGO_CONTADO', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_Puntos_DarDineroEnPagos').exists():
                Registry.objects.create(nombre='SIC_Puntos_DarDineroEnPagos', tipo='V', padre=padre, valor='0')
            if not Registry.objects.filter(nombre='SIC_Puntos_LimiteAGastarPorVenta').exists():
                Registry.objects.create(nombre='SIC_Puntos_LimiteAGastarPorVenta', tipo='V', padre=padre, valor='100')
            if not Registry.objects.filter(nombre='SIC_Puntos_VigenciaInicioPeriodoFecha').exists():
                Registry.objects.create(nombre='SIC_Puntos_VigenciaInicioPeriodoFecha', tipo='V', padre=padre, valor=datetime.now())
            if not Registry.objects.filter(nombre='SIC_Puntos_VigenciaFinPeriodoFecha').exists():
                Registry.objects.create(nombre='SIC_Puntos_VigenciaFinPeriodoFecha', tipo='V', padre=padre)
            if not Registry.objects.filter(nombre='SIC_Puntos_VigenciaFrecuenciaTipo').exists():
                Registry.objects.create(nombre='SIC_Puntos_VigenciaFrecuenciaTipo', tipo='V', padre=padre)
            if not Registry.objects.filter(nombre='SIC_Puntos_VigenciaFrecuencia').exists():
                Registry.objects.create(nombre='SIC_Puntos_VigenciaFrecuencia', tipo='V', padre=padre)
            if not Registry.objects.filter(nombre='SIC_PUNTOS_ARTICULO_PUNTOS_PREDET').exists():
                Registry.objects.create(nombre='SIC_PUNTOS_ARTICULO_PUNTOS_PREDET', tipo='V', padre=padre, valor=0)
            if not Registry.objects.filter(nombre='SIC_PUNTOS_ARTICULO_DINERO_ELECT_PREDET').exists():
                Registry.objects.create(nombre='SIC_PUNTOS_ARTICULO_DINERO_ELECT_PREDET', tipo='V', padre=padre, valor=0)
            if not Registry.objects.filter(nombre='SIC_Puntos_PrecioConImpuestos').exists():
                Registry.objects.create(nombre='SIC_Puntos_PrecioConImpuestos', tipo='V', padre=padre, valor=1)
            if not Registry.objects.filter(nombre='SIC_Puntos_PorcentajeMenosCredito').exists():
                Registry.objects.create(nombre='SIC_Puntos_PorcentajeMenosCredito', tipo='V', padre=padre, valor=0)
        management.call_command('syncdb', database=using, interactive=False)
        try:
            ClienteTipo.objects.get(nombre='TARJETA PROMOCION')
        except ObjectDoesNotExist:
            ClienteTipo.objects.create(id=-1, nombre='TARJETA PROMOCION', valor_puntos=1)

    return HttpResponseRedirect('/puntos/')