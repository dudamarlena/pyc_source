# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/log.py
# Compiled at: 2012-10-12 07:02:39
import logging, sys
LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 
   'WARNING': logging.WARNING, 
   'ERROR': logging.ERROR, 
   'CRITICAL': logging.CRITICAL}

def getLogger(object):
    if isinstance(object, basestring):
        name = object
        if '/myapp/' in name:
            name = 'myapp/' + name.split('/myapp/')[1]
        name = name.replace('/', '.')
    elif type(object) is types.InstanceType:
        name = str(object.__class__)
    else:
        name = object.__class__.__module__ + '.' + object.__class__.__name__
    return logging.getLogger(name)