# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-licyilu1/django-cbr/cbr/management/commands/load_cbr.py
# Compiled at: 2017-08-28 23:32:16
# Size of source mod 2**32: 1837 bytes
import requests, xml.dom.minidom as minidom
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from cbr.models import CBRCurrency, CBRCurrencyRate

class Command(BaseCommand):

    def load_cbr(self):
        url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        resp = requests.get(url)
        doc = minidom.parseString(resp.content.decode('cp1251'))
        valcurs = doc.getElementsByTagName('ValCurs')[0]
        date_rate = valcurs.attributes.get('Date').value
        date_rate = datetime.strptime(date_rate, '%d.%m.%Y')
        valutes = doc.getElementsByTagName('Valute')
        for v in valutes:
            code = v.attributes.get('ID').value
            num_code = v.getElementsByTagName('NumCode')[0].childNodes[0].data
            char_code = v.getElementsByTagName('CharCode')[0].childNodes[0].data
            nominal = v.getElementsByTagName('Nominal')[0].childNodes[0].data
            name = v.getElementsByTagName('Name')[0].childNodes[0].data
            rate = v.getElementsByTagName('Value')[0].childNodes[0].data
            nominal = int(nominal)
            rate = Decimal(rate.replace(',', '.'))
            currency, created = CBRCurrency.objects.get_or_create(code=code, defaults={'name': name, 'num_code': num_code, 'char_code': char_code})
            try:
                change = CBRCurrencyRate.objects.filter(currency=currency).last().rate - rate
            except AttributeError:
                change = 0

            course, created = CBRCurrencyRate.objects.get_or_create(currency=currency, date_rate=date_rate, defaults={'nominal': nominal, 'rate': rate, 'change': change})

    def handle(self, *args, **options):
        self.load_cbr()