# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/event_error.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 1036 bytes
from xbus.monitor.models.monitor import EventError
from .util import get_list
from .util import get_record
from . import view_decorators
_MODEL = 'event_error'

@view_decorators.list(_MODEL)
def event_error_list(request):

    def wrapper(ev):
        """a small wrapper to add the envelope_id & role_login keys
        to the resulting records of the list
        """
        ret = ev.as_dict()
        ret['envelope_id'] = ev.envelope.id
        ret['role_login'] = ev.role.login if ev.role else None
        return ret

    return get_list(EventError, request.GET, record_wrapper=wrapper)


@view_decorators.read(_MODEL)
def event_error_read(request):
    record = get_record(request, _MODEL)
    ret = record.as_dict()
    ret.update({'tracking': [tracker.id for tracker in record.tracking_list], 
     'user_name': record.responsible.display_name if record.responsible else ''})
    return ret