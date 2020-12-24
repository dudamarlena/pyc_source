# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/patches/error.py
# Compiled at: 2018-04-03 08:39:39
import json
from datetime import datetime
from zExceptions.ExceptionFormatter import format_exception
from edw.logger.util import get_request_data
from edw.logger.config import logger
from edw.logger.config import LOG_ERRORS

def error_logger(self, info):
    strtype = str(getattr(info[0], '__name__', info[0]))
    if strtype in self._ignored_exceptions:
        return
    else:
        if not isinstance(info[2], basestring):
            tb_text = ('').join(format_exception(*info, **{'as_html': 0}))
        else:
            tb_text = info[2]
        request = getattr(self, 'REQUEST', None)
        request_data = get_request_data(request)
        data = {'IP': request_data['ip'], 
           'User': request_data['user'], 
           'Date': datetime.now().isoformat(), 
           'Type': 'Error', 
           'URL': request_data['url'], 
           'Action': request_data['action'], 
           'ErrorType': strtype, 
           'Traceback': tb_text.decode('utf-8', 'ignore').encode('utf-8'), 
           'LoggerName': logger.name}
        logger.error(json.dumps(data))
        return


def error_wrapper(meth):
    """Log errors"""

    def extract(self, *args, **kwargs):
        error_logger(self, *args, **kwargs)
        return meth(self, *args, **kwargs)

    return extract


if LOG_ERRORS:
    from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
    SiteErrorLog.orig_raising = SiteErrorLog.raising
    SiteErrorLog.raising = error_wrapper(SiteErrorLog.raising)