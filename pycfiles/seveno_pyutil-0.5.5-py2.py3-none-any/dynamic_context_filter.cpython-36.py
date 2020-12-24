# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/logging_utilities/dynamic_context_filter.py
# Compiled at: 2019-01-17 13:53:03
# Size of source mod 2**32: 8644 bytes
import logging, threading
from collections import OrderedDict
from functools import reduce
from operator import or_
from .. import string_utilities
RFC5424_PREFIX = '1 %(isotime)s %(hostname)s {application_name} %(process)d - - [%(levelname)s]'
COLORLESS_FILELOG_PREFIX = '%(isotime)s %(hostname)s {application_name}[%(process)d] [%(levelname)s]'
COLORED_FILELOG_PREFIX = '%(isotime)s %(hostname)s {application_name}[%(process)d] [%(log_color)s%(levelname)s%(reset)s]'

class DynamicContextFilter(logging.Filter):
    __doc__ = "\n    Logging filter that renders ``cls.context()``.\n\n    Logging context is stored in thread local storage so it can be modified\n    in runtime by any thread.\n\n    This is usefull for ie. prepending ``request_id`` to all messages in\n    context of single http request. But, since it doesn't rely on any HTTP\n    framework, it is not tied to context of HTTP request only but to any kind\n    of repetitive multi step process that needs to connect produced log lines\n    into single context.\n\n    This filter will introduce following log format placeholders.\n\n    +-------------------------------------+-----------------------------------+\n    | placeholder                         | description                       |\n    +-------------------------------------+-----------------------------------+\n    | %(dynamic_context_keys_and_values)s | for given context::               |\n    |                                     |                                   |\n    |                                     |     {'foo': 'bar', 'baz': 42}     |\n    |                                     |                                   |\n    |                                     | will render placeholder as::      |\n    |                                     |                                   |\n    |                                     |    foo: bar, baz: 42              |\n    |                                     |                                   |\n    +-------------------------------------+-----------------------------------+\n    | %(dynamic_context_values)s          | for given context::               |\n    |                                     |                                   |\n    |                                     |     {'foo': 'bar', 'baz': 42}     |\n    |                                     |                                   |\n    |                                     | will render placeholder as::      |\n    |                                     |                                   |\n    |                                     |     [bar] [42]                    |\n    |                                     |                                   |\n    +-------------------------------------+-----------------------------------+\n\n    Example:\n\n        >>> import logging\n        >>> import sys\n        >>> import uuid\n        >>> from logging.config import dictConfig\n        >>>\n        >>> from seveno_pyutil import logging_utilities\n        >>>\n        >>> dictConfig({\n        ...     'version': 1,\n        ...     'disable_existing_loggers': False,\n        ...     'formatters': {\n        ...         'key_and_values': {\n        ...             'format': '%(dynamic_context_keys_and_values)s %(message)s'\n        ...         },\n        ...         'only_values': {\n        ...             'format': '%(dynamic_context_values)s %(message)s'\n        ...         }\n        ...     },\n        ...     'filters': {\n        ...         'dynamic_context': {\n        ...             '()': logging_utilities.DynamicContextFilter\n        ...         }\n        ...     },\n        ...     'handlers': {\n        ...         'console_key_and_values': {\n        ...             'class': 'logging.StreamHandler',\n        ...             'level': 'DEBUG',\n        ...             'formatter': 'key_and_values',\n        ...             'filters': ['dynamic_context'],\n        ...             'stream': 'ext://sys.stdout'\n        ...         },\n        ...         'console_only_values': {\n        ...             'class': 'logging.StreamHandler',\n        ...             'level': 'DEBUG',\n        ...             'formatter': 'only_values',\n        ...             'filters': ['dynamic_context'],\n        ...             'stream': 'ext://sys.stdout'\n        ...         },\n        ...     },\n        ...     'loggers': {\n        ...         'foo': {\n        ...             'level': 'INFO',\n        ...             'propagate': True,\n        ...             'handlers': ['console_key_and_values']\n        ...         },\n        ...         'bar': {\n        ...             'level': 'INFO',\n        ...             'propagate': True,\n        ...             'handlers': ['console_only_values']\n        ...         }\n        ...     }\n        ... })\n        >>>\n        >>> logger_foo = logging.getLogger('foo')\n        >>> logger_bar = logging.getLogger('bar')\n        >>>\n        >>> logging_utilities.DynamicContextFilter.context().update({\n        ...     # 'request_id': uuid.uuid4()\n        ...     'request_id': 'f67d41a0-8188-4294-b8a4-d20d8edfdc95'\n        ... })\n        >>> logger_foo.info('Message1')\n         request_id: f67d41a0-8188-4294-b8a4-d20d8edfdc95, Message1\n        >>> logger_bar.info('Message2')\n         [f67d41a0-8188-4294-b8a4-d20d8edfdc95] Message2\n        >>> logging_utilities.DynamicContextFilter.clear_context()\n        >>> logger_foo.info('Message3')\n         Message3\n        >>> logger_bar.info('Message4')\n         Message4\n        >>>\n\n    Warning:\n        This filter assumes and provides global logging context per thread. In cases\n        where there are multiple context holders in single thread it won't work. In\n        these cases it is necessary to utilize ordinary local context dict and use\n        standard way of passing it to log records via::\n\n            logger.foo(..., extra=context_dict)\n\n        or via own filter and::\n\n            logger = logging.getLogger(__name__)\n            my_context_dict = {'foo': 'val'}\n            logger = logging.LoggerAdapter(logger, context_dict)\n    "
    _LOGGING_CONTEXT = threading.local()

    @classmethod
    def context(cls):
        """Thread local logging context storage."""
        if not hasattr(cls._LOGGING_CONTEXT, 'data'):
            cls._LOGGING_CONTEXT.data = OrderedDict()
        return cls._LOGGING_CONTEXT.data

    @classmethod
    def clear_context(cls):
        if hasattr(cls._LOGGING_CONTEXT, 'data'):
            for key in cls._LOGGING_CONTEXT.data.keys():
                cls._LOGGING_CONTEXT.data[key] = None

    LOG_TAGS_KEYS_AND_VALUES = '%(dynamic_context_keys_and_values)s'
    LOG_TAGS_ONLY_VALUES = '%(dynamic_context_values)s'
    _SUFFIX = ','
    _KEY_VALUE_SEPARATOR = ', '
    _PREFIX = ' '

    @property
    def has_any_context(self):
        return self.context() and reduce(or_, [not string_utilities.is_blank(value) for value in self.context().values()], False)

    @property
    def dynamic_context_keys_and_values(self):
        """
        Generates data for ``record.dynamic_context_keys_and_values``
        attribute.
        """
        if self.has_any_context:
            return self._PREFIX + self._KEY_VALUE_SEPARATOR.join('{}: {}'.format(key, value) for key, value in self.context().items() if not string_utilities.is_blank(value)) + self._SUFFIX
        else:
            return ''

    @property
    def dynamic_context_values(self):
        if self.has_any_context:
            return self._PREFIX + ' '.join('[' + str(value) + ']' for value in self.context().values() if not string_utilities.is_blank(value))
        else:
            return ''

    def filter(self, record):
        record.dynamic_context_keys_and_values = self.dynamic_context_keys_and_values
        record.dynamic_context_values = self.dynamic_context_values
        return super(DynamicContextFilter, self).filter(record)