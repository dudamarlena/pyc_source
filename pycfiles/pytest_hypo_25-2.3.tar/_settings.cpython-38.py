# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\_settings.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 21702 bytes
"""A module controlling settings for Hypothesis to use in falsification.

Either an explicit settings object can be used or the default object on
this module can be modified.
"""
import contextlib, datetime, inspect, threading, warnings
from enum import Enum, IntEnum, unique
from typing import Any, Dict, List
import attr
from hypothesis.errors import HypothesisDeprecationWarning, InvalidArgument, InvalidState
from hypothesis.internal.reflection import get_pretty_function_description
from hypothesis.internal.validation import check_type, try_convert
from hypothesis.utils.conventions import not_set
from hypothesis.utils.dynamicvariables import DynamicVariable
__all__ = [
 'settings']
all_settings = {}

class settingsProperty:

    def __init__(self, name, show_default):
        self.name = name
        self.show_default = show_default

    def __get__--- This code section failed: ---

 L.  53         0  LOAD_FAST                'obj'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  54         8  LOAD_FAST                'self'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  56        12  SETUP_FINALLY        70  'to 70'

 L.  57        14  LOAD_FAST                'obj'
               16  LOAD_ATTR                __dict__
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                name
               22  BINARY_SUBSCR    
               24  STORE_FAST               'result'

 L.  61        26  LOAD_FAST                'self'
               28  LOAD_ATTR                name
               30  LOAD_STR                 'database'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    64  'to 64'
               36  LOAD_FAST                'result'
               38  LOAD_GLOBAL              not_set
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L.  62        44  LOAD_CONST               0
               46  LOAD_CONST               ('ExampleDatabase',)
               48  IMPORT_NAME_ATTR         hypothesis.database
               50  IMPORT_FROM              ExampleDatabase
               52  STORE_FAST               'ExampleDatabase'
               54  POP_TOP          

 L.  64        56  LOAD_FAST                'ExampleDatabase'
               58  LOAD_GLOBAL              not_set
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'result'
             64_0  COME_FROM            42  '42'
             64_1  COME_FROM            34  '34'

 L.  65        64  LOAD_FAST                'result'
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    12  '12'

 L.  66        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    98  'to 98'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L.  67        84  LOAD_GLOBAL              AttributeError
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                name
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            76  '76'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'

