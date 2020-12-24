# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/viator/coding/code/microservices/microservices/helpers/logs.py
# Compiled at: 2017-03-07 09:18:20
# Size of source mod 2**32: 1401 bytes


class InstanceMessage(object):

    def __init__(self, instance, logger, name, delimiter):
        self.instance = instance
        self.name = name
        self.logger = logger
        self.delimiter = delimiter

    def __call__(self, message, *args, **kwargs):
        msg = getattr(self.logger, self.name)
        msg('{}{}{}'.format(self.instance, self.delimiter, message), *args, **kwargs)


class InstanceLogger(object):
    __doc__ = "Logger wrapper for instance\n\n    usage:\n    >>>from microservices.utils import get_logger\n    >>>logger = get_logger(__name__)\n    >>>class TestClass(object):\n    >>>    def __str__(self)::\n    >>>        return 'test class'\n    >>>instance_logger = InstanceLogger(TestClass(), logger)\n    >>>instance_logger.info('Hello, world!')\n    you will see:\n        'test class - Hello, world!'\n\n    Instance Logger use method __str__\n    "
    _message_methods = ('log', 'debug', 'exception', 'info', 'warning', 'error', 'warn',
                        'fatal', 'critical')

    def __init__(self, instance, logger, delimiter=' - '):
        self.instance = instance
        self.logger = logger
        self.delimiter = delimiter

    def __getattr__(self, item):
        if item in self._message_methods:
            return InstanceMessage(self.instance, self.logger, item, self.delimiter)
        else:
            return getattr(self.logger, item)