# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/interfaces.py
# Compiled at: 2013-09-22 11:06:40
__docformat__ = 'restructuredtext'
from ztfy.base.interfaces.container import IOrderedContainer
from ztfy.blog.defaultskin.interfaces import ISiteManagerPresentationInfo as IBaseSiteManagerPresentationInfo, IBlogPresentationInfo as IBaseBlogPresentationInfo, ISectionPresentationInfo as IBaseSectionPresentationInfo, ITopicPresentationInfo as IBaseTopicPresentationInfo
from zope.container.constraints import contains
from zope.interface import Interface
from ztfy.file.schema import ImageField
from ztfy.hplskin import _

class ISiteManagerPresentationInfo(IBaseSiteManagerPresentationInfo):
    """Site manager presentation info"""
    pass


class IBlogPresentationInfo(IBaseBlogPresentationInfo):
    """Blog presentation info"""
    pass


class ISectionPresentationInfo(IBaseSectionPresentationInfo):
    """Section presentation info"""
    pass


class ITopicPresentationInfo(IBaseTopicPresentationInfo):
    """Topic presentation info"""
    pass


class IBannerImage(Interface):
    """Site manager banner interface"""
    image = ImageField(title=_('Image data'), description=_('This attribute holds image data'), required=True)


class ITopBannerImageAddFormMenuTarget(Interface):
    """Marker interface for banner image add form menu target"""
    pass


class ILeftBannerImageAddFormMenuTarget(Interface):
    """Marker interface for banner image add form menu target"""
    pass


class IBannerManager(IOrderedContainer):
    """Banner manager marker interface"""
    contains(IBannerImage)


class IBannerManagerContentsView(Interface):
    """Banner manager contents view marker interface"""
    pass