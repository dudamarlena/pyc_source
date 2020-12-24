# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneContentTemplates/Extensions/Install.py
# Compiled at: 2012-01-17 08:01:40
from Products.Archetypes.Extensions.utils import install_subskin
from Products.PloneContentTemplates.config import GLOBALS
from cStringIO import StringIO

def install(self):
    out = StringIO()
    install_subskin(self, out, GLOBALS)
    out.write('Installed skin')
    return out.getvalue()