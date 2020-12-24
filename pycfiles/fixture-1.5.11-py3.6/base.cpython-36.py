# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/base.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 7170 bytes
"""Abstract (base) Fixture components.

The more useful bits are in :mod:`fixture.loadable`

"""
import sys, traceback
from inspect import isgeneratorfunction
from six import reraise
try:
    from functools import wraps
except ImportError:

    def wraps(f):

        def wrap_with_f(new_f):
            new_f.__name__ = f.__name__
            if hasattr(f, '__module__'):
                new_f.__module__ = f.__module__
            return new_f

        return wrap_with_f


from fixture.dataset import SuperSet

class FixtureData(object):
    __doc__ = '\n    Loads one or more DataSet objects and provides an interface into that \n    data.\n    \n    Typically this is attached to a concrete Fixture class and constructed by ``data = fixture.data(...)``\n    '

    def __init__(self, datasets, dataclass, loader):
        self.datasets = datasets
        self.dataclass = dataclass
        self.loader = loader
        self.data = None

    def __enter__(self):
        """enter a with statement block.
        
        calls self.setup()
        """
        self.setup()
        return self

    def __exit__(self, type, value, traceback):
        """exit a with statement block.
        
        calls self.teardown()
        """
        self.teardown()

    def __getattr__(self, name):
        """self.name is self.data.name"""
        return getattr(self.data, name)

    def __getitem__(self, name):
        """self['name'] is self.data['name']"""
        return self.data[name]

    def setup(self):
        """load all datasets, populating self.data."""
        self.data = (self.dataclass)(*[ds.shared_instance(default_refclass=(self.dataclass)) for ds in iter(self.datasets)])
        self.loader.load(self.data)

    def teardown(self):
        """unload all datasets."""
        self.loader.unload()


class Fixture(object):
    __doc__ = 'An environment for loading data.\n    \n    An instance of this class can safely be a module-level object.\n    It may be more useful to use a concrete LoadableFixture, such as\n    SQLAlchemyFixture\n    \n    Keywords arguments:\n    \n    dataclass\n        class to instantiate with datasets (defaults to SuperSet)\n    loader\n        class to instantiate and load data sets with.\n      \n    '
    dataclass = SuperSet
    loader = None
    Data = FixtureData

    def __init__(self, dataclass=None, loader=None):
        if dataclass:
            self.dataclass = dataclass
        if loader:
            self.loader = loader

    def __iter__(self):
        for k in self.__dict__:
            yield k

    def with_data(self, *datasets, **cfg):
        """returns a decorator to wrap data around a method.
        
        All positional arguments are DataSet class objects.
        
        the decorated method will receive a new first argument, 
        the Fixture.Data instance.
    
        Keyword arguments:
        
        setup
            optional callable to be executed before test
        teardown
            optional callable to be executed (finally) after test

        """
        from nose.tools import with_setup
        setup = cfg.get('setup', None)
        teardown = cfg.get('teardown', None)

        def decorate_with_data(routine):
            if hasattr(routine, 'setup'):

                def passthru_setup():
                    routine.setup()
                    if setup:
                        setup()

            else:
                passthru_setup = setup
            if hasattr(routine, 'teardown'):

                def passthru_teardown():
                    routine.teardown()
                    if teardown:
                        teardown()

            else:
                passthru_teardown = teardown

            def setup_data():
                data = (self.data)(*datasets)
                data.setup()
                return data

            def teardown_data(data):
                data.teardown()

            @wraps(routine)
            def call_routine(*a, **kw):
                data = setup_data()
                try:
                    routine(data, *a, **kw)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    try:
                        teardown_data(data)
                    except:
                        t_ident = '-----[exception in teardown %s]-----' % hex(id(teardown_data))
                        sys.stderr.write('\n\n%s\n' % t_ident)
                        traceback.print_exc()
                        sys.stderr.write('%s\n\n' % t_ident)

                    reraise(exc.__class__, exc)
                else:
                    teardown_data(data)

            @wraps(routine)
            def iter_routine():
                for stack in routine():
                    fn = stack[0]
                    try:
                        args = stack[1:]
                    except IndexError:
                        args = tuple([])

                    def atomic_routine(*genargs, **kw):
                        setup_data = genargs[0]
                        data = setup_data()
                        try:
                            genargs = genargs[1:]
                        except IndexError:
                            genargs = tuple([])

                        genargs = (
                         data,) + genargs
                        try:
                            fn(*genargs, **kw)
                        except Exception as exc:
                            try:
                                teardown_data(data)
                            except:
                                t_ident = '-----[exception in teardown %s]-----' % hex(id(teardown_data))
                                sys.stderr.write('\n\n%s\n' % t_ident)
                                traceback.print_exc()
                                sys.stderr.write('%s\n\n' % t_ident)

                            reraise(exc.__class__, exc)
                        else:
                            teardown_data(data)

                    restack = (atomic_routine, setup_data) + args
                    yield restack

            if isgeneratorfunction(routine):
                wrapped_routine = iter_routine
            else:
                wrapped_routine = call_routine
            decorate = with_setup(setup=passthru_setup, teardown=passthru_teardown)
            return decorate(wrapped_routine)

        return decorate_with_data

    def data(self, *datasets):
        """returns a :class:`FixtureData` object for datasets."""
        return self.Data(datasets, self.dataclass, self.loader)