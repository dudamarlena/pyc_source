# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erwin/Django/iprir/iprir/management/commands/loadTLD.py
# Compiled at: 2015-06-18 12:03:05
# Size of source mod 2**32: 1870 bytes
"""loadTLD.py 01/2015

   custom django-admin command for importing:
   http://datahub.io/nl/dataset/iso-3166-1-alpha-2-country-codes
   https://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands

   python manage.py loadISO3166"""
import urllib.parse, urllib.request
from django.core.management.base import BaseCommand
from iprir.models import tld

class Command(BaseCommand):

    def handle(self, *args, **options):
        teller = 0
        try:
            try:
                stream = urllib.request.urlopen('https://raw.github.com/pudo/lobbytransparency/master/etl/countrycodes.csv')
                csvdata = str(stream.read(), 'utf-8')
                for csvLine in csvdata.split('\r\n'):
                    if csvLine:
                        if csvLine[0] == '"':
                            csvLine = csvLine[csvLine.rindex('"') + 1:]
                    try:
                        _, _, _, tmp_iso3, tmp_iso2, _, tmp_isonum, tmp_country, _ = csvLine.split(',', 8)
                        if len(tmp_iso2) == 2:
                            if len(tmp_iso3) == 3 and tmp_isonum.isdigit():
                                tmp_iso2 = tmp_iso2.lower()
                                tmp_country = tmp_country.title()
                                try:
                                    try:
                                        Tld = tld.objects.get(domain=tmp_iso2)
                                    except tld.DoesNotExist:
                                        Tld = tld(domain=tmp_iso2, type='country-code')

                                finally:
                                    Tld.description = tmp_country
                                    Tld.save()
                                    teller += 1

                    except ValueError:
                        pass

            except IOError as err:
                print('Error=' + str(err))

        finally:
            print(str(teller) + ' records touched')