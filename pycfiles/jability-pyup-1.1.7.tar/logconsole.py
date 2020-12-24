# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/amqp/logconsole.py
# Compiled at: 2013-05-25 04:38:30
from middleware import *

class LogConsole:

    def __init__(self, amqp_config, output=sys.stdout):
        self.conf = amqp_config
        self.output = output

    def run(self):
        consumer = AMQP_LogConsumer(self.conf)
        consumer.open()
        consumer.setOutput(self.output)
        consumer.consume_forever()
        consumer.close()