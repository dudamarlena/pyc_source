# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\Bodegon\DoCodeDB\procesos\correo_sendGrid.py
# Compiled at: 2020-03-04 17:25:28
# Size of source mod 2**32: 2061 bytes
from django.core.mail import send_mail
from DoCodeDB.models import Tsendgrid
from django.template import loader
from django.conf import settings

def enviar_correo(origen, correo_enviar, cc, info, template):
    result = {'estatus':False, 
     'msj':''}
    if settings.ENVIAR_CORREO:
        try:
            api_key = Tsendgrid.objects.all().first()
            settings.SENDGRID_API_KEY = api_key.key
            context = {}
            context.update(info)
            html_message = loader.render_to_string(template, context)
            send_mail('Registro',
              'Body',
              origen,
              [
             correo_enviar],
              fail_silently=False,
              html_message=html_message)
            if cc != None:
                send_mail('Formulario de Contacto', '', origen, cc, fail_silently=False, html_message=html_message)
            result['estatus'] = True
            result['msj'] = 'Correo Enviado'
            return result
        except Exception as e:
            try:
                result['estatus'] = False
                result['msj'] = str(e)
                return result
            finally:
                e = None
                del e

    else:
        result['estatus'] = False
        result['msj'] = 'No se envio correo: ENVIAR_CORREO = False'
        return result