# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/rpc/preprocessors/preprocessor.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 1164 bytes
import logging
LOG = logging.getLogger(__name__)
instruction_preprocessors = {}

def add_preprocessor(entry, name, description, doc=None):
    LOG.info('Adding preprocessor %s' % name)
    instruction_preprocessors[name] = {'name':name, 
     'entry':entry, 
     'description':description, 
     'doc':doc}


def preprocessor(name, description):

    def wrap(entry):
        add_preprocessor(entry, name, description, doc=(entry.__doc__))
        return entry

    return wrap