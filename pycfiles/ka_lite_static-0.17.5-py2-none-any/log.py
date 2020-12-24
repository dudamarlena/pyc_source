# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/log.py
# Compiled at: 2018-07-11 18:15:30
import logging, traceback
from django.conf import settings
from django.core import mail
from django.views.debug import ExceptionReporter, get_exception_reporter_filter
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


try:
    from logging.config import dictConfig
except ImportError:
    from django.utils.dictconfig import dictConfig

getLogger = logging.getLogger
DEFAULT_LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}, 
               'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}}, 
   'handlers': {'console': {'level': 'INFO', 
                            'filters': [
                                      'require_debug_true'], 
                            'class': 'logging.StreamHandler'}, 
                'null': {'class': 'django.utils.log.NullHandler'}, 
                'mail_admins': {'level': 'ERROR', 
                                'filters': [
                                          'require_debug_false'], 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django': {'handlers': [
                                     'console']}, 
               'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': False}, 
               'py.warnings': {'handlers': [
                                          'console']}}}

class AdminEmailHandler(logging.Handler):
    """An exception log handler that emails log entries to site admins.

    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.
    """

    def __init__(self, include_html=False):
        logging.Handler.__init__(self)
        self.include_html = include_html

    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
             record.levelname,
             request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL',
             record.getMessage())
            filter = get_exception_reporter_filter(request)
            request_repr = filter.get_request_repr(request)
        except Exception:
            subject = '%s: %s' % (
             record.levelname,
             record.getMessage())
            request = None
            request_repr = 'Request repr() unavailable.'

        subject = self.format_subject(subject)
        if record.exc_info:
            exc_info = record.exc_info
            stack_trace = ('\n').join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = (
             None, record.getMessage(), None)
            stack_trace = 'No stack trace available'
        message = '%s\n\n%s' % (stack_trace, request_repr)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        html_message = self.include_html and reporter.get_traceback_html() or None
        mail.mail_admins(subject, message, fail_silently=True, html_message=html_message)
        return

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length.
        RFC 2822's hard limit is 998 characters per line. So, minus "Subject: "
        the actual subject must be no longer than 989 characters.
        """
        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')
        return formatted_subject[:989]


class CallbackFilter(logging.Filter):
    """
    A logging filter that checks the return value of a given callable (which
    takes the record-to-be-logged as its only parameter) to decide whether to
    log a record.

    """

    def __init__(self, callback):
        self.callback = callback

    def filter(self, record):
        if self.callback(record):
            return 1
        return 0


class RequireDebugFalse(logging.Filter):

    def filter(self, record):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):

    def filter(self, record):
        return settings.DEBUG