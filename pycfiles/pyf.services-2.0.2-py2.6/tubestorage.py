# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/tubestorage.py
# Compiled at: 2010-06-21 10:30:17
"""Crud Tube Controllers"""
from tg import expose, flash, require, request, redirect, validate
from formencode import validators
from pylons import tmpl_context
from pyf.services.model import DBSession
from pyf.services import model
from pyf.services.model import TubeStorage
from pylons.controllers.util import abort
from sprox.tablebase import TableBase
from sprox.formbase import AddRecordForm, EditableForm
from sprox.fillerbase import EditFormFiller
from pyf.services.controllers.crud import SecureCrudRestController, DataGrid, render_boolean, render_link_field, has_model_permission
from pyf.services.controllers.crud import FancyTableFiller as TableFiller
from pyf.services.core.events import create_event_track, get_logger
from pyf.services.core.router import Router
from pyf.services.core.tasks import launch_tube
from pyf.services.versionning.base import get_repository
from pyf.services.versionning.check import check_tube
from pyf.transport import decode_packet_flow
from repoze.what.predicates import NotAuthorizedError
from operator import itemgetter
from pyf.services.controllers.widgets import TubeLauncher
from tgscheduler.scheduler import add_single_task
import simplejson, transaction, time, tw.forms, logging
log = logging.getLogger()

class TubeStorageController(SecureCrudRestController):
    model = TubeStorage
    __post_to_versionning__ = False
    __order_by__ = 'identifier'
    __desc__ = False

    class new_form_type(AddRecordForm):
        __model__ = TubeStorage
        __omit_fields__ = ['id']
        __require_fields__ = ['identifier', 'key', 'value']

    class edit_form_type(EditableForm):
        __model__ = TubeStorage

    class edit_filler_type(EditFormFiller):
        __model__ = TubeStorage

    class table_type(TableBase):
        __base_widget_type__ = DataGrid
        __model__ = TubeStorage
        __omit_fields__ = ['id']
        __field_order__ = [
         'identifier', 'key', 'value']

    class table_filler_type(TableFiller):
        __model__ = TubeStorage

    @has_model_permission('view')
    @expose('pyf.services.templates.tubestorage.get_one')
    @expose('json')
    def get_one(self, tubestorage_id, action=None, **kwargs):
        tubestorage = DBSession.query(TubeStorage).get(tubestorage_id)
        if request.response_type == 'application/json':
            return dict(value=tubestorage)
        return dict(tubestorage=tubestorage, value=tubestorage, model='TubeStorage')

    @has_model_permission('edit')
    @expose('pyf.services.templates.tubestorage.edit')
    def edit(self, *args, **kwargs):
        return SecureCrudRestController.edit(self, *args, **kwargs)

    @has_model_permission('create')
    @expose('pyf.services.templates.tubestorage.edit')
    def new(self, *args, **kwargs):
        return SecureCrudRestController.new(self, *args, **kwargs)

    @has_model_permission('view')
    @expose('json')
    def get(self, identifier=None, key=None, value=None):
        query = DBSession.query(TubeStorage)
        if identifier is not None:
            query = query.filter(TubeStorage.identifier == identifier)
        if key is not None:
            query = query.filter(TubeStorage.key == key)
        if value is not None:
            query = query.filter(TubeStorage.value == value)
        if query.count() == 0:
            abort(404, comment='There is no corresponding storage')
        if request.response_type == 'application/json':
            return dict(value=list(query))
        else:
            return

    @has_model_permission('')
    @expose('json')
    def store(self, identifier, key, value):
        ts = TubeStorage(identifier=identifier, key=key, value=value)
        DBSession.add(ts)
        DBSession.flush()
        return dict(value=ts)