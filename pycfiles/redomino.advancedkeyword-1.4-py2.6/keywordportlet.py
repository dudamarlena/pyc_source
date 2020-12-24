# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/portlets/keywordportlet.py
# Compiled at: 2013-05-08 04:41:18
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import implements
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.component import getMultiAdapter
from z3c.form import form
from z3c.form import field
from z3c.form import button
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redomino.advancedkeyword import _
from plone.z3cform import layout

class PortletFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
       portlets layout.
    """
    index = ViewPageTemplateFile('portlets_layout.pt')


class IKeywordPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    name = schema.TextLine(title=_('label_keywordportlet_title', default='Title'), description=_('help_keywordportlet_title', default="The title of the keyword portlet. If empty, it will be used 'Search by {tag}'"), default='', required=True)
    selectedtag = schema.Choice(title=_('label_tags', default='Tags'), vocabulary='redomino.advancedkeyword.vocabularies.Keywords', required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IKeywordPortlet)
    name = ''
    selectedtag = ''

    def __init__(self, name='', selectedtag=''):
        self.name = name
        self.selectedtag = selectedtag

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.name:
            return self.name
        else:
            return _('label_keywordportlet_deftitle', default='Search for ${tag}', mapping={'tag': self.selectedtag})


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    def title(self):
        return self.data.title

    @property
    def available(self):
        return bool(self._data())

    render = ViewPageTemplateFile('keywordportlet.pt')

    def getChildrenTags(self):
        results = self._data()
        return results

    @memoize
    def _data(self):
        tag = self.data.selectedtag
        vocab_factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.Keywords')
        vocab = vocab_factory(self.context)
        tag_level = len(tag.split('.')) + 1
        results = [ (term.value, term.value.split('.')[(-1)]) for term in vocab if term.value.startswith(tag) if len(term.value.split('.')) == tag_level ]
        return results


class AddForm(form.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    implements(IPortletAddForm)
    fields = field.Fields(IKeywordPortlet)
    label = _('label_add_keywordportlet', default='Add keyword portlet')

    def create(self, data):
        return Assignment(**data)

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        addview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(addview))
        url = str(getMultiAdapter((context, self.request), name='absolute_url'))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_('label_save', default='Save'), name='add')
    def handleAdd(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            obj = self.createAndAdd(data)
            if obj is not None:
                self._finishedAdd = True
            return

    @button.buttonAndHandler(_('label_cancel', default='Cancel'), name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''


AddFormView = layout.wrap_form(AddForm, PortletFormWrapper)

class EditForm(form.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    implements(IPortletEditForm)
    fields = field.Fields(IKeywordPortlet)
    label = _('label_modify_keyword_portlet', default='Modify keyword portlet')

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request), name='absolute_url'))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_('label_save', default='Save'), name='apply')
    def handleSave(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = _('status_changes_saved', default='Changes saved')
        else:
            self.status = _('status_no_changes', default='No changes')
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_('label_cancel', default='Cancel'), name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''


EditFormView = layout.wrap_form(EditForm, PortletFormWrapper)