Parse error at or near `POP_TOP' instruction at offset 80

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        raise AttributeError('Cannot delete attribute %s' % (self.name,))

    @property
    def __doc__(self):
        description = all_settings[self.name].description
        default = repr(getattr(settings.default, self.name)) if self.show_default else '(dynamically calculated)'
        return '%s\n\ndefault value: ``%s``' % (description, default)


default_variable = DynamicVariable(None)

class settingsMeta(type):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    @property
    def default(self):
        v = default_variable.value
        if v is not None:
            return v
        if hasattr(settings, '_current_profile'):
            settings.load_profile(settings._current_profile)
            assert default_variable.value is not None
        return default_variable.value

    def _assign_default_internal(self, value):
        default_variable.value = value

    def __setattr__(self, name, value):
        if name == 'default':
            raise AttributeError('Cannot assign to the property settings.default - consider using settings.load_profile instead.')
        else:
            if not (isinstance(value, settingsProperty) or name.startswith('_')):
                raise AttributeError('Cannot assign hypothesis.settings.%s=%r - the settings class is immutable.  You can change the global default settings with settings.load_profile, or use @settings(...) to decorate your test instead.' % (
                 name, value))
        return type.__setattr__(self, name, value)


class settings(settingsMeta('settings', (object,), {})):
    __doc__ = 'A settings object controls a variety of parameters that are used in\n    falsification. These may control both the falsification strategy and the\n    details of the data that is generated.\n\n    Default values are picked up from the settings.default object and\n    changes made there will be picked up in newly created settings.\n    '
    _WHITELISTED_REAL_PROPERTIES = [
     '_construction_complete', 'storage']
    _settings__definitions_are_locked = False
    _profiles = {}
    __module__ = 'hypothesis'

    def __getattr__(self, name):
        if name in all_settings:
            return all_settings[name].default
        raise AttributeError('settings has no attribute %s' % (name,))

    def __init__(self, parent: 'settings'=None, **kwargs: Any) -> None:
        if parent is not None:
            if not isinstance(parent, settings):
                raise InvalidArgument('Invalid argument: parent=%r is not a settings instance' % (parent,))
        else:
            if kwargs.get('derandomize'):
                if kwargs.get('database') is not None:
                    raise InvalidArgument('derandomize=True implies database=None, so passing database=%r too is invalid.' % (
                     kwargs['database'],))
                kwargs['database'] = None
            self._construction_complete = False
            defaults = parent or settings.default
            if defaults is not None:
                for setting in all_settings.values():
                    if kwargs.get(setting.name, not_set) is not_set:
                        kwargs[setting.name] = getattr(defaults, setting.name)
                    elif setting.validator:
                        kwargs[setting.name] = setting.validator(kwargs[setting.name])

        for name, value in kwargs.items():
            if name not in all_settings:
                raise InvalidArgument('Invalid argument: %r is not a valid setting' % (name,))
            setattr(self, name, value)
        else:
            self.storage = threading.local()
            self._construction_complete = True

    def __call__(self, test):
        """Make the settings object (self) an attribute of the test.

        The settings are later discovered by looking them up on the test itself.
        """
        if not callable(test):
            raise InvalidArgument('settings objects can be called as a decorator with @given, but decorated test=%r is not callable.' % (
             test,))
        if inspect.isclass(test):
            from hypothesis.stateful import RuleBasedStateMachine
            if issubclass(test, RuleBasedStateMachine):
                attr_name = '_hypothesis_internal_settings_applied'
                if getattr(test, attr_name, False):
                    raise InvalidArgument('Applying the @settings decorator twice would overwrite the first version; merge their arguments instead.')
                setattr(test, attr_name, True)
                test.TestCase.settings = self
                return test
            raise InvalidArgument('@settings(...) can only be used as a decorator on functions, or on subclasses of RuleBasedStateMachine.')
        if hasattr(test, '_hypothesis_internal_settings_applied'):
            raise InvalidArgument('%s has already been decorated with a settings object.\n    Previous:  %r\n    This:  %r' % (
             get_pretty_function_description(test),
             test._hypothesis_internal_use_settings,
             self))
        test._hypothesis_internal_use_settings = self
        test._hypothesis_internal_settings_applied = True
        return test

    @classmethod
    def _define_setting(cls, name, description, default, options=None, validator=None, show_default=True):
        """Add a new setting.

        - name is the name of the property that will be used to access the
          setting. This must be a valid python identifier.
        - description will appear in the property's docstring
        - default is the default value. This may be a zero argument
          function in which case it is evaluated and its result is stored
          the first time it is accessed on any given settings object.
        """
        if settings._settings__definitions_are_locked:
            raise InvalidState('settings have been locked and may no longer be defined.')
        elif options is not None:
            options = tuple(options)
            if not default in options:
                raise AssertionError
        elif not validator is not None:
            raise AssertionError
        all_settings[name] = Setting(name=name,
          description=(description.strip()),
          default=default,
          options=options,
          validator=validator)
        setattr(settings, name, settingsProperty(name, show_default))

    @classmethod
    def lock_further_definitions(cls):
        settings._settings__definitions_are_locked = True

    def __setattr__(self, name, value):
        if name in settings._WHITELISTED_REAL_PROPERTIES:
            return object.__setattr__(self, name, value)
        elif name in all_settings:
            if self._construction_complete:
                raise AttributeError('settings objects are immutable and may not be assigned to after construction.')
            else:
                setting = all_settings[name]
                if setting.options is not None:
                    if value not in setting.options:
                        raise InvalidArgument('Invalid %s, %r. Valid options: %r' % (
                         name, value, setting.options))
                return object.__setattr__(self, name, value)
        else:
            raise AttributeError('No such setting %s' % (name,))

    def __repr__(self):
        bits = ('%s=%r' % (name, getattr(self, name)) for name in all_settings)
        return 'settings(%s)' % ', '.join(sorted(bits))

    def show_changed(self):
        bits = []
        for name, setting in all_settings.items():
            value = getattr(self, name)
            if value != setting.default:
                bits.append('%s=%r' % (name, value))
            return ', '.join(sorted(bits, key=len))

    @staticmethod
    def register_profile(name: str, parent: 'settings'=None, **kwargs: Any) -> None:
        """Registers a collection of values to be used as a settings profile.

        Settings profiles can be loaded by name - for example, you might
        create a 'fast' profile which runs fewer examples, keep the 'default'
        profile, and create a 'ci' profile that increases the number of
        examples and uses a different database to store failures.

        The arguments to this method are exactly as for
        :class:`~hypothesis.settings`: optional ``parent`` settings, and
        keyword arguments for each setting that will be set differently to
        parent (or settings.default, if parent is None).
        """
        check_type(str, name, 'name')
        settings._profiles[name] = settings(parent=parent, **kwargs)

    @staticmethod
    def get_profile--- This code section failed: ---

 L. 312         0  LOAD_GLOBAL              check_type
                2  LOAD_GLOBAL              str
                4  LOAD_FAST                'name'
                6  LOAD_STR                 'name'
                8  CALL_FUNCTION_3       3  ''
               10  POP_TOP          

 L. 313        12  SETUP_FINALLY        26  'to 26'

 L. 314        14  LOAD_GLOBAL              settings
               16  LOAD_ATTR                _profiles
               18  LOAD_FAST                'name'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L. 315        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    58  'to 58'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 316        40  LOAD_GLOBAL              InvalidArgument
               42  LOAD_STR                 'Profile %r is not registered'
               44  LOAD_FAST                'name'
               46  BUILD_TUPLE_1         1 
               48  BINARY_MODULO    
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            32  '32'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

Parse error at or near `POP_TOP' instruction at offset 36

    @staticmethod
    def load_profile(name: str) -> None:
        """Loads in the settings defined in the profile provided.

        If the profile does not exist, InvalidArgument will be raised.
        Any setting not defined in the profile will be the library
        defined default for that setting.
        """
        check_type(str, name, 'name')
        settings._current_profile = name
        settings._assign_default_internal(settings.get_profile(name))


