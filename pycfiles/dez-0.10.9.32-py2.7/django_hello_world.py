# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/django_hello_world.py
# Compiled at: 2015-11-19 18:49:54
import os, sys
from dez.http.application import HTTPApplication
import django.core.handlers.wsgi
sys.path.insert(0, '/home/mario/stuff/__orbited/demos/python')

def main(**kwargs):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangochat.settings'
    application = django.core.handlers.wsgi.WSGIHandler()
    server = HTTPApplication('', kwargs['port'])
    server.add_wsgi_rule('/', application)
    server.start()