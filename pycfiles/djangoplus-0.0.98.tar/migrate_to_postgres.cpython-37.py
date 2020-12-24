# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/migrate_to_postgres.py
# Compiled at: 2019-02-17 16:38:38
# Size of source mod 2**32: 1815 bytes
import os, psycopg2, sqlite3
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        dbinfo = settings.DATABASES.get('postgres')
        username, password = dbinfo['USER'], dbinfo['PASSWORD']
        conn = psycopg2.connect('user={} password={}'.format(username, password))
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute('{} {};'.format('drop database if exists', settings.PROJECT_NAME))
        cur.execute('{} {};'.format('create database', settings.PROJECT_NAME))
        cur.close()
        conn.close()
        call_command('migrate', database='postgres', ignore_sync_permissions=True)
        conn = sqlite3.connect('sqlite.db')
        cur = conn.cursor()
        cur.execute('update admin_user set permission_mapping = "{}";')
        conn.commit()
        conn.close()
        conn = psycopg2.connect('dbname={} user={} password={}'.format(settings.PROJECT_NAME, username, password))
        cur = conn.cursor()
        cur.execute('delete from django_content_type;')
        conn.commit()
        conn.close()
        with open('/tmp/output.json', 'w+') as (f):
            call_command('dumpdata', database='sqlite', stdout=f)
            f.close()
        call_command('loaddata', '/tmp/output.json', database='postgres')
        os.unlink('/tmp/output.json')