# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/event_tracking.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 1866 bytes
from pyramid.httpexceptions import HTTPBadRequest
from xbus.monitor.auth import get_logged_user_id
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import Event
from xbus.monitor.models.monitor import EventTracking
from .util import get_list
from .util import get_record
from . import view_decorators
_MODEL = 'event_tracking'

def _update_record(request, record):
    """Update the record using JSON data."""
    try:
        vals = request.json_body
        record.comment = vals['comment']
        record.event_id = vals['event_id']
        if vals['new_state']:
            record.new_state = vals['new_state']
    except (KeyError, ValueError):
        raise HTTPBadRequest(json_body={'error': 'Invalid data'})


@view_decorators.list(_MODEL)
def event_tracking_list(request):
    return get_list(EventTracking, request.GET)


@view_decorators.create(_MODEL)
def event_tracking_create(request):
    record = EventTracking()
    record.user_id = get_logged_user_id(request)
    _update_record(request, record)
    event = DBSession.query(Event).filter(Event.id == record.event_id).first()
    new_state = getattr(record, 'new_state', None)
    if new_state:
        event.tracking_state = new_state
    if record.user_id != event.responsible_id:
        event.responsible_id = record.user_id
    DBSession.add(record)
    DBSession.flush()
    DBSession.refresh(record)
    return record.as_dict()


@view_decorators.read(_MODEL)
def event_tracking_read(request):
    record = get_record(request, _MODEL)
    ret = record.as_dict()
    ret['user_name'] = record.user.display_name
    return ret