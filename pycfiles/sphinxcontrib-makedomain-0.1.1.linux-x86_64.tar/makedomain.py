# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sphinxcontrib/makedomain.py
# Compiled at: 2013-10-21 18:26:35
"""
    makedomain
    ~~~~~~~~~~

    A GNU Make domain.

    This domain provides `make:target`, `make:var` and `make:expvar`
    directives and roles.

    :copyright: 2012 by Kay-Uwe (Kiwi) Lorenz, ModuleWorks GmbH
    :license: BSD, see LICENSE for details.
"""
__version__ = '0.1.1'
release = __version__
version = release.rsplit('.', 1)[0]
from sphinxcontrib.domaintools import custom_domain
import re

def setup(app):
    app.add_domain(custom_domain('GnuMakeDomain', name='make', label='GNU Make', elements=dict(target=dict(objname='Make Target', indextemplate='pair: %s; Make Target'), var=dict(objname='Make Variable', indextemplate='pair: %s; Make Variable'), expvar=dict(objname='Make Variable, exported', indextemplate='pair: %s; Make Variable, exported'))))