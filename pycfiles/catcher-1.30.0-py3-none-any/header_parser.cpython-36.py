# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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