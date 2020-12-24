# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-tutelary/tutelary/exceptions.py
# Compiled at: 2016-04-11 11:38:07
# Size of source mod 2**32: 2816 bytes


class TutelaryException(Exception):
    pass


class EffectException(TutelaryException):
    __doc__ = 'Exception raised when an effect type other that ``allow`` or\n    ``deny`` is encountered in a JSON policy body.\n\n    '

    def __init__(self, effect):
        super().__init__("illegal permission effect: '" + effect + "'")


class PatternOverlapException(TutelaryException):
    __doc__ = 'Exception raised when overlapping action or object patterns are\n    used in a single policy clause.\n\n    '

    def __init__(self, exc_type):
        super().__init__('overlapping ' + exc_type + ' patterns in policy clause')


class PolicyBodyException(TutelaryException):
    __doc__ = 'Exception raised for miscellaneous errors in JSON policy bodies.'

    def __init__(self, msg=None, lineno=None, colno=None):
        if msg is not None:
            super().__init__('illegal policy body: ' + msg)
        else:
            super().__init__('illegal policy body: ' + 'line ' + str(lineno) + ', column ' + str(colno))


class VariableSubstitutionException(TutelaryException):
    __doc__ = 'Exception raised for illegal variable substitutions when using JSON\n    policy bodies.\n\n    '

    def __init__(self):
        super().__init__('illegal variable substitution in policy body')


class RoleVariableException(TutelaryException):
    __doc__ = 'Exception raised for missing or illegal variable substitutions for\n    permissions roles.\n\n    '

    def __init__(self, msg):
        super().__init__('illegal role variables: ' + msg)


class DecoratorException(TutelaryException):
    __doc__ = 'Exception raised if the ``permissioned_model`` decorator is used\n    without the required ``TutelaryMeta`` class member being included\n    in the model.\n\n    '

    def __init__(self, decorator, msg):
        super().__init__("error expanding decorator '" + decorator + "': " + msg)


class PermissionObjectException(TutelaryException):
    __doc__ = 'Exception raised by the ``permissioned_model`` decorator if a\n    ``permissions_object`` property in the ``actions`` list refers to\n    a non-existent model field, or to a field that is not a foreign\n    key or one-to-one relation field.\n\n    '

    def __init__(self, prop):
        super().__init__("invalid permissions_object property '" + prop + "' in permissioned_model")


class InvalidPermissionObjectException(TutelaryException):
    __doc__ = 'Exception raised by authentication backend if the object passed to\n    backend methods is not either a ``tutelary.engine.Object`` or a\n    Django model instance with a ``get_permissions_object`` method.\n\n    '

    def __init__(self):
        super().__init__('invalid object passed to django-tutelary ' + 'backend method')