# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/ping.py
# Compiled at: 2015-09-29 14:51:18
import os, logging
from centinel.experiment import Experiment

class PingExperiment(Experiment):
    name = 'ping'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []

    def run(self):
        for line in self.input_file:
            self.host = line.strip()
            self.ping_test()

    def ping_test(self):
        result = {'host': self.host}
        logging.info('Running ping to %s' % self.host)
        response = os.system('ping -c 1 ' + self.host + ' >/dev/null 2>&1')
        if response == 0:
            result['success'] = 'true'
        else:
            result['success'] = 'false'
        self.results.append(result)