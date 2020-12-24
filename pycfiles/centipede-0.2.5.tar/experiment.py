# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiment.py
# Compiled at: 2015-09-29 14:51:18


class ExperimentList(type):
    experiments = {}

    def __init__(cls, name, bases, attrs):
        if name != 'Experiment':
            ExperimentList.experiments[cls.name] = cls


class Experiment:
    __metaclass__ = ExperimentList
    input_files = None
    overrides_tcpdump = False
    external_results = None
    params = {}

    def run(self):
        raise NotImplementedError