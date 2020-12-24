# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tg/ext/repoze/who/authorize.py
# Compiled at: 2008-06-04 11:09:41
"""this module provides an authorize decorator that reimplements the functionnalities
that were present in the orginal identity framework of TG1.
"""
from pylons import request
from copy import copy
import itertools
from pylons.controllers.util import abort
from tg import flash
from inspect import getargspec, formatargspec
from peak.util.decorators import decorate_assignment

def decorate(func, caller, signature=None):
    """Decorate func with caller."""
    if signature is not None:
        (argnames, varargs, kwargs, defaults) = signature
    else:
        (argnames, varargs, kwargs, defaults) = getargspec(func)
    if defaults is None:
        defaults = ()
    parameters = formatargspec(argnames, varargs, kwargs, defaults)[1:-1]
    defval = itertools.count(len(argnames) - len(defaults))
    args = formatargspec(argnames, varargs, kwargs, defaults, formatvalue=lambda value: '=%s' % argnames[defval.next()])[1:-1]
    func_str = '\ndef %s(%s):\n  return caller(func, %s)\n' % (func.__name__, parameters, args)
    exec_dict = dict(func=func, caller=caller)
    exec func_str in exec_dict
    newfunc = exec_dict[func.__name__]
    newfunc.__doc__ = func.__doc__
    newfunc.__dict__ = func.__dict__.copy()
    newfunc.__module__ = func.__module__
    if hasattr(func, '__composition__'):
        newfunc.__composition__ = copy(func.__composition__)
    else:
        newfunc.__composition__ = [
         func]
    newfunc.__composition__.append(newfunc)
    return newfunc


def weak_signature_decorator(entangler):
    """Decorate function with entangler and change signature to accept
    arbitrary additional arguments.

    Enables alternative decorator syntax for Python 2.3 as seen in PEAK:

        [my_decorator(foo)]
        def baz():
            pass

    Mind, the decorator needs to be a closure for this syntax to work.
    """

    def callback(frame, k, v, old_locals):
        return decorate(v, entangler(v), make_weak_signature(v))

    return decorate_assignment(callback, 3)


def simple_weak_signature_decorator(caller):
    """Decorate function with caller and change signature to accept
    arbitrary additional arguments."""

    def entangle(func):
        return decorate(func, caller, make_weak_signature(func))

    return entangle


def make_weak_signature(func):
    """Change signature to accept arbitrary additional arguments."""
    (argnames, varargs, kwargs, defaults) = getargspec(func)
    if kwargs is None:
        kwargs = '_decorator__kwargs'
    if varargs is None:
        varargs = '_decorator__varargs'
    return (
     argnames, varargs, kwargs, defaults)


class Predicate(object):
    """Generic base class for testing true or false for a condition.
    """

    def eval_with_object(self, obj, errors=None):
        """Determine whether the predicate is True or False for the given object.
        """
        raise NotImplementedError

    def append_error_message(self, errors=None):
        if errors is None:
            return
        errors.append(self.error_message % self.__dict__)
        return


class CompoundPredicate(Predicate):
    """A predicate composed of other predicates.
    """

    def __init__(self, *predicates):
        self.predicates = predicates


class All(CompoundPredicate):
    """A compound predicate that evaluates to true only if all sub-predicates
    evaluate to true for the given input.
    """

    def eval_with_object(self, obj, errors=None):
        """Return true if all sub-predicates evaluate to true.
        """
        for p in self.predicates:
            if not p.eval_with_object(obj, errors):
                return False

        return True


class Any(CompoundPredicate):
    """A compound predicate that evaluates to true if any one of its sub-predicates
    evaluates to true.
    """
    error_message = 'No predicates were able to grant access'

    def eval_with_object(self, obj, errors=None):
        """Return true if any sub-predicate evaluates to true.
        """
        for p in self.predicates:
            if p.eval_with_object(obj, None):
                return True

        self.append_error_message(errors)
        return False


class IdentityPredicateHelper(object):
    """A mix-in helper class for Identity Predicates.
    """

    def __nonzero__(self):
        environ = request.environ
        identity = environ.get('repoze.who.identity')
        return self.eval_with_object(identity)


class is_user(Predicate, IdentityPredicateHelper):
    """Predicate for checking if the username matches...
    """
    error_message = 'Not the good user'

    def __init__(self, user_name):
        self.user_name = user_name

    def eval_with_object(self, obj, errors=None):
        user = None
        identity = request.environ.get('repoze.who.identity')
        if identity:
            user = identity.get('user')
        if identity and user and self.user_name == user.user_name:
            return True
        self.append_error_message(errors)
        return False


class in_group(Predicate, IdentityPredicateHelper):
    """Predicate for requiring a group.
    """
    error_message = 'Not member of group: %(group_name)s'

    def __init__(self, group_name):
        self.group_name = group_name

    def eval_with_object(self, obj, errors=None):
        identity = request.environ.get('repoze.who.identity')
        if identity and self.group_name in identity.get('groups'):
            return True
        self.append_error_message(errors)
        return False


class in_all_groups(All, IdentityPredicateHelper):
    """Predicate for requiring membership in a number of groups.
    """

    def __init__(self, *groups):
        group_predicates = [ in_group(g) for g in groups ]
        super(in_all_groups, self).__init__(*group_predicates)


class in_any_group(Any, IdentityPredicateHelper):
    """Predicate for requiring membership in at least one group
    """
    error_message = 'Not member of any group: %(group_list)s'

    def __init__(self, *groups):
        self.group_list = (', ').join(groups)
        group_predicates = [ in_group(g) for g in groups ]
        super(in_any_group, self).__init__(*group_predicates)


class not_anonymous(Predicate, IdentityPredicateHelper):
    """Predicate for checking whether current visitor is anonymous.
    """
    error_message = 'Anonymous access denied'

    def eval_with_object(self, obj, errors=None):
        identity = request.environ.get('repoze.who.identity')
        if not identity:
            self.append_error_message(errors)
            return False
        return True


class has_permission(Predicate, IdentityPredicateHelper):
    """Predicate for checking whether the visitor has a particular permission.
    """
    error_message = 'Permission denied: %(permission_name)s'

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def eval_with_object(self, obj, errors=None):
        """Determine whether the visitor has the specified permission.
        """
        identity = request.environ.get('repoze.who.identity')
        if identity and self.permission_name in identity.get('permissions'):
            return True
        self.append_error_message(errors)
        return False


class has_all_permissions(All, IdentityPredicateHelper):
    """Predicate for checking whether the visitor has all permissions.
    """

    def __init__(self, *permissions):
        permission_predicates = [ has_permission(p) for p in permissions ]
        super(has_all_permissions, self).__init__(*permission_predicates)


class has_any_permission(Any, IdentityPredicateHelper):
    """Predicate for checking whether the visitor has at least one permission.
    """
    error_message = 'No matching permissions: %(permission_list)s'

    def __init__(self, *permissions):
        self.permission_list = (', ').join(permissions)
        permission_predicates = [ has_permission(p) for p in permissions ]
        super(has_any_permission, self).__init__(*permission_predicates)


def require(predicate, obj=None):
    """Function decorator that checks whether the current user is a member of the
    groups specified and has the permissions required.
    """

    def entangle(fn):

        def require(func, self, *args, **kwargs):
            errors = []
            environ = request.environ
            identity = environ.get('repoze.who.identity')
            if predicate is None or predicate.eval_with_object(identity, errors):
                return fn(self, *args, **kwargs)
            flash(errors)
            abort(401)
            return

        fn._require = predicate
        return require

    return weak_signature_decorator(entangle)