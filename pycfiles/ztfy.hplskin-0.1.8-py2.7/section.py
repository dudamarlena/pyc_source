# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/section.py
# Compiled at: 2013-09-21 08:56:03
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAnnotations
from ztfy.blog.interfaces.section import ISection
from ztfy.hplskin.interfaces import ISectionPresentationInfo
from ztfy.hplskin.layer import IHPLLayer
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import adapts
from zope.interface import implements
from zope.proxy import ProxyBase, setProxiedObject
from ztfy.hplskin.menu import HPLSkinDialogMenuItem
from ztfy.blog.defaultskin.section import SectionPresentation as BaseSectionPresentation, SectionIndexView as BaseSectionIndexView
from ztfy.hplskin import _
SECTION_PRESENTATION_KEY = 'ztfy.hplskin.section.presentation'

class SectionPresentationViewMenuItem(HPLSkinDialogMenuItem):
    """Section presentation menu item"""
    title = _(' :: Presentation model...')


class SectionPresentation(BaseSectionPresentation):
    """Section presentation infos"""
    implements(ISectionPresentationInfo)


class SectionPresentationAdapter(ProxyBase):
    adapts(ISection)
    implements(ISectionPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(SECTION_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[SECTION_PRESENTATION_KEY] = SectionPresentation()
        setProxiedObject(self, presentation)
        return


class SectionPresentationTargetAdapter(object):
    adapts(ISection, IHPLLayer)
    implements(IPresentationTarget)
    target_interface = ISectionPresentationInfo

    def __init__(self, context, request):
        self.context, self.request = context, request


class SectionIndexView(BaseSectionIndexView):
    """Section index page"""
    pass