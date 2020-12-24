# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/statusupdate.py
# Compiled at: 2014-03-11 12:09:55
import logging, re, time
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from persistent import Persistent
from zope.interface import implements
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToObject
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from interfaces import IStatusUpdate
from utils import get_microblog_context
logger = logging.getLogger('plonesocial.microblog')

class StatusUpdate(Persistent):
    implements(IStatusUpdate)

    def __init__(self, text, context=None):
        self.__parent__ = self.__name__ = None
        self.id = long(time.time() * 1000000.0)
        self.text = text
        self.date = DateTime()
        self._init_userid()
        self._init_creator()
        self._init_context(context)
        return

    def _init_userid(self):
        self.userid = getSecurityManager().getUser().getId()

    def _init_creator(self):
        portal_membership = getToolByName(getSite(), 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        self.creator = member.getUserName()

    def _init_context(self, context):
        m_context = get_microblog_context(context)
        if m_context is None:
            self._context_uuid = None
        else:
            self._context_uuid = self._context2uuid(m_context)
        if m_context is context:
            self.context_object = None
        else:
            self.context_object = context
        return

    @property
    def context(self):
        if not self.context_uuid:
            return None
        else:
            return uuidToObject(self._context_uuid)

    @property
    def context_uuid(self):
        try:
            return self._context_uuid
        except AttributeError:
            self._context_uuid = None
            return

        return

    def _context2uuid(self, context):
        return IUUID(context)

    @property
    def tags(self):
        return [ x.strip('#,.;:!$') for x in re.findall('#\\S+', self.text) ]

    def getURL(self):
        return ''

    def getObject(self):
        try:
            c_obj = self.context_object
        except AttributeError:
            c_obj = self.context_object = None

        return c_obj or self

    def Title(self):
        return self.text