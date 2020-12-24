# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/z3tinymce/zcml.py
# Compiled at: 2012-04-18 09:01:42
from zope.component.zcml import handler
from interfaces import IZ3TinyMCEConfig
from zope.interface import implements

class Z3TinyMCEConfig(object):
    implements(IZ3TinyMCEConfig)
    path = ''

    def __init__(self, path):
        self.path = path

    def getPath(self):
        return self.path


def registerZ3TinyMCEConfig(context, path, port, maxConnections):
    context.action(discriminator=('RegisterOpenOfficeConfig', path), callable=handler, args=(
     'registerUtility',
     Z3TinyMCEConfig(path),
     Iz3TinyMCEConfig))