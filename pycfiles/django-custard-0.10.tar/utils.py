# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/custard/custard/utils.py
# Compiled at: 2015-01-26 05:03:43
from __future__ import unicode_literals
from django.utils import importlib

def import_class(name):
    components = name.split(b'.')
    mod = importlib.import_module(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod