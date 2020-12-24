# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/environment/dpisonline/src/kotti_alert/kotti_alert/views/edit.py
# Compiled at: 2019-09-18 14:40:37
"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import datetime, colander
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.security import Principal
from pyramid.view import view_config
from deform.widget import RadioChoiceWidget, RichTextWidget, TextAreaWidget
from kotti_alert import _
from kotti_alert.resources import Alert

def user_or_group_validator(node, value):
    user_or_group = Principal.query.filter((Principal.name == value) | Principal.groups.contains(value)).first()
    if not user_or_group:
        raise colander.Invalid(node, _('Invalid username, group or role.'))


class AlertSchema(DocumentSchema):
    """ Schema for Alert. """
    body = colander.SchemaNode(colander.String(), title=_('Read more text'), widget=RichTextWidget(height=500), missing='')
    description = colander.SchemaNode(colander.String(), title=_('Alert Message'), widget=TextAreaWidget(cols=40, rows=5), missing='')
    alert_status = colander.SchemaNode(colander.String(), title=_('Alert Status'), validator=colander.OneOf(['info', 'warning', 'danger']), widget=RadioChoiceWidget(values=[
     [
      'info', _('General')],
     [
      'warning', _('Warning')],
     [
      'danger', _('Important')]]), default='info')
    active = colander.SchemaNode(colander.Boolean(), title=_('Enable this alert.'), default=False)
    end_date = colander.SchemaNode(colander.Date(), default=datetime.date.today() + datetime.timedelta(30))
    priority = colander.SchemaNode(colander.Integer(), title=_('Priorty'), default=10)
    username_or_group = colander.SchemaNode(colander.String(), title=_('Username, group or role'), description=_('Only the specified user, group or users with the given role will see this alert. For groups and roles, prepend "group:" or "role:" to the available group or role, e.g. role:principal'), validator=colander.All(user_or_group_validator), default='', missing='')


@view_config(name=Alert.type_info.add_view, permission=Alert.type_info.add_permission, renderer='kotti:templates/edit/node.pt')
class AlertAddForm(AddFormView):
    """ Form to add a new instance of Alert. """
    schema_factory = AlertSchema
    add = Alert
    item_type = _('Alert')


@view_config(name='edit', context=Alert, permission='edit', renderer='kotti:templates/edit/node.pt')
class AlertEditForm(EditFormView):
    """ Form to edit existing Alert objects. """
    schema_factory = AlertSchema