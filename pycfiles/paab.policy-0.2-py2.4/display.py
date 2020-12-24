# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paab/policy/actions/display.py
# Compiled at: 2008-03-09 13:46:41
from OFS.SimpleItem import SimpleItem
from persistent import Persistent
from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone import PloneMessageFactory
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

class IDisplayAction(Interface):
    """
    Interface for the configurable aspects of a notify action.
    This is also used to create add and edit forms, below.
    """
    __module__ = __name__


class DisplayAction(SimpleItem):
    """The actual persistent implementation of the notify action element.
    """
    __module__ = __name__
    implements(IDisplayAction, IRuleElementData)
    element = 'paab.policy.Display'

    @property
    def summary(self):
        pass


class DisplayActionExecutor(object):
    """The executor for this action.
    This is registered as an adapter in configure.zcml
    """
    __module__ = __name__
    implements(IExecutable)
    adapts(Interface, IDisplayAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        obj = self.event.object
        parent = obj.getParentNode()
        r = parent.title
        p = self.context
        wftool = getToolByName(p, 'portal_workflow')
        id = obj.id
        title = obj.title
        description = obj.description
        _createObjectByType('Topic', obj, id=id, title=title, description=description)
        topic = getattr(obj, id)
        sort_crit = topic.addCriterion('created', 'ATSortCriterion')
        state_crit = topic.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_crit.setValue('published')
        topic.setSortCriterion('effective', True)
        topic.unmarkCreationFlag()
        subject_crit = topic.addCriterion('subject', 'ATListCriterion')
        subject_crit.field = 'Subject'
        subject_crit.value = (title,)
        subject_crit.operator = 'or'
        status = wftool.getStatusOf('simple_publication_workflow', topic)
        if status['review_state'] != 'published':
            wftool.doActionFor(topic, 'publish')
        obj.setDefaultPage(id)
        return True


class DisplayAddForm(AddForm):
    """An add form for notify rule actions.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDisplayAction)
    label = _('Add Deafult Action')
    description = _('A notify action can show a message to the user.')
    form_name = _('Configure element')

    def create(self, data):
        a = DisplayAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class DisplayEditForm(EditForm):
    """An edit form for notify rule actions.
    Formlib does all the magic here.
    """
    __module__ = __name__
    form_fields = form.FormFields(IDisplayAction)
    label = _('Edit Display Action')
    description = _('A display action can show a message to the user.')
    form_name = _('Configure element')