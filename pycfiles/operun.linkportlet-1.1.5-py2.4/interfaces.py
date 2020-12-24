# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/operun/linkportlet/interfaces.py
# Compiled at: 2009-04-08 09:06:23
from zope.interface import Interface, Attribute
from zope import schema
from plone.app.portlets.interfaces import IColumn
from zope.viewlet.interfaces import IViewletManager
from zope.app.container.constraints import contains
from operun.linkportlet import OperunLinkPortletMessageFactory as _

class IOperunLinkArea(Interface):
    """A folderish content type which contains operun Links and operun Link Folders
    """
    __module__ = __name__
    contains('operun.linkportlet.interfaces.IOperunLinkFolder', 'operun.linkportlet.interfaces.IOperunLink')
    title = schema.TextLine(title=_('title', default='Title'), required=True)


class IOperunLinkFolder(Interface):
    """A folder that can contain operun Links and other operun Link Folders
    """
    __module__ = __name__
    contains('operun.linkportlet.interfaces.IOperunLinkFolder', 'operun.linkportlet.interfaces.IOperunLink')
    title = schema.TextLine(title=_('title', default='Title'), required=True)


class IOperunLink(Interface):
    """A configurable link
    """
    __module__ = __name__
    title = schema.TextLine(title=_('title', default='Title'), required=True)
    description = schema.Text(title=_('description', default='Description'), description=_('description_desc', default='A descriptive text.'), required=False)
    linkType = schema.TextLine(title=_('link_type', default=_('Link Type')), description=_('link_type_desc', default=_('Select whether this is an internal or external link.')), required=True)
    internalLink = schema.TextLine(title=_('internal_remoteURL', default='Internal Link'), description=_('internal_remoteURL_desc', default='A link to content inside the CMS.'), required=False)
    externalLink = schema.TextLine(title=_('external_remoteURL', default=_('External Link')), description=_('external_remoteURL_desc', default=_('A link to content outside of the CMS.')), required=False)
    linkTarget = schema.TextLine(title=_('link_target', default='Target window'), description=_('link_target_desc', default='Select whether the link should be opened in the same window or a new one.'), required=True)


class IOperunUnique(Interface):
    """Marker interface for classes with only one instance"""
    __module__ = __name__