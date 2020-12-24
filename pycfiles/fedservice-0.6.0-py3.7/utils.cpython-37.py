# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/utils.py
# Compiled at: 2019-08-26 12:03:08
# Size of source mod 2**32: 634 bytes
import json, logging
from oidcservice.exception import ResponseError
logger = logging.getLogger(__name__)

def load_json(file_name):
    with open(file_name) as (fp):
        js = json.load(fp)
    return js


def fed_parse_response(instance, info, sformat='', state='', **kwargs):
    if sformat in ('jose', 'jws', 'jwe'):
        resp = instance.post_parse_response(info, state=state)
        if not resp:
            logger.error('Missing or faulty response')
            raise ResponseError('Missing or faulty response')
        return resp
    return (instance.parse_response)(info, sformat, state, **kwargs)