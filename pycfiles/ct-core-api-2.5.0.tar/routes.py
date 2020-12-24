# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/web/dez_server/routes.py
# Compiled at: 2016-07-29 22:12:05
from ...util import read
url = None
static = {}
cb = {}
for line in read('app.yaml', True):
    if line.startswith('- url: '):
        url = line[7:].strip()
    elif url:
        if line.startswith('  static_dir: '):
            target = line[14:].strip()
            if '*' in url:
                static[url] = target
            else:
                url = url.rstrip('/')
                static[url] = static[url + '/'] = target
            url = None
        elif line.startswith('  script: '):
            cb[url] = line[10:].split('.')[0]
            url = None