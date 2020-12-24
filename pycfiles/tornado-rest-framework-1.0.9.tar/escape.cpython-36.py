# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/utils/escape.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 785 bytes
import json
from rest_framework.core.translation import LazyString
from rest_framework.utils import jsonlib, has_ujson
from rest_framework.utils.transcoder import force_text

class LazyStringEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, LazyString):
            return force_text(o)
        else:
            return super().default(o)


def json_encode(value):
    if not has_ujson:
        options = {'ensure_ascii':False,  'allow_nan':False, 
         'indent':None, 
         'separators':(',', ':'), 
         'cls':LazyStringEncoder}
        return (jsonlib.dumps)(value, **options)
    else:
        return jsonlib.dumps(value, escape_forward_slashes=False)


def json_decode(value):
    return jsonlib.loads(value)