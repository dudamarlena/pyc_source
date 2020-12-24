# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nik/PycharmProjects/VTIXPaymentAssist/vtixy_payment_assist/management/commands/payorder.py
# Compiled at: 2015-04-11 16:30:36
from django.conf import settings
from django.core.management import BaseCommand, CommandError
import slumber
from slumber.exceptions import HttpClientError

class Command(BaseCommand):
    args = '<order_id>'
    help = 'Pay order by ID'
    can_import_settings = True

    def handle(self, *args, **options):
        try:
            order_id = args[0]
        except IndexError:
            raise CommandError('Need one argument')

        api = slumber.API(settings.VTIXY_HOST + '/', auth=(settings.VTIXY_LOGIN, settings.VTIXY_PASSWORD))
        try:
            order = api.orders(order_id).get()
        except HttpClientError as e:
            raise CommandError(e.args[0])

        self.stdout.write('Got order "%s". Price: %s' % (order_id, order['price']))
        if order['sold']:
            raise CommandError('Order "%s" already payed' % order['id'])
        try:
            api.orders(order_id).patch({'sold': True, 'transaction_id': '0000000000'})
        except HttpClientError as e:
            raise CommandError(e.args[0])

        self.stdout.write('Order payed')
        if hasattr(settings, 'VTIXY_LOYALTY'):
            loyalty_name = order['loyalty_name']
            loyalty_card = order['loyalty_card']
            if loyalty_name is not None:
                for loyalty_program in settings.VTIXY_LOYALTY:
                    if loyalty_name == loyalty_program[0]:
                        price = float(order['price'])
                        model = __import__(loyalty_program[1], globals(), locals(), ['models'], -1).models.Order
                        model.objects.create(number=order_id, amount=price, card=loyalty_card, state=model.STATE_CLOSED)
                    self.stdout.write('Loyalty "%s" informed' % loyalty_program[1])

        self.stdout.write('Done')
        return