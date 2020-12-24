# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/get_deleted.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 614 bytes
from hoerapi.lowlevel import call_api
from hoerapi.util import parse_date, CommonEqualityMixin
from hoerapi.parser import parser_list

class DeleteEntry(CommonEqualityMixin):

    def __init__(self, data):
        self.event_id = int(data['event_ID'])
        self.deldate = parse_date(data['deldate'])


def get_deleted(dateStart=None, dateEnd=None):
    params = {}
    if dateStart is not None:
        params['dateStart'] = dateStart.strftime('%y-%m-%d')
    if dateEnd is not None:
        params['dateEnd'] = dateEnd.strftime('%y-%m-%d')
    return parser_list(DeleteEntry, call_api('getDeleted', params))