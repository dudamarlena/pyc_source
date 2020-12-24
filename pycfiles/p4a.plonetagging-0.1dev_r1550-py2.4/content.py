# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/content.py
# Compiled at: 2007-10-12 18:11:48
from zope import component
from zope import interface
import AccessControl
from Acquisition import aq_inner
from lovely.tag import engine
from lovely.tag import tagging
from lovely.tag import interfaces
from p4a.plonetagging import interfaces as ptifaces
from OFS.SimpleItem import SimpleItem
from Products.CMFCore import DynamicType

class ContentTaggingEngine(SimpleItem, engine.TaggingEngine):
    """A Zope2 capable persistent tagging engine.
    """
    __module__ = __name__

    @property
    def __parent__(self):
        raise AttributeError()

    def getTags(self, items=None, users=None):
        if users is not None and not isinstance(users, (tuple, list)):
            users = [
             users]
        return engine.TaggingEngine.getTags(self, items, users)


class UserTagging(tagging.UserTagging):
    __module__ = __name__
    component.adapts(DynamicType.DynamicType)

    @property
    def _pid(self):
        return AccessControl.getSecurityManager().getUser().getId()


class TaggingConfig(SimpleItem):
    __module__ = __name__
    interface.implements(ptifaces.ITaggingConfig)

    def __init__(self, *args, **kwargs):
        super(TaggingConfig, self).__init__(args, kwargs)
        self.tagcloud_tag_blacklist = []


def lookup_tagging_config(context):
    return component.queryUtility(ptifaces.ITaggingConfig, context=context)


def update_keywords(obj, evt):
    engine = component.queryUtility(interfaces.ITaggingEngine)
    if engine is not None:
        tagging = interfaces.ITagging(aq_inner(obj), None)
        if tagging is not None:
            obj.setSubject(list(tagging.getTags()))
            obj.reindexObject()
    return