# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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