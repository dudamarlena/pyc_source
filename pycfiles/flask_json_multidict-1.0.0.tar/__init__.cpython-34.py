# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/underdog/github/flask-json-multidict/flask_json_multidict/__init__.py
# Compiled at: 2015-03-03 20:22:23
# Size of source mod 2**32: 1278 bytes
from werkzeug.datastructures import MultiDict

def get_json_multidict(request):
    """Extract MultiDict from `request.get_json` to produce similar MultiDict to `request.form`"""
    body = request.get_json()
    multi_dict_items = []
    for key in body:
        value = body[key]
        if isinstance(value, list):
            for subvalue in value:
                if not isinstance(subvalue, list) and not isinstance(subvalue, dict):
                    multi_dict_items.append((key, subvalue))
                    continue

        elif isinstance(value, dict):
            continue
            multi_dict_items.append((key, value))

    return MultiDict(multi_dict_items)