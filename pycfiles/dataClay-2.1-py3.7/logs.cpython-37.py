# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/logs.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 807 bytes
""" Class description goes here. """
import json, logging

class JSONFormatter(logging.Formatter):
    __doc__ = 'Simple JSON formatter for the logging facility.'

    def format(self, obj):
        """Note that obj is a LogRecord instance."""
        ret = dict(obj.__dict__)
        args = ret.pop('args')
        msg = ret.pop('msg')
        ret['message'] = msg % args
        try:
            ei = ret.pop('exc_info')
        except KeyError:
            pass
        else:
            if ei is not None:
                ret['exc_info'] = self.formatException(ei)