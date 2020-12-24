# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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