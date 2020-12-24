# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/user.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 370 bytes
from xbus.monitor.models.monitor import User
from .util import get_list
from .util import get_record
from . import view_decorators
_MODEL = 'user'

@view_decorators.list(_MODEL)
def user_list(request):
    return get_list(User, request.GET)


@view_decorators.read(_MODEL)
def user_read(request):
    record = get_record(request, _MODEL)
    return record.as_dict()