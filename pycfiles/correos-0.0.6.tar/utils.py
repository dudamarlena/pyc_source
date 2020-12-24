# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/resteve/virtualenv/nan38mifarma/python-correos/correos/utils.py
# Compiled at: 2018-03-16 06:03:46


def correos_url(debug=False):
    """
    Correos URL connection

    :param debug: If set to true, use Envialia test URL
    """
    if debug:
        return 'https://preregistroenviospre.correos.es/preregistroenvios'
    else:
        return 'https://preregistroenvios.correos.es/preregistroenvios'


def services():
    services = {'S0030': 'PAQUETE POSTAL PRIORITARIO (I)', 
       'S0033': 'POSTAL EXPRES (N)', 
       'S0034': 'POSTAL EXPRES (I)', 
       'S0198': 'POSTAL EXPRES LISTA', 
       'S0132': 'PAQ 72 DOMICILIO', 
       'S0133': 'PAQ 72 OFICINA', 
       'S0135': 'LOGISTICA INVERSA CON ENVIO ASOCIADO', 
       'S0148': 'LOGISTICA INVERSA DE RETORNO', 
       'S0235': 'PAQ 48 ENTREGA A DOMICILIO', 
       'S0236': 'PAQ 48 EN OFICINA', 
       'S0197': 'PAQ 48 (LOGISTICA INVERSA)', 
       'S0031': 'PAQUETE POSTAL ECONOMICO (I)', 
       'S0175': 'PAQ 48 ENTREGA EN HOMEPAQ', 
       'S0176': 'PAQ 48 ENTREGA EN CITYPAQ', 
       'S0177': 'PAQ 72 ENTREGA EN HOMEPAQ', 
       'S0178': 'PAQ 72 ENTREGA EN CITYPAQ'}
    return services


DELIVERY_OFICINA = {'S0236': 'LS', 
   'S0133': 'LS'}
CASHONDELIVERY_SERVICES = [
 'S0132', 'S0235']