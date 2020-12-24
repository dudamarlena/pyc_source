# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/interfaces/blog.py
# Compiled at: 2014-05-08 12:30:23
__docformat__ = 'restructuredtext'
from zope.site.interfaces import IFolder
from ztfy.blog.interfaces import IMainContent, IBaseContentRoles
from ztfy.blog.interfaces.category import ICategoryManagerTarget
from ztfy.blog.interfaces.container import IOrderedContainer
from ztfy.blog.interfaces.topic import ITopic, ITopicContainer
from ztfy.i18n.interfaces.content import II18nBaseContent
from ztfy.security.interfaces import ILocalRoleManager
from zope.container.constraints import contains
from zope.interface import Interface
from zope.schema import Bool, List, Object
from ztfy.blog import _

class IBlogFolder(IFolder):
    """Custom topics container"""
    contains('ztfy.blog.interfaces.blog.IBlogFolder', ITopic)


class IBlogInfo(II18nBaseContent):
    """Base blog interface"""
    visible = Bool(title=_('Visible ?'), description=_('Check to keep blog visible...'), default=True, required=True)


class IBlogWriter(Interface):
    """Blog writer interface"""
    pass


class IBlog(IBlogInfo, IBlogWriter, IBaseContentRoles, ITopicContainer, IMainContent, ICategoryManagerTarget, ILocalRoleManager):
    """Blog full interface"""
    contains(IBlogFolder)


class IBlogContainerInfo(Interface):
    """Blog container marker interface"""
    blogs = List(title=_('Blogs list'), value_type=Object(schema=IBlog), readonly=True)


class IBlogContainer(IBlogContainerInfo, IOrderedContainer):
    """Blog container full interface"""
    pass