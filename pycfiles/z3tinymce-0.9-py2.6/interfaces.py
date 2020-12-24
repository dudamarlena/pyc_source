# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/z3tinymce/interfaces.py
# Compiled at: 2012-04-18 11:00:33
from zope import interface
from zope.configuration import fields

class IZ3TinyMCESchema(interface.Interface):
    path = fields.Path(title='Path to TinyMCE config file', description='Full path to Javascript file that contains TinyMCE config', required=True)