# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/MANAGER/app/utils/debug.py
# Compiled at: 2017-11-27 07:43:17
# Size of source mod 2**32: 427 bytes
import sys, traceback
from django.views.debug import ExceptionReporter
__all__ = [
 'get_html_traceback']

def get_html_traceback(request=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    message = '%s : %s' % (exc_type, exc_value)
    reporter = ExceptionReporter(request, exc_type, exc_value, exc_traceback, is_email=False)
    html_message = reporter.get_traceback_html()
    return (message, html_message)