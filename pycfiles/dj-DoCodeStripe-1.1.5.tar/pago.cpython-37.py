# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\pagos\DoCodeStripe\procesos\pago.py
# Compiled at: 2020-04-17 13:53:13
# Size of source mod 2**32: 1773 bytes
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def definir_pago(tituloPago, descr, cantidad, logo):
    msj = 'Pago Definido Correctamente (url): '
    contexto = {}
    try:
        cantidad_final = cantidad * 100
        logo_final = 'img/shop.jpg'
        if logo != None:
            logo_final = logo
        contexto = {'tituloPago':tituloPago, 
         'descripcion':descr + '($' + str(cantidad) + '.00 MXN)', 
         'key':settings.STRIPE_PUBLISHABLE_KEY, 
         'cantidad':cantidad, 
         'cantidad_final':cantidad_final, 
         'logo':logo_final, 
         'msj':msj}
    except Exception as e:
        try:
            contexto['msj'] = str(e)
        finally:
            e = None
            del e

    return contexto


def realizar_pago(request, precio, desc):
    resultPay = {'titulo':'Pagos', 
     'charge':'', 
     'nombre':'', 
     'cantidad':'', 
     'pagado':False, 
     'recibo':'', 
     'error':''}
    try:
        if request.method == 'POST':
            charge = stripe.Charge.create(amount=(precio * 100),
              currency='mxn',
              description=desc,
              source=(request.POST['stripeToken']))
            resultPay['charge'] = charge
            resultPay['nombre'] = charge.source.name
            resultPay['cantidad'] = charge.amount / 100
            resultPay['pagado'] = charge.paid
            resultPay['recibo'] = charge.receipt_url
    except Exception as e:
        try:
            resultPay['error'] = str(e)
        finally:
            e = None
            del e

    return resultPay