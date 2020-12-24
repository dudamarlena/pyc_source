# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/views/edit.py
# Compiled at: 2018-09-19 04:04:51
"""
Created on 2018-09-19
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import colander, deform
from kotti.resources import get_root, Document
from kotti.security import get_principals
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config
from kotti_group_manager import _
from kotti_group_manager.resources import GroupPage
from kotti_group_manager.security import create_groups_listing_page

@colander.deferred
def deferred_choices_widget(node, kw):
    all_groups = []
    principals = get_principals()
    for p in principals.search(name='group:*'):
        value = p.name
        label = p.title
        all_groups.append((value, label))

    return deform.widget.Select2Widget(values=all_groups)


class AddGroupPageSchema(DocumentSchema):
    group_name = colander.SchemaNode(colander.String(), widget=deferred_choices_widget)


@view_config(name=GroupPage.type_info.add_view, permission=GroupPage.type_info.add_permission, renderer='kotti:templates/edit/node.pt')
class GroupPageAddForm(AddFormView):
    """ Form to add a new instance of GroupPage. """
    schema_factory = AddGroupPageSchema
    add = GroupPage
    item_type = _('GroupPage')

    def __init__(self, context, request, **kwargs):
        context = create_groups_listing_page()
        super(GroupPageAddForm, self).__init__(context, request, **kwargs)


@view_config(name='edit', context=GroupPage, permission='edit', renderer='kotti:templates/edit/node.pt')
class GroupPageEditForm(EditFormView):
    """ Form to edit existing GroupPage objects. """
    schema_factory = DocumentSchema