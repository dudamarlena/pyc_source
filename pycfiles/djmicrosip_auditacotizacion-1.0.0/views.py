# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_auditacotizacion\djmicrosip_auditacotizacion\views.py
# Compiled at: 2017-10-02 14:39:59
from .forms import *
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
from django.db import router, connections
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView
from microsip_api.comun.comun_functions import get_short_folio, split_letranumero, get_long_folio
from microsip_api.comun.sic_db import first_or_none
import csv, json

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_auditacotizacion/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def audita_view(request, template_name='djmicrosip_auditacotizacion/auditoria.html'):
    monedas = Moneda.objects.all()
    dls = first_or_none(Moneda.objects.filter(es_moneda_local='N'))
    tipo_cambio = 1
    listas_precios = PrecioEmpresa.objects.all()
    DetalleFormset = CotizacionFormset(VentasDocumentoDetalleForm, extra=1, can_delete=True, can_order=False)
    formset = DetalleFormset(request.POST or None)
    context = {'formset': formset, 
       'monedas': monedas, 
       'tipo_cambio_dls': tipo_cambio, 
       'listas_precios': listas_precios}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def GetArticulobyClave(request):
    clave = request.GET['clave']
    articulo_id = None
    articulo_nombre = None
    articulo_clave = ArticuloClave.objects.filter(clave=clave)
    if articulo_clave:
        articulo_id = articulo_clave[0].articulo.id
        articulo_nombre = articulo_clave[0].articulo.nombre
    data = {'articulo_id': articulo_id, 
       'articulo_nombre': articulo_nombre}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def CreaDocumento(request):
    ya_surtido = 0
    existe = 0
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    documento_folio = None
    lista = json.loads(request.GET['lista'])
    moneda = Moneda.objects.get(es_moneda_local='S')
    folio_pedido = request.GET['folio_pedido']
    serie, num = split_letranumero(folio_pedido)
    folio = get_long_folio(serie.upper(), num)
    pedido = first_or_none(VentasDocumento.objects.filter(folio=folio, tipo='P'))
    if pedido:
        existe = 1
        if pedido.estado == 'P':
            cliente = pedido.cliente
            cliente_direccion = first_or_none(ClienteDireccion.objects.filter(cliente=cliente))
            almacen = pedido.almacen
            condicion_pago = pedido.condicion_pago
            vendedor = pedido.vendedor
            cliente_clave = first_or_none(ClienteClave.objects.filter(cliente=cliente))
            documento = VentasDocumento(tipo='R', subtipo='N', fecha=datetime.now(), folio='', cliente=cliente, cliente_clave=cliente_clave, cliente_direccion=cliente_direccion, direccion_consignatario=cliente_direccion, almacen=almacen, descuento_tipo='P', descuento_importe=0, descuento_porcentaje=0, estado='P', aplicado='S', moneda=moneda, tipo_cambio=1, condicion_pago=condicion_pago, vendedor=vendedor, modalidad_facturacion=None, sistema_origen='VE', creacion_usuario=request.user.username)
            documento.save()
            documento_folio = documento.folio
            for detalle in lista:
                articulo_id = int(detalle[0])
                articulo = Articulo.objects.get(id=articulo_id)
                precio_con_impuesto = 0
                precio_empresa = first_or_none(PrecioEmpresa.objects.filter(id=43))
                articulo_precio = first_or_none(ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa=precio_empresa))
                if articulo_precio:
                    precio = articulo_precio.precio
                    moneda_id = articulo_precio.moneda.id
                    es_moneda_local = articulo_precio.moneda.es_moneda_local
                    precio_con_impuesto = GetPrecioVentaArticulo(articulo, precio_empresa.id)[1]
                unidades = float(detalle[1])
                articulo = Articulo.objects.get(id=articulo_id)
                articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
                if settings.MICROSIP_VERSION < 2017:
                    query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'Q')"
                else:
                    query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N','P','N')"
                c.execute(query, [articulo.id, precio_con_impuesto])
                precio_sin_impuesto = c.fetchall()[0][0]
                c.close()
                detalle_doc = VentasDocumentoDetalle.objects.create(id=-1, documento=documento, articulo_clave=articulo_clave, articulo=articulo, unidades=unidades, precio_unitario=precio_sin_impuesto, descuento_porcentaje=0, precio_total_neto=0, posicion=-1)

            liga = VentasDocumentoLiga.objects.create(id=-1, devolucion=documento, factura=pedido)
            liga = first_or_none(VentasDocumentoLiga.objects.filter(devolucion=documento, factura=pedido))
            detalles_remision = VentasDocumentoDetalle.objects.filter(documento=documento)
            for detalle_remision in detalles_remision:
                detalle_pedido = first_or_none(VentasDocumentoDetalle.objects.filter(documento=pedido, articulo=detalle_remision.articulo))
                c.execute(' insert into doctos_ve_ligas_det values(%s,%s,%s);' % (liga.id, detalle_pedido.id, detalle_remision.id))

            c.execute(' EXECUTE PROCEDURE APLICA_DOCTO_VE(%s);' % documento.id)
            c.execute("execute procedure calc_totales_docto_ve(%s,'N')" % documento.id)
            management.call_command('syncdb', database=using, interactive=False)
        else:
            ya_surtido = 1
    data = {'documento_folio': documento_folio, 'surtido': ya_surtido, 
       'existe': existe}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def GetPrecioVentaArticulo(articulo, precio_empresa_id):
    precio_con_impuesto = 0
    precio_sin_impuesto = 0
    try:
        articuloprecio = ArticuloPrecio.objects.get(articulo__id=articulo.id, precio_empresa__id=precio_empresa_id)
    except Exception as e:
        moneda = Moneda.objects.get(es_moneda_local='S')
        precio_sin_impuesto = 0
        tipo_cambio = 1
    else:
        precio_sin_impuesto = articuloprecio.precio
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        if settings.MICROSIP_VERSION < 2017:
            query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'P')"
        else:
            query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N','P','N')"
        c.execute(query, [articulo.id, precio_sin_impuesto])
        precio_con_impuesto = c.fetchall()[0][0]
        c.close()

    return (precio_sin_impuesto, precio_con_impuesto)