@contextlib.contextmanager
def local_settings(s):
    default_context_manager = default_variable.with_value(s)
    with default_context_manager:
        (yield s)


@attr.s()
class Setting:
    name = attr.ib()
    description = attr.ib()
    default = attr.ib()
    options = attr.ib()
    validator = attr.ib()


def _max_examples_validator(x):
    check_type(int, x, name='max_examples')
    if x < 1:
        raise InvalidArgument('max_examples=%r should be at least one. You can disable example generation with the `phases` setting instead.' % (
         x,))
    return x


settings._define_setting('max_examples',
  default=100,
  validator=_max_examples_validator,
  description='\nOnce this many satisfying examples have been considered without finding any\ncounter-example, falsification will terminate.\n\nThe default value is chosen to suit a workflow where the test will be part of\na suite that is regularly executed locally or on a CI server, balancing total\nrunning time against the chance of missing a bug.\n\nIf you are writing one-off tests, running tens of thousands of examples is\nquite reasonable as Hypothesis may miss uncommon bugs with default settings.\nFor very complex code, we have observed Hypothesis finding novel bugs after\n*several million* examples while testing :pypi:`SymPy`.\n')
settings._define_setting('derandomize',
  default=False,
  options=(True, False),
  description='\nIf this is True then hypothesis will run in deterministic mode\nwhere each falsification uses a random number generator that is seeded\nbased on the hypothesis to falsify, which will be consistent across\nmultiple runs. This has the advantage that it will eliminate any\nrandomness from your tests, which may be preferable for some situations.\nIt does have the disadvantage of making your tests less likely to\nfind novel breakages.\n')

def _validate_database(db):
    from hypothesis.database import ExampleDatabase
    if db is None or isinstance(db, ExampleDatabase):
        return db
    raise InvalidArgument('Arguments to the database setting must be None or an instance of ExampleDatabase.  Try passing database=ExampleDatabase(%r), or construct and use one of the specific subclasses in hypothesis.database' % (
     db,))


settings._define_setting('database',
  default=not_set,
  show_default=False,
  description='\nAn instance of hypothesis.database.ExampleDatabase that will be\nused to save examples to and load previous examples from. May be ``None``\nin which case no storage will be used, ``":memory:"`` for an in-memory\ndatabase, or any path for a directory-based example database.\n',
  validator=_validate_database)

@unique
class Phase(IntEnum):
    explicit = 0
    reuse = 1
    generate = 2
    target = 3
    shrink = 4

    def __repr__(self):
        return 'Phase.%s' % (self.name,)


@unique
class HealthCheck(Enum):
    __doc__ = 'Arguments for :attr:`~hypothesis.settings.suppress_health_check`.\n\n    Each member of this enum is a type of health check to suppress.\n    '

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__, self.name)

    @classmethod
    def all(cls) -> List['HealthCheck']:
        return list(HealthCheck)

    data_too_large = 1
    filter_too_much = 2
    too_slow = 3
    return_value = 5
    large_base_example = 7
    not_a_test_method = 8


