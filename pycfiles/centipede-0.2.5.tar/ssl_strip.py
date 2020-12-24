# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/ssl_strip.py
# Compiled at: 2015-09-29 14:51:18
import logging, requests
from centinel.experiment import Experiment

class SSLStripExperiment(Experiment):
    name = 'ssl_strip'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []

    def run(self):
        for line in self.input_file:
            site = line.strip()
            self.ssl_strip_test(site)

    def ssl_strip_test(self, site):
        result = {'site': site}
        logging.info('Checking %s for SSL stripping' % site)
        req = requests.get(site, allow_redirects=False)
        result['headers'] = dict(req.headers)
        result['status'] = req.status_code
        result['success'] = True
        if req.status_code > 399 or req.status_code < 300:
            result['success'] = False
        if 'https' not in req.headers.get('location', ''):
            result['success'] = False
        self.results.append(result)