# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/events/base.py
# Compiled at: 2018-03-22 08:59:14
import abc, logging, json
from edw.logger.events import ZOPE_STATUS
from edw.logger.decorators import LogErrors
from edw.logger.config import logger
from edw.logger.config import LOG_CONTENT

class CustomLogErrors(LogErrors):

    def build_error(self, tb):
        entry = super(CustomLogErrors, self).build_error(tb)
        entry['EventType'] = self.context._action
        return entry


def log_errors(message):

    def decorator(func):

        def wrapped(self, *args, **kwargs):
            return CustomLogErrors(func, message, context=self)(*args, **kwargs)

        return wrapped

    return decorator


class BaseEvent(object):
    __metaclass__ = abc.ABCMeta

    @log_errors('Cannot log content action.')
    def __call__(self, *args):
        if not LOG_CONTENT:
            return
        else:
            if not ZOPE_STATUS['ready']:
                return
            if len(args) == 1:
                event = args[0]
                context = None
            else:
                context, event = args
            if self._skip(context, event):
                return
            result = self.log(context, event)
            if result:
                logger.info(json.dumps(result))
            return

    @abc.abstractmethod
    def log(self, context, event):
        pass

    def _skip(self, context, event):
        """ Skip logging.
        """
        return False