# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-intel/egg/herokal/settings.py
# Compiled at: 2013-06-04 16:33:01
import os, re, json, sys
if 'DEBUG' in os.environ.keys():
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    for setting, value in os.environ.iteritems():
        if re.search('^[A-Z][A-Z0-9_]+$', setting):
            try:
                setattr(sys.modules[__name__], setting, json.loads(value))
            except:
                setattr(sys.modules[__name__], setting, value)

else:
    try:
        from local_settings import *
    except ImportError as e:
        print 'Caught %s trying to import local_settings. Please make sure\n                 local_settings.py exists and is free of errors.\n              '
        raise

try:
    del os
    del re
    del json
    del sys
except:
    pass