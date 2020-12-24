# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/__init__.py
# Compiled at: 2012-10-06 02:43:50
"""
RDFlib Store implementation for Django, providing lots of extra goodies.

Use this application by just including it in your INSTALLED_APPS. After this,
you can create a new Graph using:

>>> import rdflib
>>> g = rdflib.Graph('Django')

"""
from rdflib.plugin import register
from rdflib.store import Store
register('Django', Store, 'rdflib_django.store', 'DjangoStore')