@unique
class Verbosity(IntEnum):
    quiet = 0
    normal = 1
    verbose = 2
    debug = 3

    def __repr__(self):
        return 'Verbosity.%s' % (self.name,)


settings._define_setting('verbosity',
  options=(tuple(Verbosity)),
  default=(Verbosity.normal),
  description='Control the verbosity level of Hypothesis messages')

def _validate_phases(phases):
    phases = tuple(phases)
    for a in phases:
        if not isinstance(a, Phase):
            raise InvalidArgument('%r is not a valid phase' % (a,))
        return tuple((p for p in list(Phase) if p in phases))


settings._define_setting('phases',
  default=(tuple(Phase)),
  description='Control which phases should be run. See :ref:`the full documentation for more details <phases>`',
  validator=_validate_phases)

def _validate_stateful_step_count(x):
    check_type(int, x, name='stateful_step_count')
    if x < 1:
        raise InvalidArgument('stateful_step_count=%r must be at least one.' % (x,))
    return x


settings._define_setting(name='stateful_step_count',
  default=50,
  validator=_validate_stateful_step_count,
  description='\nNumber of steps to run a stateful program for before giving up on it breaking.\n')
settings._define_setting(name='report_multiple_bugs',
  default=True,
  options=(True, False),
  description='\nBecause Hypothesis runs the test many times, it can sometimes find multiple\nbugs in a single run.  Reporting all of them at once is usually very useful,\nbut replacing the exceptions can occasionally clash with debuggers.\nIf disabled, only the exception with the smallest minimal example is raised.\n')

def validate_health_check_suppressions(suppressions):
    suppressions = try_convert(list, suppressions, 'suppress_health_check')
    for s in suppressions:
        if not isinstance(s, HealthCheck):
            raise InvalidArgument('Non-HealthCheck value %r of type %s is invalid in suppress_health_check.' % (
             s, type(s).__name__))
        return suppressions


settings._define_setting('suppress_health_check',
  default=(),
  description='A list of :class:`~hypothesis.HealthCheck` items to disable.',
  validator=validate_health_check_suppressions)

class duration(datetime.timedelta):
    __doc__ = 'A timedelta specifically measured in milliseconds.'

    def __repr__(self):
        ms = self.total_seconds() * 1000
        return 'timedelta(milliseconds=%r)' % (int(ms) if ms == int(ms) else ms,)


def _validate_deadline(x):
    if x is None:
        return x
    invalid_deadline_error = InvalidArgument('deadline=%r (type %s) must be a timedelta object, an integer or float number of milliseconds, or None to disable the per-test-case deadline.' % (
     x, type(x).__name__))
    if isinstance(x, (int, float)):
        if isinstance(x, bool):
            raise invalid_deadline_error
        try:
            x = duration(milliseconds=x)
        except OverflowError:
            raise InvalidArgument('deadline=%r is invalid, because it is too large to represent as a timedelta. Use deadline=None to disable deadlines.' % (
             x,)) from None

    if isinstance(x, datetime.timedelta):
        if x <= datetime.timedelta(0):
            raise InvalidArgument('deadline=%r is invalid, because it is impossible to meet a deadline <= 0. Use deadline=None to disable deadlines.' % (
             x,))
        return duration(seconds=(x.total_seconds()))
    raise invalid_deadline_error


settings._define_setting('deadline',
  default=duration(milliseconds=200),
  validator=_validate_deadline,
  description='\nIf set, a duration (as timedelta, or integer or float number of milliseconds)\nthat each individual example (i.e. each time your test\nfunction is called, not the whole decorated test) within a test is not\nallowed to exceed. Tests which take longer than that may be converted into\nerrors (but will not necessarily be if close to the deadline, to allow some\nvariability in test run time).\n\nSet this to None to disable this behaviour entirely.\n')
settings._define_setting('print_blob',
  default=False,
  options=(True, False),
  description='\nIf set to True, Hypothesis will print code for failing examples that can be used with\n:func:`@reproduce_failure <hypothesis.reproduce_failure>` to reproduce the failing example.\n')
settings.lock_further_definitions()

def note_deprecation(message: str, *, since: str) -> None:
    if since != 'RELEASEDAY':
        date = datetime.datetime.strptime(since, '%Y-%m-%d').date()
        assert datetime.date(2016, 1, 1) <= date
    warnings.warn((HypothesisDeprecationWarning(message)), stacklevel=2)


settings.register_profile('default', settings())
settings.load_profile('default')
assert settings.default is not None