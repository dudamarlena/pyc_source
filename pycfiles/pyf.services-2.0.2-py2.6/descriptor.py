# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/descriptor.py
# Compiled at: 2010-05-21 08:57:50
"""Crud Descriptor Controllers"""
from tg import expose, flash, require, request, redirect, validate
from formencode import validators
from pylons import tmpl_context
from pyf.services.model import DBSession
from pyf.services import model
from pyf.services.model import Descriptor
from sprox.tablebase import TableBase
from sprox.formbase import AddRecordForm, EditableForm
from sprox.fillerbase import EditFormFiller
from pyf.services.controllers.crud import SecureCrudRestController, DataGrid, render_boolean, render_link_field, has_model_permission
from pyf.services.controllers.crud import FancyTableFiller as TableFiller
from pyf.services.core.events import create_event_track, get_logger
from pyf.services.core.router import Router
from pyf.services.core.tasks import launch_tube
from tgscheduler.scheduler import add_single_task
import transaction, time

class DescriptorController(SecureCrudRestController):
    model = Descriptor
    __post_to_versionning__ = True
    __order_by__ = 'name'
    __desc__ = False

    class new_form_type(AddRecordForm):
        __model__ = Descriptor
        __field_order__ = ['id', 'name', 'display_name', 'description',
         'default_encoding', 'payload_xml']

    class edit_form_type(EditableForm):
        __model__ = Descriptor
        __field_order__ = ['id', 'name', 'display_name', 'description',
         'default_encoding', 'payload_xml']

    class edit_filler_type(EditFormFiller):
        __model__ = Descriptor

    class table_type(TableBase):
        __base_widget_type__ = DataGrid
        __model__ = Descriptor
        __omit_fields__ = ['id', 'payload_xml', 'id', 'dispatchs']
        __xml_fields__ = ['actions', 'dispatchs']

    class table_filler_type(TableFiller):
        __model__ = Descriptor
        dispatchs = render_link_field('/dispatchs/%s', 'dispatchs', 'display_name')

    @has_model_permission('edit')
    @expose('pyf.services.templates.descriptor.edit')
    def edit(self, *args, **kwargs):
        return SecureCrudRestController.edit(self, *args, **kwargs)

    @has_model_permission('create')
    @expose('pyf.services.templates.descriptor.edit')
    def new(self, *args, **kwargs):
        return SecureCrudRestController.new(self, *args, **kwargs)