# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/browser/timesheet.py
# Compiled at: 2010-04-14 23:21:59
"""
a timesheet to bill time to a story or an artifact
"""
import operator
from datetime import datetime
from time import time
from zope.interface import implements
from zope.formlib import form
from zope.viewlet.interfaces import IViewlet
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.formlib.formbase import PageForm
from Products.Five.formlib.formbase import EditFormBase
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.vocabulary import SimpleVocabulary
from plone.app.layout.viewlets.common import ViewletBase
from interfaces import IPlonepmTimesheet
from interfaces import ITimesheetForm
from iscorpio.plonepm.utils import revision2Link
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class ChangeLogViewlet(ViewletBase):
    """
    the viewlet to display time billing change logs for the container.
    """
    __module__ = __name__
    index = ViewPageTemplateFile('timesheet_changelog.pt')

    def changeLog(self):
        obj = aq_inner(self.context)
        log = []
        for item in obj.getChangeLog():
            if not item.has_key('worktime'):
                if isinstance(item['datetime'], str):
                    continue
                item['worktime'] = item['datetime']
                item['logtime'] = item['datetime']
            log.append(item)

        return sorted(log, key=operator.itemgetter('worktime'), reverse=True)

    def getMemberFullName(self, memberId):
        """
        return the full name for the given member's id.
        """
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getMemberInfo(memberId)
        if not member:
            return memberId
        else:
            return member['fullname']

    def getFormatedWhen(self, when):
        """
        return a formated datetime to tell when the job been done.
        """
        if isinstance(when, str):
            return when
        else:
            return when.strftime('%Y-%m-%d %H:%M')

    def getFormatedDesc(self, desc):
        """
        return the vormated description by converting rivision number to
        href link.
        """
        obj = aq_inner(self.context)
        return revision2Link(desc, obj.getXppm_browse_code_url())


class BillTimeFormViewlet(PageForm):
    """
    form class based on zope.formlib, it will have a different browser
    defination in zcml.
    """
    __module__ = __name__
    form_fields = form.Fields(ITimesheetForm)
    template = ViewPageTemplateFile('timesheet_form.pt')
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.form_fields['who'].field.vocabulary = self.developers()
        self.form_fields['who'].field.default = self.defaultDeveloperId()
        self.form_fields['when'].field.default = datetime.fromtimestamp(time())

    def allowBillTime(self):
        """
        using membership tool to check current user's permission for
        billing time or not.
        """
        mtool = getToolByName(self, 'portal_membership')
        return mtool.checkPermission('ModifyPortalContent', self.context)

    def developers(self):
        """
        returns the developers assigned to this project as a titled vocabulary.
        """
        context = aq_inner(self.context)
        portalMembers = getToolByName(context, 'portal_membership')
        items = set([ (id, id, portalMembers.getMemberById(id).getProperty('fullname', id)) for id in context.getProjectDevelopers() ])
        member = context.getCurrentMember()
        items.add((member.getId(), member.getId(), member.getProperty('fullname', member.getId())))
        return SimpleVocabulary.fromTitleItems(items)

    def defaultDeveloperId(self):
        """
        returns the current authenticated member as default developer!
        """
        context = aq_inner(self.context)
        return context.getCurrentMember().getId()

    @form.action('Bill Time')
    def action_billTime(self, action, data):
        context = aq_inner(self.context)
        when = data.get('when')
        who = data.get('who')
        description = data.get('description')
        duration = data.get('duration')
        percentage = data.get('percentage')
        context.logTimesheet(when, description, duration, percentage, who)
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal_catalog.indexObject(context)
        self.request.response.redirect(context.absolute_url())