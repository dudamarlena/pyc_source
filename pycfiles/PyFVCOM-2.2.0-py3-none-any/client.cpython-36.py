# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/receptor/client.py
# Compiled at: 2020-01-01 13:17:50
# Size of source mod 2**32: 1400 bytes
__doc__ = '\nAdministra las respuestas recibidas del BCCR, para ponerlo en funcionamiento se debe crear una aplicación web,\npor ejemplo en django y agrear lo siguiente en urls.py\n\n.. code:: python\n\n    from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE\n    from soapfish.django_ import django_dispatcher\n    dispatcher = django_dispatcher(ResultadoDeSolicitudSoap_SERVICE)\n\n    urlpatterns = [\n         ...\n    url(r\'^wcfv2\\/Bccr\\.Sinpe\\.Fva\\.EntidadDePruebas\\.Notificador\\/ResultadoDeSolicitud\\.asmx$\', \n    dispatcher, name="receptor_fva"),\n    ]\n    \n'
from pyfva import logger

def reciba_notificacion(data):
    """
    Recibe la notificación del BCCR

    :params data: Es un diccionario con los siguientes atributos

        * **id_solicitud:**  Id de la solicitud del BCCR
        * **documento:** Documento firmado
        * **fue_exitosa:** si fue exitosa la firma
        * **codigo_error:** código de error

    No requiere retornar nada

    """
    logger.debug({'message':'Receptor: reciba notificación',  'data':data, 
     'location':__file__})


def valide_servicio():
    """
    Valida el si el servicio está disponible

    :returns:
        True si el servicio está disponible, 
        False si no lo está
    """
    dev = True
    logger.debug({'message':'Receptor: reciba notificación',  'data':dev,  'location':__file__})
    return dev