# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/packet/interfaces/filter.py
# Compiled at: 2013-05-16 04:38:47
from ztfy.sendit.app.interfaces.filter import IFilteringPlugin
from zope.interface import Interface
from zope.schema import TextLine, List, Choice
from ztfy.sendit import _

class IMimetypeFilterPluginInfo(Interface):
    """MIME types filter plug-in configuration info"""
    forbidden_extensions = TextLine(title=_('Forbidden extensions'), description=_("Any packet containing a document with a given extension will be excluded.\nPlease enter forbidden files extensions, including leading dot (like '.doc'), separated with spaces or commas"), required=False)
    forbidden_mimetypes = List(title=_('Forbidden MIME types'), description=_('Any packet containing a document of a selected MIME type will be excluded'), value_type=Choice(vocabulary='ZTFY MIME types'), required=False)
    forbidden_magic_types = List(title=_('Forbidden Magic types'), description=_('Magic library provides some custom MIME types, you can select which will be excluded'), value_type=Choice(vocabulary='ZTFY magic types'), required=False)


class IMimetypeFilterPlugin(IFilteringPlugin):
    """A filtering plug-in handling MIME types"""
    pass


class IMimetypeFilterTarget(Interface):
    """Marker interface for MIME types filtering"""
    pass