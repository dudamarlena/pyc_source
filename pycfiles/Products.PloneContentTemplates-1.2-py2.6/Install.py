# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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