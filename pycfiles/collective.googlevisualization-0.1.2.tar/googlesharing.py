# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/googlesharing/browser/googlesharing.py
# Compiled at: 2010-03-24 19:15:46
__author__ = "D'Elia Federica"
from plone.app.workflow.browser.sharing import SharingView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _
from zExceptions import Forbidden
from Acquisition import aq_inner
from Products.ATContentTypes.content.file import ATFile
from Products.CMFCore.utils import getToolByName
from collective.googlesharing.browser.GDataSharing import GDataSharing

class GoogleSharing(SharingView, GDataSharing):
    __module__ = __name__
    template = ViewPageTemplateFile('googlesharing.pt')

    def __call__(self):
        """Perform the update and redirect if necessary, or render the page
        """
        postback = True
        form = self.request.form
        submitted = form.get('form.submitted', False)
        save_button = form.get('form.button.Save', None) is not None
        cancel_button = form.get('form.button.Cancel', None) is not None
        if submitted and not cancel_button:
            if not self.request.get('REQUEST_METHOD', 'GET') == 'POST':
                raise Forbidden
            authenticator = self.context.restrictedTraverse('@@authenticator', None)
            if not authenticator.verify():
                raise Forbidden
            inherit = bool(form.get('inherit', False))
            reindex = self.update_inherit(inherit, reindex=False)
            entries = form.get('entries', [])
            roles = [ r['id'] for r in self.roles() ]
            settings = []
            for entry in entries:
                settings.append(dict(id=entry['id'], type=entry['type'], roles=[ r for r in roles if entry.get('role_%s' % r, False) ]))

            if settings:
                reindex = self.update_role_settings(settings, reindex=False) or reindex
                context = aq_inner(self.context)
                info = getattr(context, 'file_filesystemstorage_info', None)
                gooId = getattr(info, 'gooId', False)
                if gooId:
                    self.GDocsSharingPermissions(context, settings)
            if reindex:
                aq_inner(self.context).reindexObjectSecurity()
            IStatusMessage(self.request).addStatusMessage(_('Changes saved.'), type='info')
        if cancel_button:
            postback = False
        if postback:
            return self.template()
        else:
            context_state = self.context.restrictedTraverse('@@plone_context_state')
            url = context_state.view_url()
            self.request.response.redirect(url)
        return

    def GDocsSharingPermissions(self, context, settings):
        owner = context.getOwner()
        owner_id = owner.getId()
        mt = getToolByName(context, 'portal_membership')
        if mt.isAnonymousUser():
            return
        member = mt.getAuthenticatedMember()
        member_id = member.getId()
        if not member_id == owner_id:
            return
        settings = settings[1:]
        for setting in settings:
            role = self.convertRolesToGDocs(setting.get('roles'))
            if setting.get('type') == 'user':
                member = mt.getMemberById(setting.get('id'))
                email = member.getProperty('email')
                self.GDocsSetRole(email, role, context)
            if setting.get('type') == 'group':
                t = getToolByName(context, 'acl_users')
                group = t.getGroup(setting.get('id'))
                group_ids = group.getMemberIds()
                for id in group_ids:
                    member = mt.getMemberById(id)
                    email = member.getProperty('email')
                    self.GDocsSetRole(email, role, context)

    def convertRolesToGDocs(self, roles):
        writer = False
        reader = False
        for role in roles:
            if role == 'Editor':
                writer = True
            if role == 'Reader':
                reader = True

        if writer:
            return 'writer'
        elif reader:
            return 'reader'
        else:
            return ''

    def GDocsSetRole(self, email, role, context):
        gd_client = self.Auth(context)
        acl_feed = self.GetAclFeed(gd_client, context)
        update_acl_entry = False
        for acl_entry in acl_feed.entry:
            if email == acl_entry.scope.value:
                update_acl_entry = True
                if not role == '':
                    self.UpdateAclEntry(gd_client, acl_entry, role)
                else:
                    self.DeleteAclEntry(gd_client, acl_entry)

        if not update_acl_entry and not role == '':
            self.AddAclEntry(gd_client, role, email, context)