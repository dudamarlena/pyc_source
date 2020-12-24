# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dodi/envs/isdc/isdc_modules/isdc_geodb/geodb/migrations/userfunctions_migration.py
# Compiled at: 2018-09-02 23:51:50
"""
custom migration file for database functions
add this file to dependencies list in first migration file (0001_xxxxx)
ex:
    dependencies = [
        ('geodb', 'userfunctions_migration'),
    ]
"""
from __future__ import unicode_literals
from django.db import migrations, models
from pprint import pprint
import django.contrib.gis.db.models.fields, os
curpath = os.path.dirname(os.path.abspath(__file__))

def getsql_userfunctions_create():
    with open(os.path.join(curpath, b'userfunctions_create.sql'), b'r') as (f):
        return f.read()


def getsql_userfunctions_drop():
    with open(os.path.join(curpath, b'userfunctions_drop.sql'), b'r') as (f):
        return f.read()


class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.RunSQL(getsql_userfunctions_create(), reverse_sql=getsql_userfunctions_drop())]