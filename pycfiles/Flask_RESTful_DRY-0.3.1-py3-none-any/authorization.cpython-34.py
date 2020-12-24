# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/authorization.py
# Compiled at: 2015-04-14 08:47:33
# Size of source mod 2**32: 3287 bytes
from flask.ext.login import current_user, login_fresh
from .class_init import attrs
__all__ = ('Requirement', 'Signed_in', 'Not_signed_in', 'Anybody', 'Base_auth_context',
           'sort')

class Requirement:
    __doc__ = "These represent an authorization requirement.\n\n    These objects are stored in the api classes.\n\n    These are intended to be immutable.\n\n    The constructor allows you to place any additional attributes on the\n    requirement for other uses.  By convention, attribute names starting with\n    '_' do not affect how the Requirement validates against an authorization\n    context.  One of these is the '_overrides' attribute, which should be a\n    :class:`.class_init.attrs` that will be added to the url method execution\n    context.\n\n    The `validate` method returns True if valid, False is not valid with no\n    reason given, and a str if not valid for that reason.\n\n    Subclasses must define a validate(self, context, debug) method that return\n    True if the requirement is met, and either False, or `reason` if not met.\n    The `reason` is a str specifying what the user can do to meet this\n    requirement.\n    "
    _overrides = attrs()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._keys = tuple(sorted(k for k in kwargs.keys() if k[0] != '_'))

    def equivalent(self, other):
        """Returns True if self validates identically to other.
        """
        return self.__class__ == other.__class__ and self._keys == other._keys and all(getattr(self, k) == getattr(other, k) for k in self._keys)


class Signed_in(Requirement):
    level = 800
    must_be_fresh = False

    def __repr__(self):
        if self.must_be_fresh:
            return '<Signed_in: must_be_fresh>'
        return '<Signed_in>'

    def validate(self, context, debug):
        if current_user.is_authenticated() and (not self.must_be_fresh or login_fresh()):
            return True
        return False


class Not_signed_in(Requirement):
    level = 800

    def __repr__(self):
        return '<Not_signed_in>'

    def validate(self, context, debug):
        if not current_user.is_authenticated():
            return True
        return False


class Anybody(Requirement):
    level = 900

    def __repr__(self):
        return '<Anybody>'

    def validate(self, context, debug):
        return True


class Base_auth_context:
    __doc__ = 'This caches validation results from the requirements.\n\n    It does this because the link processing hits the same auth_context for\n    every link that might be relevant to the current situation.\n    '

    def __init__(self):
        self.cache = {}

    def meets(self, requirement, debug):
        ans = self.cache.get(requirement, None)
        if ans is None:
            ans = self.cache[requirement] = requirement.validate(self, debug)
        return ans


def sort(*requirements):
    """Returns tuple of requirements sorted by increasing level.
    """
    return tuple(sorted(requirements, key=lambda r: r.level))