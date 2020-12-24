# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/project/settings_qa_smart_site.py
# Compiled at: 2015-09-02 09:05:45
from project.settings_qa_base import *
LAYERS['layers'] = ('basic', 'smart')
SITE_ID = 4
STATIC_ROOT = abspath('..', 'skeleton-static', 'web')
STATIC_URL = '/static/smart/'
try:
    import local_settings
    from local_settings import *
except ImportError:
    pass

if hasattr(local_settings, 'configure'):
    lcl = locals()
    di = local_settings.configure(**locals())
    lcl.update(**di)