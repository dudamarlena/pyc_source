# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_docit/kotti_docit/views/edit.py
# Compiled at: 2016-10-10 16:19:10
"""
Created on 2016-09-20
:author: Oshane Bailey (oshane@alteroo.com)
"""
import colander
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config
from kotti_docit import _
from kotti_docit.resources import AdminManual

class AdminManualSchema(DocumentSchema):
    """ Schema for AdminManual. """
    pass


@view_config(name=AdminManual.type_info.add_view, permission=AdminManual.type_info.add_permission, renderer='kotti:templates/edit/node.pt')
class AdminManualAddForm(AddFormView):
    """ Form to add a new instance of AdminManual. """
    schema_factory = AdminManualSchema
    add = AdminManual
    item_type = _('AdminManual')


@view_config(name='edit', context=AdminManual, permission='edit', renderer='kotti:templates/edit/node.pt')
class AdminManualEditForm(EditFormView):
    """ Form to edit existing AdminManual objects. """
    schema_factory = AdminManualSchema