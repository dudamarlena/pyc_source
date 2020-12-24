# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/settings.py
# Compiled at: 2015-11-19 06:56:59
TEMPLATE_PATH = '/root/coreInit/coreinit/templates/'
DEFAULT_LOGGER = 'coreinit.logger.syslog_driver'
DEFAULT_DB = 'coreinit.db.drivers.redis_driver'
CACHE_URL = 'localhost'
import os, imp, sys
if 'COREINIT_CONFIG' in os.environ:
    ext_config = imp.load_source('x', os.environ['COREINIT_CONFIG'])
    for variable in dir(ext_config):
        print 'Overriding variable %s' % variable
        setattr(sys.modules[__name__], variable, getattr(ext_config, variable))

else:
    print 'No additional configuration'