# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erwin/Django/iprir/iprir/management/commands/loadISO3166.py
# Compiled at: 2015-02-05 15:51:25
# Size of source mod 2**32: 2845 bytes
"""loadISO3166.py 01/2015

   custom django-admin command for importing:
   http://datahub.io/nl/dataset/iso-3166-1-alpha-2-country-codes
   https://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands

   python manage.py loadISO3166"""
import urllib.parse, urllib.request
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from iprir.models import Country

class Command(BaseCommand):

    def handle(self, *args, **options):
        Tl = 0
        try:
            stream = urllib.request.urlopen('https://raw.github.com/pudo/lobbytransparency/master/etl/countrycodes.csv')
            csvdata = str(stream.read(), 'utf-8')
            for theLink in range(0, 2):
                for csvLine in csvdata.split('\r\n'):
                    if csvLine:
                        if csvLine[0] == '"':
                            csvLine = csvLine[csvLine.rindex('"') + 1:]
                    try:
                        tmp_euname, tmp_modified, tmp_linked_to_country, tmp_iso3, tmp_iso2, tmp_grc, tmp_isonum, tmp_country, tmp_imperitive = csvLine.split(',', 8)
                        if len(tmp_iso2) == 2:
                            if len(tmp_iso3) == 3:
                                if tmp_isonum.isdigit() and (theLink == 0 or tmp_linked_to_country):
                                    pass
                        tmp_iso2 = tmp_iso2.upper()
                        tmp_iso3 = tmp_iso3.upper()
                        tmp_country = tmp_country.title()
                        tmp_linked_to_country = tmp_linked_to_country.strip().title()
                        try:
                            try:
                                c = Country.objects.get(iso2=tmp_iso2)
                            except Country.DoesNotExist:
                                c = Country(iso2=tmp_iso2, active=True)

                        finally:
                            c.iso3 = tmp_iso3
                            c.isonum = int(tmp_isonum)
                            c.description = tmp_country
                            Tl += 1
                            c.save()

                        if tmp_linked_to_country != '':
                            try:
                                linkedc = Country.objects.get(description=tmp_linked_to_country)
                                if linkedc.pk:
                                    c.mainCountry_id = linkedc.pk
                                    c.save()
                            except:
                                pass

                    except ValueError:
                        pass

                print(theLink)

        except IOError as err:
            print('Error=' + str(err))