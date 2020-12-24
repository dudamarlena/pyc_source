# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/event_bus_utils/rmq_handler.py
# Compiled at: 2018-01-23 16:38:14
# Size of source mod 2**32: 9954 bytes
import logging, json, re, datetime, traceback, pika, time, os
from inspect import istraceback
try:
    from collections import OrderedDict
except ImportError:
    pass

VERSION = '0.0.8'
API_VERSION = '1.0.8'
AMQP_URL = 'amqp://guest:guest@localhost'
AMQP_EXCHANGE = 'amq.topic'
try:
    AMQP_URL = str(os.environ['AMQP_URL'])
    AMQP_EXCHANGE = str(os.environ['AMQP_EXCHANGE'])
    print('Env vars for AMQP connection succesfully imported')
    print('URL: %s' % AMQP_URL)
    print('AMQP_EXCHANGE: %s' % AMQP_EXCHANGE)
except KeyError as e:
    print(' Cannot retrieve environment variables for AMQP connection, using default url: %s, exchange: %s' % (
     AMQP_URL, AMQP_EXCHANGE))

RESERVED_ATTRS = ('args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                  'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
                  'message', 'msg', 'name', 'pathname', 'process', 'processName',
                  'relativeCreated', 'stack_info', 'thread', 'threadName')
RESERVED_ATTR_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))

def merge_record_extra(record, target, reserved=RESERVED_ATTR_HASH):
    """
    Merges extra attributes from LogRecord object into target dictionary
    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.__dict__.items():
        if key not in reserved and not (hasattr(key, 'startswith') and key.startswith('_')):
            target[key] = value

    return target


class JsonFormatter(logging.Formatter):
    __doc__ = '\n    A custom formatter to format logging records as json strings.\n    extra values will be formatted as str() if nor supported by\n    json default encoder\n    '

    def __init__(self, *args, **kwargs):
        """
        :param json_default: a function for encoding non-standard objects
            as outlined in http://docs.python.org/2/library/json.html
        :param json_encoder: optional custom encoder
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        """
        self.json_default = kwargs.pop('json_default', None)
        self.json_encoder = kwargs.pop('json_encoder', None)
        self.prefix = kwargs.pop('prefix', '')
        (logging.Formatter.__init__)(self, *args, **kwargs)
        if not self.json_encoder:
            if not self.json_default:

                def _default_json_handler(obj):
                    """Prints dates in ISO format"""
                    if isinstance(obj, (datetime.date, datetime.time)):
                        return obj.isoformat()
                    else:
                        if istraceback(obj):
                            tb = ''.join(traceback.format_tb(obj))
                            return tb.strip()
                        if isinstance(obj, Exception):
                            return 'Exception: %s' % str(obj)
                        return str(obj)

                self.json_default = _default_json_handler
        self._required_fields = self.parse()
        self._skip_fields = dict(zip(self._required_fields, self._required_fields))
        self._skip_fields.update(RESERVED_ATTR_HASH)

    def parse(self):
        """Parses format string looking for substitutions"""
        standard_formatters = re.compile('\\((.+?)\\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)

        log_record.update(message_dict)
        merge_record_extra(record, log_record, reserved=(self._skip_fields))

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return json.dumps(log_record, default=(self.json_default),
          cls=(self.json_encoder))

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
            log_record = OrderedDict()
            log_record['component'] = record.name
            log_record['_api_version'] = API_VERSION
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)
        return '%s%s' % (self.prefix, self.jsonify_log_record(log_record))


class RabbitMQHandler(logging.Handler):
    __doc__ = "\n     A handler that acts as a RabbitMQ publisher\n     Example setup::\n        handler = RabbitMQHandler('amqp://guest:guest@localhost')\n    "

    def __init__(self, url, name, exchange='amq.topic'):
        logging.Handler.__init__(self)
        self.url = url
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.exchange = exchange
        self.name = name
        self.createLock()

    def emit(self, record):
        self.acquire()
        routing_key = '.'.join(['log', record.levelname.lower(), self.name])
        try:
            try:
                self.channel.basic_publish(exchange=(self.exchange),
                  routing_key=routing_key,
                  body=(self.format(record)),
                  properties=pika.BasicProperties(content_type='application/json'))
            except (pika.exceptions.ConnectionClosed, BrokenPipeError):
                print('Log handler connection closed. Reconnecting..')
                self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
                self.channel = self.connection.channel()
                self.channel.basic_publish(exchange=(self.exchange),
                  routing_key=routing_key,
                  body=(self.format(record)),
                  properties=pika.BasicProperties(content_type='application/json'))

        finally:
            self.release()

    def close(self):
        self.acquire()
        try:
            self.channel.close()
        except (AttributeError, pika.exceptions.ConnectionClosed):
            pass

        try:
            try:
                self.connection.close()
            except (AttributeError, pika.exceptions.ConnectionClosed):
                pass

        finally:
            self.release()

        self.connection, self.channel = (None, None)


if __name__ == '__main__':
    rabbitmq_handler = RabbitMQHandler(AMQP_URL, 'MyComponent')
    json_formatter = JsonFormatter()
    rabbitmq_handler.setFormatter(json_formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(rabbitmq_handler)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    logger.addHandler(sh)
    while True:
        logger.critical('This is a critical message')
        time.sleep(1)
        logger.error('This is an error')
        time.sleep(1)
        logger.warning('This is a warning')
        time.sleep(1)
        logger.info('This is an info')
        time.sleep(1)
        logger.debug('This is a debug')