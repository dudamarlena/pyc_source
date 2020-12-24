# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eg/theme/browser/egosearch.py
# Compiled at: 2010-11-25 03:44:53
from zope import interface, schema
from z3c.form import form, field, button, browser, widget
from plone.z3cform.layout import wrap_form
import datetime
from z3c.form import interfaces
from z3c.form.browser import checkbox
from z3c.form.testing import TestRequest
from Products.CMFCore.utils import getToolByName

class IEgoSearch(interface.Interface):
    __module__ = __name__
    SearchableText = schema.TextLine(title='Full Text', description='Fulltext         search including title, description and text body.', required=False)
    author = schema.TextLine(title='Author', description='Please specify the        user id.', required=False)
    date_von = schema.Int(title='Startdatum', required=False, description="Please enter a start intervall.Value must be 4 digit - e.g. '1600' or '1850'.")
    date_bis = schema.Int(title='Enddatum', required=False, description="Please enter an end intervall. Value must be 4 digit - e.g. '1600' or '1850'.")
    topic = schema.List(title='Topic', description='Please limit your         search by selecting one or multiple items from the list.', value_type=schema.Choice(vocabulary='eg.theme.vocabularies.topics'), default=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'], required=False)
    area = schema.List(title='Area ', description='Please limit your         search by selecting one or multiple items from the list.', value_type=schema.Choice(vocabulary='eg.theme.vocabularies.area'), default=['0', '1', '2', '3', '4', '5', '6'], required=False)
    thread = schema.Choice(title='Thread', description='Please specify a thread.', vocabulary='eg.theme.vocabularies.thread', default='10', required=False)
    item_type = schema.List(title='Type', description='Please select one or more        type(s) to refine your search.', value_type=schema.Choice(vocabulary='eg.theme.vocabularies.media'), default=['n', 'a', 'i', 'v', 'o'], required=False)


class EgoSearchForm(form.Form):
    __module__ = __name__
    fields = field.Fields(IEgoSearch)
    ignoreContext = True
    label = 'Ego Advanced Search'

    def MemberList(context):
        mlist = []
        membership = getToolByName(context, 'portal_membership')
        for m in membership.listMemberIds():
            mlist.append(membership.getMemberInfo(m)['fullname'])

        return mlist

    def MyFieldWidget(field, req):
        return widget.FieldWidget(field, checkbox.SingleCheckBoxWidget(req))

    def MyMultiSelectWidget(field, req):
        return widget.FieldWidget(field, checkbox.CheckBoxWidget(req))

    fields['area'].widgetFactory = MyMultiSelectWidget
    fields['topic'].widgetFactory = MyMultiSelectWidget
    fields['item_type'].widgetFactory = MyMultiSelectWidget

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @button.buttonAndHandler('Search')
    def handleSearch(self, action):
        (data, errors) = self.extractData()
        if errors:
            return
        base_url = '%s/search' % self.portal.absolute_url()
        qstring = '?portal_type=Document'
        if data['SearchableText'] is not None:
            qstring += '&SearchableText=%s' % data['SearchableText']
        else:
            qstring += '&SearchableText=%s' % ''
        if data['author'] is not None:
            qstring += '&Creator=%s' % data['author']
        else:
            qstring += '&Creator=%s' % ''
        if data['date_von'] is not None:
            qstring += '&timefrom:int=%s&timefrom_usage=range:min' % data['date_von']
        else:
            qstring = qstring
        if data['date_bis'] is not None:
            qstring += '&timeuntil:int=%s&timeuntil_usage=range:max' % data['date_bis']
        else:
            qstring = qstring
        qstring += '&topic=%s' % ('+OR+').join(data['topic'])
        qstring += '&area=%s' % ('+OR+').join(data['area'])
        if data['thread'] == '10':
            qstring += '&thread=%s' % ''
        else:
            qstring += '&thread=%s' % data['thread']
        qstring += '&mediacontent=%s' % ('+OR+').join(data['item_type'])
        qstring += '&sort_on=effective&sort_order=descending'
        self.request.response.redirect(base_url + qstring)
        return


EgoSearchView = wrap_form(EgoSearchForm)