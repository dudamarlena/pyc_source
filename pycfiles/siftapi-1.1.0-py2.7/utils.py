# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/siftapi/utils.py
# Compiled at: 2019-02-19 21:08:42
from . import version
VERSION = version.__version__
API_URL = {'production': 'https://api.easilydo.com', 
   'engineering': 'https://api-engineering.easilydo.com'}

def build_url(env, path):
    url = API_URL[env]
    return '%s/%s%s' % (url, VERSION, path)