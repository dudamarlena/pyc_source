# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/get_user_information.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1403 bytes
import json
cs_handler = 'raw_response'
content_type = 'application/json'
output = csm_api.get_user_information((globals()),
  uname=(cs_form.get('username', None)),
  passwd=(cs_form.get('password_hash', None)),
  api_token=(cs_form.get('api_token', None)),
  course=(cs_form.get('course', None)),
  _as=(cs_form.get('as', None)))

def _json_mapper(x):
    if isinstance(x, (set, tuple)):
        return list(x)
    return


response = json.dumps(output, default=_json_mapper)