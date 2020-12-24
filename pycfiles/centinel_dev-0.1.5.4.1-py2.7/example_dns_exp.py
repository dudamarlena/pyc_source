# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/example_dns_exp.py
# Compiled at: 2015-09-29 14:51:18
import os, logging
from centinel.experiment import Experiment
from centinel.primitives import dnslib

class DNSExperiment(Experiment):
    name = 'dns_example'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []

    def run(self):
        domains = []
        for line in self.input_file:
            domains.append(line.strip())

        lookup_results = dnslib.lookup_domains(domains)
        lookup_results['exp-name'] = 'lookups'
        self.results.append(lookup_results)
        chaos_results = dnslib.send_chaos_queries()
        chaos_results['exp-name'] = 'chaos'
        self.results.append(chaos_results)