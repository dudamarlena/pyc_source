# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bopen/atcontenttypes/interfaces/richfolder.py
# Compiled at: 2010-09-07 11:53:01
from zope.interface import Interface
from zope import schema
from bopen.atcontenttypes import atcontenttypesMessageFactory as _

class IRichFolder(Interface):
    """A rich folder"""
    __module__ = __name__
    content_logo = schema.Bytes(title=_('Content Image'), required=False, description=_('Field description'))
    dont_link_to_contents = schema.Bool(title=_("Don't link to contents"), required=False, description=_('Field description'))
    long_description = schema.Text(title=_('Long Description'), required=False, description=_('Will be shown befor the body and where long descriptions are needed'))
    text = schema.Text(title=_('Body text'), required=False, description=_('Field description'))