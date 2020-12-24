# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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