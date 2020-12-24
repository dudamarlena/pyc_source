# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/message/header_parser.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 519 bytes
from catchbot.config import load_mapping

def get_info_from_headers(headers):
    _value = None
    _host = None
    for host, value in load_mapping()['hosts'].items():
        header = value['header']
        if header not in headers:
            pass
        else:
            _value = value
            _host = host
            break

    result = {'host': _host}
    if 'store_header_value' in value:
        result.update({value['store_header_value']: headers[value['header']]})
    return result