# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/plugin_interfaces/metaclasses.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 5978 bytes
import logging, inspect
from functools import wraps
from ..components.individual import IndividualBase
from ..components.population import Population
from ..mpiutil import master_only

class AnalysisMeta(type):
    __doc__ = ' Metaclass for analysis plugin class\n    '

    def __new__(cls, name, bases, attrs):
        if 'interval' in attrs:
            interval = attrs['interval']
            if type(interval) is not int or interval <= 0:
                raise TypeError('analysis interval must be a positive integer')
        for method_name in ('setup', 'register_step', 'finalize'):
            method = attrs.get(method_name, None)
            if method is not None and not callable(method):
                msg = '{} must be a callable object'.format(method)
                raise AttributeError(msg)
            else:
                if method is None:
                    if method_name == 'setup':
                        attrs[method_name] = lambda self, ng, engine: None
                    else:
                        if method_name == 'register_step':
                            attrs[method_name] = lambda self, g, population, engine: None
                        elif method_name == 'finalize':
                            attrs[method_name] = lambda self, population, engine: None

        called_in_master = attrs['master_only'] if 'master_only' in attrs else False
        if called_in_master:
            for method_name in ('setup', 'register_step', 'finalize'):
                attrs[method_name] = master_only(attrs[method_name])

        logger_name = 'lsga.{}'.format(name)
        attrs['logger'] = logging.getLogger(logger_name)
        return type.__new__(cls, name, bases, attrs)


class CrossoverMeta(type):
    __doc__ = ' Metaclass for crossover operator class.\n    '

    def __new__(cls, name, bases, attrs):
        if 'cross' not in attrs:
            raise AttributeError('crossover operator class must have cross method')
        else:
            if 'pc' in attrs:
                if attrs['pc'] <= 0.0 or attrs['pc'] > 1.0:
                    raise ValueError('Invalid crossover probability')
            cross = attrs['cross']
            sig = inspect.signature(cross)
            if 'father' not in sig.parameters:
                raise NameError('cross method must have father parameter')
            if 'mother' not in sig.parameters:
                raise NameError('cross method must have mother parameter')

        @wraps(cross)
        def _wrapped_cross(self, father, mother):
            if not (isinstance(father, IndividualBase) and isinstance(mother, IndividualBase)):
                raise TypeError("father and mother's type must be subclass of IndividualBase")
            return cross(self, father, mother)

        attrs['cross'] = _wrapped_cross
        logger_name = 'lsga.{}'.format(name)
        attrs['logger'] = logging.getLogger(logger_name)
        return type.__new__(cls, name, bases, attrs)


class MutationMeta(type):
    __doc__ = ' Metaclass for mutation operator class.\n    '

    def __new__(cls, name, bases, attrs):
        if 'mutate' not in attrs:
            raise AttributeError('mutation operator class must have mutate method')
        else:
            if 'pm' in attrs:
                if attrs['pm'] <= 0.0 or attrs['pm'] > 1.0:
                    raise ValueError('Invalid mutation probability')
            mutate = attrs['mutate']
            sig = inspect.signature(mutate)
            if 'individual' not in sig.parameters:
                raise NameError('mutate method must have individual parameter')

        @wraps(mutate)
        def _wrapped_mutate(self, individual, engine):
            if not isinstance(individual, IndividualBase):
                raise TypeError("individual' type must be subclass of IndividualBase")
            return mutate(self, individual, engine)

        attrs['mutate'] = _wrapped_mutate
        logger_name = 'lsga.{}'.format(name)
        attrs['logger'] = logging.getLogger(logger_name)
        return type.__new__(cls, name, bases, attrs)


class SelectionMeta(type):
    __doc__ = ' Metaclass for selection operator class.\n    '

    def __new__(cls, name, bases, attrs):
        if 'select' not in attrs:
            raise AttributeError('selection operator class must have select method')
        else:
            select = attrs['select']
            sig = inspect.signature(select)
            if 'population' not in sig.parameters:
                raise NameError('select method must have population parameter')
            if 'fitness' not in sig.parameters:
                raise NameError('select method must have fitness parameter')

        @wraps(select)
        def _wrapped_select(self, population, fitness):
            if not isinstance(population, Population):
                raise TypeError('population must be Population object')
            if not callable(fitness):
                raise TypeError('fitness must be a callable object')
            return select(self, population, fitness)

        attrs['select'] = _wrapped_select
        logger_name = 'lsga.{}'.format(name)
        attrs['logger'] = logging.getLogger(logger_name)
        return type.__new__(cls, name, bases, attrs)