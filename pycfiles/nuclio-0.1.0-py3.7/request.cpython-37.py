# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nuclio/request.py
# Compiled at: 2018-07-26 10:18:42
# Size of source mod 2**32: 4404 bytes
import json, logging
from datetime import datetime
from sys import stdout
from traitlets import HasTraits, Int, Unicode, Instance, Dict, default, Any

class TriggerInfo(HasTraits):
    __doc__ = 'Mock Trigger information\n\n    Attributes:\n        klass (str): trigger class\n        kind (str): trigger kind\n    '
    klass = Unicode()
    kind = Unicode()


class Event(HasTraits):
    __doc__ = "Mock nuclio event\n\n    Attributes:\n        body: Event body\n        content_type (string): body content type\n        trigger (TriggerInfo): trigger information\n        fields (dict): event fields\n        headers (dict): event headers\n        id: event ID\n        method (str): event method (e.g. 'POST')\n        path (str): event path (e.g. '/handler')\n        size (int): body length in bytes\n        timestamp (datetime): event time\n        url (str): event URL (e.g. 'http://nuclio.io')\n        type (str): event type\n        type_version (str): event type version\n        version (str): event version\n    "
    body = Unicode()
    content_type = Unicode('text/plain')
    trigger = Instance(TriggerInfo)
    fields = Dict()
    headers = Dict()
    id = Unicode()
    method = Unicode('POST')
    path = Unicode('/')
    size = Int()
    timestamp = Instance(datetime)
    url = Unicode('http://nuclio.io')
    type = Unicode()
    type_version = Unicode()
    version = Unicode()

    @default('timestamp')
    def _timestamp_default(self):
        return datetime.now()


class Response(HasTraits):
    __doc__ = 'Mock nuclio response\n\n    Args:\n        headers (dict): Response headers\n        body: Response body\n        status_code (int): Response status code (usually HTTP response code)\n        content_type (str): Response content type (e.g. text/plain)\n    '
    headers = Dict()
    body = Any()
    status_code = Int(200)
    content_type = Unicode('text/plain')


class _Formatter(logging.Formatter):

    def format(self, record):
        """Format log record a string. We're trying to simulate what the nuclio
        logger does.
        """
        timestamp = self.formatTime(record)
        name = record.name
        level = record.levelname[0]
        message = record.getMessage()
        with_data = getattr(record, 'with', None)
        if with_data:
            message = '{} {}'.format(message, json.dumps(with_data))
        return '{} {} ({}) {}'.format(timestamp, name, level, message)


class _Logger:

    def __init__(self, log_format=''):
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(_Formatter())
        self._logger = logger = logging.getLogger('nuclio')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    def debug(self, message, *args):
        (self._logger.debug)(message, *args)

    def info(self, message, *args):
        (self._logger.info)(message, *args)

    def warn(self, message, *args):
        (self._logger.warning)(message, *args)

    def error(self, message, *args):
        (self._logger.error)(message, *args)

    def debug_with(self, message, *args, **kw_args):
        (self._logger.debug)(message, *args, **{'extra': {'with': kw_args}})

    def info_with(self, message, *args, **kw_args):
        (self._logger.info)(message, *args, **{'extra': {'with': kw_args}})

    def warn_with(self, message, *args, **kw_args):
        (self._logger.warning)(message, *args, **{'extra': {'with': kw_args}})

    def error_with(self, message, *args, **kw_args):
        (self._logger.error)(message, *args, **{'extra': {'with': kw_args}})


class Context(HasTraits):
    __doc__ = 'Mock nuclio context\n\n    Attributes:\n        platform: nuclio platform\n        logger: nuclio logger\n        user_data: User data\n    '
    platform = Unicode('local')
    logger = Instance(_Logger, args=())
    user_data = Any(lambda : None)
    Response = Response