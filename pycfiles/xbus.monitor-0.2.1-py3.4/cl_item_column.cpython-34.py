# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/cl_item_column.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 2933 bytes
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from xbus.monitor.models.data_clearing import get_session
from xbus.monitor.models.data_clearing import ItemColumn
from .util import get_list
from .util import get_record
from . import view_decorators
_MODEL = 'cl_item_column'

def _update_record(request, record):
    """Update the record using JSON data."""
    try:
        vals = request.json_body
        record.type_id = vals['type_id']
        record.attribute_name = vals['attribute_name']
        record.field_name = vals['field_name']
        record.column_name = vals.get('column_name')
        record.display_name = vals.get('display_name')
        record.data_type = vals.get('data_type') or 'ANY'
        record.related_type_id = vals.get('related_type_id') or None
        record.join_id = vals.get('join_id') or None
        record.is_external_key = vals.get('is_external_key', False)
        record.is_clearable = vals.get('is_clearable', True)
        record.is_dest_default = vals.get('is_dest_default', False)
        record.is_protected = vals.get('is_protected', False)
        record.is_required = vals.get('is_required', False)
        if not record.column_name:
            if record.is_clearable or record.is_external_key:
                raise HTTPBadRequest(json_body={'error': 'Must be associated with a database column'})
    except (KeyError, ValueError):
        raise HTTPBadRequest(json_body={'error': 'Invalid data'})


@view_decorators.list(_MODEL)
def cl_item_column_list(request):

    def record_wrapper(record):
        """Include type names."""
        ret = record.as_dict()
        ret['type_name'] = record.type.display_name
        return ret

    return get_list(ItemColumn, request.GET, sqla_session=get_session(request), record_wrapper=record_wrapper)


@view_decorators.create(_MODEL)
def cl_item_column_create(request):
    record = ItemColumn()
    _update_record(request, record)
    session = get_session(request)
    session.add(record)
    session.flush()
    session.refresh(record)
    return record.as_dict()


@view_decorators.read(_MODEL)
def cl_item_column_read(request):
    record = get_record(request, _MODEL)
    return record.as_dict()


@view_decorators.update(_MODEL)
def cl_item_column_update(request):
    record = get_record(request, _MODEL)
    _update_record(request, record)
    return record.as_dict()


@view_decorators.delete(_MODEL)
def cl_item_column_delete(request):
    record = get_record(request, _MODEL)
    get_session(request).delete(record)
    return Response(status_int=204, json_body={})