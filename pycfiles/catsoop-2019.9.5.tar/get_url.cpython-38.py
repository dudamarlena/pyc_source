# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/get_url.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1161 bytes
import json
path = cs_form.get('path', None)
cs_handler = 'raw_response'
content_type = 'application/json'
try:
    path = [i for i in path.split('/') if i != '']
    cpath = list(path)
    cpath[0] = 'COURSE'
    ctx = csm_loader.generate_context(path)
    out = {'ok':True,  'url':csm_dispatch.get_real_url(ctx, '/'.join(cpath))}
except:
    out = {'ok': False}
else:
    response = json.dumps(out)