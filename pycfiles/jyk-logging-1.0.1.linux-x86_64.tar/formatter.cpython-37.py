# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyongkang/anaconda3/lib/python3.7/site-packages/jyk/logging/formatter.py
# Compiled at: 2020-03-28 09:38:02
# Size of source mod 2**32: 8603 bytes
import os, logging, json, re
from datetime import date, datetime, time
import traceback, importlib
from inspect import istraceback
from collections import OrderedDict
RESERVED_ATTRS = ('args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                  'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
                  'message', 'msg', 'name', 'pathname', 'process', 'processName',
                  'relativeCreated', 'stack_info', 'thread', 'threadName')

def mergeRecordExtra(record, target, reserved):
    """ Merges extra attributes from LogRecord object into target dictionary
    
    Args:
        record (logging.LogRecord): logging.LogRecord
        target (dict): dict to update
        reserved (dict or list): reserved keys to skip
    
    Returns:
        dict: target dict
    """
    for key, value in record.__dict__.items():
        if key not in reserved:
            target[key] = hasattr(key, 'startswith') and key.startswith('_') or value

    return target


class JsonEncoder(json.JSONEncoder):
    __doc__ = 'A custom encoder extending the default JSONEncoder'

    def default(self, obj):
        if isinstance(obj, (date, datetime, time)):
            return self.format_datetime_obj(obj)
        else:
            if istraceback(obj):
                return ''.join(traceback.format_tb(obj)).strip()
            if type(obj) == Exception or isinstance(obj, Exception) or type(obj) == type:
                return str(obj)
            try:
                return super(JsonEncoder, self).default(obj)
            except TypeError:
                try:
                    return str(obj)
                except Exception:
                    return

    def format_datetime_obj(self, obj):
        return obj.isoformat()


class JsonFormatter(logging.Formatter):
    __doc__ = '\n    A custom formatter to format logging records as json strings.\n    Extra values will be formatted as str() if not supported by\n    json default encoder\n    '

    def __init__(self, *args, **kwargs):
        """
        Args:
        :param json_default: a function for encoding non-standard objects
            as outlined in http://docs.python.org/2/library/json.html
        :param json_encoder: optional custom encoder
        :param json_serializer: a :meth:`json.dumps`-compatible callable
            that will be used to serialize the log record.
        :param json_indent: an optional :meth:`json.dumps`-compatible numeric value
            that will be used to customize the indent of the output json.
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        :param json_indent: indent parameter for json.dumps
        :param json_ensure_ascii: ensure_ascii parameter for json.dumps
        :param reserved_attrs: an optional list of fields that will be skipped when
            outputting json log record. Defaults to all log record attributes:
            http://docs.python.org/library/logging.html#logrecord-attributes
        :param timestamp: an optional string/boolean field to add a timestamp when
            outputting the json log record. If string is passed, timestamp will be added
            to log record using string as key. If True boolean is passed, timestamp key
            will be "timestamp". Defaults to False/off.
        """
        self.json_default = self._str_to_fn(kwargs.pop('json_default', None))
        self.json_encoder = self._str_to_fn(kwargs.pop('json_encoder', None))
        self.json_serializer = self._str_to_fn(kwargs.pop('json_serializer', json.dumps))
        self.json_indent = kwargs.pop('json_indent', None)
        self.json_ensure_ascii = kwargs.pop('json_ensure_ascii', True)
        self.prefix = kwargs.pop('prefix', '')
        reserved_attrs = kwargs.pop('reserved_attrs', RESERVED_ATTRS)
        self.reserved_attrs = dict(zip(reserved_attrs, reserved_attrs))
        self.timestamp = kwargs.pop('timestamp', True)
        (logging.Formatter.__init__)(self, *args, **kwargs)
        if not self.json_encoder:
            if not self.json_default:
                self.json_encoder = JsonEncoder
        self._required_fields = self.parse()
        self._skip_fields = dict(zip(self._required_fields, self._required_fields))
        self._skip_fields.update(self.reserved_attrs)

    def _str_to_fn(self, fn_as_str):
        """
        If the argument is not a string, return whatever was passed in.
        Parses a string such as package.module.function, imports the module
        and returns the function.
        :param fn_as_str: The string to parse. If not a string, return it.
        """
        if not isinstance(fn_as_str, str):
            return fn_as_str
        path, _, function = fn_as_str.rpartition('.')
        module = importlib.import_module(path)
        return getattr(module, function)

    def parse(self):
        """
        Parses format string looking for substitutions
        This method is responsible for returning a list of fields (as strings)
        to include in all log messages.
        """
        standard_formatters = re.compile('\\((.+?)\\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)

        action = record.__dict__.get('action')
        status = record.__dict__.get('status')
        task_id = record.__dict__.get('task_id', os.getpid())
        required_field = {'task_id':task_id, 
         'action':action, 
         'status':status, 
         'level':record.levelname.lower(), 
         'message':record.getMessage()}
        for k, v in required_field.items():
            log_record[k] = v

        log_record.update(message_dict)
        mergeRecordExtra(record, log_record, reserved=(self._skip_fields))
        if self.timestamp:
            key = self.timestamp if type(self.timestamp) == str else 'timestamp'
            log_record[key] = datetime.utcnow()

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return self.json_serializer(log_record, default=(self.json_default),
          cls=(self.json_encoder),
          indent=(self.json_indent),
          ensure_ascii=(self.json_ensure_ascii))

    def format(self, record):
        """Formats a log record and serializes to json"""
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
        else:
            record.message = record.getMessage()
        if 'asctime' in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)
        if record.exc_info:
            if not message_dict.get('exc_info'):
                message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info'):
            if record.exc_text:
                message_dict['exc_info'] = record.exc_text
        try:
            if record.stack_info:
                if not message_dict.get('stack_info'):
                    message_dict['stack_info'] = self.formatStack(record.stack_info)
        except AttributeError:
            pass

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)
        return '%s%s' % (self.prefix, self.jsonify_log_record(log_record))