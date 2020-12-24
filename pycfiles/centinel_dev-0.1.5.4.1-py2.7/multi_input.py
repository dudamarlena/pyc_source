# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/multi_input.py
# Compiled at: 2015-09-29 14:51:18
import centinel.primitives.http as http
from centinel.experiment import Experiment

class MultiInputHTTPRequestExperiment(Experiment):
    """ This is the multiple-input-file HTTP
    experiment. You can specify filenames using the
    list in the class definition to have Centinel
    load them prior to running the experiment.
    """
    name = 'multi_input_http_request'
    input_files = [
     'input_1', 'input_2']

    def __init__(self, input_files):
        self.input_files = input_files
        self.results = []
        self.host = None
        self.path = '/'
        return

    def run(self):
        for filename, input_file in self.input_files.items():
            for line in input_file:
                self.host = line.strip()
                self.http_request()

    def http_request(self):
        result = http.get_request(self.host, self.path)
        self.results.append(result)