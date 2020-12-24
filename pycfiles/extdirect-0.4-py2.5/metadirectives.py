# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/zope/metadirectives.py
# Compiled at: 2009-09-20 13:59:59
from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.schema import TextLine

class IDirectRouter(Interface):
    """
    Registers a name and a javascript viewlet for a DirectRouter subclass.
    """
    name = TextLine(title='Name', description='The name of the requested view.')
    for_ = GlobalObject(title='For Interface', description='The interface the directive is used for.', required=False)
    class_ = GlobalObject(title='Class', description='The DirectRouter subclass')
    namespace = TextLine(title='Namespace', description=unicode('The JavaScript namespace under which the remote methods should be available'))
    layer = TextLine(title='Layer', description='The layer', required=False)