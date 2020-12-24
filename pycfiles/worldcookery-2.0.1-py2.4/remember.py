# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/skin/remember.py
# Compiled at: 2006-09-21 05:27:36
from persistent.list import PersistentList
from zope.component import getUtility
from zope.viewlet.viewlet import ViewletBase
from zope.exceptions import UserError
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.session.interfaces import ISession
from zope.app.intid.interfaces import IIntIds
KEY = 'worldcookery'

class RememberViewlet(ViewletBase):
    __module__ = __name__

    def update(self):
        remember = self.request.form.get('worldcookery.remember')
        if remember is not None:
            intid = getUtility(IIntIds).queryId(self.context)
            if intid is None:
                raise UserError(_('This object cannot be remembered.'))
            session = ISession(self.request)[KEY]
            remembered = session.setdefault('remembered', PersistentList())
            if intid in remembered:
                raise UserError(_('This object is already remembered.'))
            remembered.append(intid)
        forget = self.request.form.get('worldcookery.forget')
        if forget is not None:
            forget = int(forget)
            session = ISession(self.request)[KEY]
            remembered = session.get('remembered', [])
            if forget not in remembered:
                raise UserError(_('Cannot forget an object that was not remembered.'))
            remembered.remove(forget)
        return

    render = ViewPageTemplateFile('remember.pt')

    def getRememberedItems(self):
        intids = getUtility(IIntIds)
        session = ISession(self.request)[KEY]
        remembered = session.get('remembered', [])
        return ({'id': intid, 'object': intids.queryObject(intid)} for intid in remembered)