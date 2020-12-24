# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/management/commands/init_city_db.py
# Compiled at: 2017-12-04 05:13:13
__author__ = 'zhangyue'
import os, datetime, urllib2, json
from django.core.management.base import BaseCommand, CommandError
from bee_django_crm.utils import loadJson
from bee_django_crm.models import Province, City, District

class Command(BaseCommand):

    def handle(self, *args, **options):

        def init_db():
            json_data = loadJson('city')
            citylist = json_data['citylist']
            print len(citylist).__str__() + '个省'
            for data in citylist:
                province = data['p']
                p = save_province(province)
                city_list = data['c']
                for city_data in city_list:
                    city = city_data['n']
                    c = save_city(p, city)
                    if city_data.has_key('a'):
                        district_list = city_data['a']
                        for district_data in district_list:
                            district = district_data['s']
                            save_district(c, district)

        def save_province(province):
            p = Province()
            p.name = province
            p.save()
            return p

        def save_city(p, city):
            c = City()
            c.province = p
            c.name = city
            c.save()
            return c

        def save_district(c, district):
            d = District()
            d.city = c
            d.name = district
            d.save()

        p_list = Province.objects.all()
        if p_list.count() == 0:
            init_db()