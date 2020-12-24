# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mpcabd/Projects/pyentist/env/lib/python3.5/site-packages/pyentist/__init__.py
# Compiled at: 2016-03-06 15:35:03
# Size of source mod 2**32: 1088 bytes
from .errors import *
from .result import Result
from .experiment import Experiment
from .observation import Observation
from .default import DefaultExperiment
from contextlib import contextmanager

@contextmanager
def science(name, options=None):
    if options and 'experiment_class' in options:
        args = 'args' in options and options['args'] or []
        kwargs = 'kwargs' in options and options['kwargs'] or {}
        experiment = options['experiment_class'](name, *args, **kwargs)
    else:
        experiment = DefaultExperiment(name)
    if options and 'context' in options:
        experiment.context = options['context']
    else:
        experiment.context = default_scientist_context()
    yield experiment
    if options and 'run' in options:
        experiment.run(options['run'])
    else:
        experiment.run()


def default_scientist_context():
    return {}


__all__ = [
 'BadBehaviorError', 'BehaviorMissingError', 'BehaviorNotUniqueError', 'NoValueError', 'MismatchError',
 'Result',
 'Experiment',
 'Observation',
 'DefaultExperiment']