# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_facturacion\djmicrosip_facturacion\views.py
# Compiled at: 2017-09-29 12:19:19
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView
from microsip_api.apps.cfdi.certificador.core import CertificadorSAT, create_ini_file_33_pv, create_ini_file, save_xml_in_document_33_pv, save_xml_in_document
from microsip_api.comun.comun_functions import split_letranumero, get_long_folio
from microsip_api.comun.sic_db import first_or_none
import csv, datetime, json, os
from django.core.mail import send_mail, EmailMessage
from django.core.files import File
from django.core.mail.backends.smtp import EmailBackend
from django.contrib.staticfiles.templatetags.staticfiles import static
import shutil

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_facturacion/index.html'):
    cliente = None
    titulo = 'Inicio'
    form = RFCSearchForm(request.POST or None)
    if form.is_valid():
        rfc = form.cleaned_data['rfc']
        cliente = ClienteDireccion.objects.get(rfc_curp=rfc).cliente
        titulo = 'Facturacion | %s' % cliente.nombre
    context = {'form': form, 
       'cliente': cliente, 
       'titulo': titulo}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def facturar(request, id, template_name='djmicrosip_facturacion/facturar.html'):
    using = router.db_for_write(PuntoVentaDocumento)
    c = connections[using].cursor()
    cliente = Cliente.objects.get(id=id)
    total = 0
    documento = None
    form = FacturarForm(request.POST or None)
    if form.is_valid():
        ticket = form.cleaned_data['folio_ticket'].capitalize()
        folio, serie = split_letranumero(ticket)
        folio_largo = get_long_folio(folio, serie)
        documento = PuntoVentaDocumento.objects.filter(folio=folio_largo, tipo='V')[0]
        c.execute("select coalesce(total_a_pagar,0) from calc_totales_docto_pv(%s,'%s','%s',null)" % (documento.id, 'S', 'D'))
        total = c.fetchall()[0][0]
    context = {'form': form, 'cliente': cliente, 
       'documento': documento, 
       'total': total}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def FacturaTicket(request):
    errors = None
    num_tickets = 0
    factura_id = None
    ini_file_path = ''
    url = ''
    ticket_id = request.GET['ticket_id']
    cliente_id = request.GET['cliente_id']
    mail_destino = request.GET['mail_destino']
    cliente = Cliente.objects.get(id=cliente_id)
    direccion = first_or_none(ClienteDireccion.objects.filter(cliente=cliente, es_ppal='S'))
    ticket = PuntoVentaDocumento.objects.get(id=ticket_id)
    envio_por_correo = 0
    using = router.db_for_write(PuntoVentaDocumento)
    c = connections[using].cursor()
    c.execute("select coalesce(folio,'%s') from get_folio_factura_pv(%s,'%s') ;" % ('xx', ticket.id, 'F'))
    factura = c.fetchall()[0][0]
    if factura.strip() != 'xx':
        errors = 'El ticket ya ha sido facturado.'
    else:
        query = "select lugar_expedicion_id from lugares_expedicion where es_ppal='S'"
        c.execute(query)
        lugar_expedicion_id = c.fetchall()[0][0]
        factura = PuntoVentaDocumento.objects.create(id=-1, caja=ticket.caja, cajero=ticket.cajero, cliente=cliente, cliente_fac=cliente, direccion_cliente=direccion, moneda=ticket.moneda, tipo='F', folio='', fecha=datetime.datetime.now(), hora=datetime.datetime.now().strftime('%H:%M:%S'), clave_cliente=ticket.clave_cliente, clave_cliente_fac=ticket.clave_cliente_fac, tipo_cambio=ticket.tipo_cambio, estado='N', aplicado='S', importe_neto=0, total_impuestos=0, importe_donativo=0, total_fpgc=0, sistema_origen='PV', descripcion=ticket.descripcion, es_cfd='S', modalidad_facturacion='CFDI', lugar_expedicion=lugar_expedicion_id)
        c.execute('EXECUTE PROCEDURE GET_REPORTE_ID')
        reporte_id = c.fetchall()[0][0]
        BookmarkReporte.objects.create_manual(using=using, reporte_id=reporte_id, objeto_id=ticket.id, fecha=datetime.datetime.now())
        c = connections[using].cursor()
        query = "EXECUTE PROCEDURE COPIA_TICKETS_A_FAC_PV('L',null," + str(factura.id) + ",'C'," + str(reporte_id) + ')'
        c.execute(query)
        num_tickets = c.fetchall()[0][0]
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
        factura_id = factura.id
        carpeta_facturacion_sat = 'C:\\SAT\\'
        certificador_sat = CertificadorSAT(carpeta_facturacion_sat, modo=settings.MODO_SERVIDOR)
        datos_empresa = Registry.objects.using(using).get(nombre='DatosEmpresa')
        datos_empresa = Registry.objects.using(using).filter(padre=datos_empresa)
        rfc = datos_empresa.get(nombre='Rfc').get_value().replace('-', '').replace(' ', '')
        create_ini_file_33_pv(factura.id, carpeta_facturacion_sat, using)
        ini_file_path = '%s\\facturas\\\\%s.ini' % (carpeta_facturacion_sat, factura.folio)
        errors = certificador_sat.certificar_33(ini_file_path=ini_file_path, rfc=rfc)
        if not errors:
            save_xml_in_document_33_pv(ini_file_path, using, factura.id)
            destinos = []
            if direccion.email != '' and direccion.email != None:
                destinos.append(direccion.email)
            if mail_destino != '':
                destinos.append(mail_destino)
                envio_por_correo = enviar_factura(ini_file_path, destinos)
        url = mostrar_factura('%s.pdf' % ini_file_path)
    datos = {'factura_id': factura_id, 
       'errors': errors, 
       'num_tickets': num_tickets, 
       'envio_por_correo': envio_por_correo, 
       'archivo': '%s.pdf' % ini_file_path, 
       'url': url}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')


def enviar_factura(ini_file_path, destinos):
    fpdf = open('%s.pdf' % ini_file_path)
    fxml = open('%s.xml' % ini_file_path)
    pdf = File(fpdf)
    xml = File(fxml)
    backend = EmailBackend(host='smtp.live.com', port=587, username='sic1318@hotmail.com', password='adminSIC123', use_tls=True)
    mail = EmailMessage('Factura', 'Le enviamos su Factura Electronica', 'sic1318@hotmail.com', destinos, connection=backend)
    mail.attach_file('%s.pdf' % ini_file_path)
    mail.attach_file('%s.xml' % ini_file_path)
    x = mail.send()
    return x


def mostrar_factura(archivo_ruta):
    file_name = archivo_ruta.split('\\')[(-1)]
    app_dir = os.path.dirname(__file__)
    static_dir = os.path.join(settings.PDF, 'facturas')
    facturas_path = os.path.join(app_dir, 'static', 'djmicrosip_facturacion', 'facturas')
    new_file_path1 = os.path.join(static_dir, file_name)
    shutil.copyfile(archivo_ruta, new_file_path1)
    new_file_path2 = os.path.join(facturas_path, file_name)
    shutil.copyfile(archivo_ruta, new_file_path2)
    url = static('djmicrosip_facturacion/facturas/%s' % file_name)
    return url