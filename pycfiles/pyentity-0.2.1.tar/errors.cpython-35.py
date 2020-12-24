# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mpcabd/Projects/pyentist/env/lib/python3.5/site-packages/pyentist/errors.py
# Compiled at: 2016-03-06 16:06:47
# Size of source mod 2**32: 1213 bytes


class BadBehaviorError(Exception):

    def __init__(self, experiment, name, message):
        self.experiment = experiment
        self.name = name
        super(BadBehaviorError, self).__init__(message)


class BehaviorMissingError(BadBehaviorError):

    def __init__(self, experiment, name):
        super(BehaviorMissingError, self).__init__(experiment, name, '{} missing {} behavior'.format(experiment.name, name))


class BehaviorNotUniqueError(BadBehaviorError):

    def __init__(self, experiment, name):
        super(BehaviorNotUniqueError, self).__init__(experiment, name, '{} already has {} behavior'.format(experiment.name, name))


class NoValueError(Exception):

    def __init__(self, observation):
        self.observation = observation
        super(NoValueError, self).__init__("{} didn't return a value".format(observation.name))


class MismatchError(Exception):

    def __init__(self, name, result):
        self.name = name
        self.result = result
        super(MismatchError, self).__init__("experiment '{}' observations mismatched".format(name))