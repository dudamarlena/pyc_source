# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/site.py
# Compiled at: 2013-09-21 08:56:17
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAnnotations
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.hplskin.interfaces import ISiteManagerPresentationInfo
from ztfy.hplskin.layer import IHPLLayer
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import adapts
from zope.interface import implements
from zope.proxy import setProxiedObject, ProxyBase
from ztfy.blog.defaultskin.site import SiteManagerPresentation as BaseSiteManagerPresentation, SiteManagerIndexView as BaseSiteManagerIndexView
from ztfy.hplskin.menu import HPLSkinDialogMenuItem
from ztfy.hplskin import _
SITE_MANAGER_PRESENTATION_KEY = 'ztfy.hplskin.presentation'

class SiteManagerPresentationViewMenuItem(HPLSkinDialogMenuItem):
    """Site manager presentation menu item"""
    title = _(' :: Presentation model...')


class SiteManagerPresentation(BaseSiteManagerPresentation):
    """Site manager presentation infos"""
    implements(ISiteManagerPresentationInfo)


class SiteManagerPresentationAdapter(ProxyBase):
    adapts(ISiteManager)
    implements(ISiteManagerPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(SITE_MANAGER_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[SITE_MANAGER_PRESENTATION_KEY] = SiteManagerPresentation()
        setProxiedObject(self, presentation)
        return


class SiteManagerPresentationTargetAdapter(object):
    adapts(ISiteManager, IHPLLayer)
    implements(IPresentationTarget)
    target_interface = ISiteManagerPresentationInfo

    def __init__(self, context, request):
        self.context, self.request = context, request


class SiteManagerIndexView(BaseSiteManagerIndexView):
    """Site manager index page"""
    pass