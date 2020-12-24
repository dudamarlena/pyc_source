# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/http_request.py
# Compiled at: 2015-09-29 14:51:18
import centinel.primitives.http as http
from centinel.experiment import Experiment

class HTTPRequestExperiment(Experiment):
    name = 'http_request'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []
        self.host = None
        self.path = '/'
        return

    def run(self):
        for line in self.input_file:
            self.host = line.strip()
            self.http_request()

    def http_request(self):
        result = http.get_request(self.host, self.path)
        self.results.append(result)