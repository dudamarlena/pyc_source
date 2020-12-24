# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/examples/mathoperations.py
# Compiled at: 2019-12-09 06:13:05
# Size of source mod 2**32: 1116 bytes
from bcsdk.bcsdk import Handler
import logging
log = logging.getLogger('math example')

class MathOperationsHandler(Handler):
    a = None
    operator = None
    response = None
    operations = {'ADD':lambda a, b: a + b, 
     'SUB':lambda a, b: a - b, 
     'MUL':lambda a, b: a * b, 
     'MOD':lambda a, b: a % b, 
     'DIV':lambda a, b: a / b}

    def __init__(self):
        super().__init__()
        self.operator = self.operations['ADD']

    def on_message(self, msg):
        log.error('on_message: {}'.format(msg))
        if self.a is None:
            self.a = int(msg['payload'])
        else:
            response = self.operator(self.a, int(msg['payload']))
            log.error('Emitting response ' + str(response))
            self.send_message({'payload': response})
            self.a = None

    def on_init(self, conf):
        log.error('on_init: {}'.format(conf))
        self.operator = self.operations[conf.get('operation', 'ADD')]
        log.error('Operator is ' + str(self.operator))

    def on_destroy(self):
        log.error('on_destroy')