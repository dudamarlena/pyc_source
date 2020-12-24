# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/browser/admin.py
# Compiled at: 2008-10-06 10:31:13
"""Forms
"""
from string import strip
from datetime import datetime
from zope import event
from Acquisition import aq_inner
from zope.app.component.hooks import getSite
from zope.formlib import form
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except:
    from zope.app.event.objectevent import ObjectModifiedEvent

from iccommunity.core.browser.base import BaseSettingsForm
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from iccommunity.mediawiki import interfaces
from iccommunity.mediawiki import MediawikiMessageFactory as _

class MediawikiRolesMapper(BaseSettingsForm):
    """Configlet to map Plone roles to mediawiki roles"""
    __module__ = __name__
    form_name = _('Mediawiki Roles Mapper')
    form_fields = form.Fields(interfaces.IicCommunityManagementMediawikiRolesMapper, render_context=True)

    @form.action(_('Apply'), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        rolemap = data['rolemap']
        mtool = getToolByName(aq_inner(self.context), 'portal_membership')
        plone_roles = mtool.getPortalRoles()
        mediawiki_roles = [
         'sysop']
        for item in rolemap:
            if item is None:
                continue
            if item.find(';') < 0:
                message = _('No ";" found.The items must match the following pattern: "Plone role; Mediawiki Role" without quotes. ')
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return
            (plone_role, mediawiki_role) = tuple(map(strip, item.split(';')))
            if plone_role not in plone_roles:
                message = _('You entered a non valid Plone role. The items must match the following pattern: "Plone role; Mediawiki Role" without quotes, where Plone role is a valid role in the portal. Valid Plone roles are: %s' % (plone_roles,))
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return
            elif mediawiki_role not in mediawiki_roles:
                message = _('You entered a non valid Mediawiki role. The items must match the following pattern: "Plone role; Mediawiki Role" without quotes, where Plone role is a valid role in the portal. Valid Mediawiki roles are: %s' % (mediawiki_roles,))
                IStatusMessage(self.request).addStatusMessage(message, type='warn')
                return

        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            event.notify(ObjectModifiedEvent(self.context))
            self.status = _('Updated on ${date_time}', mapping={'date_time': str(datetime.utcnow())})
        else:
            self.status = _('No changes')
        return


class MediawikiSQLServer(BaseSettingsForm):
    """Configlet for the Mediawiki SQL Server"""
    __module__ = __name__
    form_name = _('Mediawiki SQL Server')
    form_fields = form.Fields(interfaces.IicCommunityManagementMediawikiSQLServer, render_context=True)

    @form.action(_('Apply'), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            import _mysql
            from _mysql_exceptions import ProgrammingError, OperationalError, DatabaseError
            try:
                db = _mysql.connect(host=data['hostname'], user=data['username'], passwd=data['password'], db=data['database'])
                if not data['dbprefix']:
                    data['dbprefix'] = ''
                db.query('SELECT * from %suser' % data['dbprefix'])
                r = db.store_result()
                event.notify(ObjectModifiedEvent(self.context))
                self.status = _('Updated on ${date_time}', mapping={'date_time': str(datetime.utcnow())})
            except (ProgrammingError, OperationalError), m:
                (code, mess) = m
                self.status = _('Error ${code}: ${msg}', mapping={'code': code, 'msg': mess})

        else:
            self.status = _('No changes')