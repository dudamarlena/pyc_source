# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\identity\conditions.py
# Compiled at: 2011-03-26 09:20:08
"""Definition of the identity predicates."""
__all__ = [
 'All', 'Any', 'NotAny', 'CompoundPredicate', 'IdentityPredicateHelper', 'Predicate', 'SecureObject', 'SecureResource', 'from_host', 'from_any_host', 'in_all_groups', 'in_any_group', 'in_group', 'has_all_permissions', 'has_any_permission', 'has_permission', 'not_anonymous', 'require']
from types import MethodType
from cherrypy import request
from turbogears import config
from turbogears.decorator import weak_signature_decorator
from turbogears.util import match_ip, request_available
from turbogears.identity.exceptions import IdentityException, IdentityFailure, RequestRequiredException
from turbogears.identity.base import current

class Predicate(object):
    """Generic base class for testing true or false for a condition."""
    __module__ = __name__

    def eval_with_object(self, obj, errors=None):
        """Determine whether predicate is True or False for the given object."""
        raise NotImplementedError

    def append_error_message(self, errors=None):
        if errors is None:
            return
        errors.append(self.error_message % self.__dict__)
        return


class CompoundPredicate(Predicate):
    """A predicate composed of other predicates."""
    __module__ = __name__

    def __init__(self, *predicates):
        self.predicates = predicates


class All(CompoundPredicate):
    """Logical 'and' of all sub-predicates.

    This compound predicate evaluates to true only if all of its sub-predicates
    evaluate to true for the given input.

    """
    __module__ = __name__
    error_message = 'One of the predicates denied access'

    def eval_with_object(self, obj, errors=None):
        """Return true if all sub-predicates evaluate to true.
        """
        for p in self.predicates:
            if not p.eval_with_object(obj, errors):
                self.append_error_message(errors)
                return False

        return True


class Any(CompoundPredicate):
    """Logical 'or' of all sub-predicates.

    This compound predicate evaluates to true if any one of its sub-predicates
    evaluates to true for the given input.

    """
    __module__ = __name__
    error_message = 'No predicate was able to grant access'

    def eval_with_object(self, obj, errors=None):
        """Return true if any sub-predicate evaluates to true."""
        for p in self.predicates:
            if p.eval_with_object(obj, None):
                return True

        self.append_error_message(errors)
        return False


class NotAny(CompoundPredicate):
    """Locigal 'nor' of all sub-predicates.

    A compound predicate that evaluates to true only if no sub-predicates
    evaluate to true for the given input.

    """
    __module__ = __name__
    error_message = 'One of the predicates did not deny access'

    def eval_with_object(self, obj, errors=None):
        """Return true if no sub-predicates evaluate to true."""
        for p in self.predicates:
            if p.eval_with_object(obj, errors):
                self.append_error_message(errors)
                return False

        return True


class IdentityPredicateHelper(object):
    """A mix-in helper class for Identity Predicates."""
    __module__ = __name__

    def __nonzero__(self):
        return self.eval_with_object(current)


class in_group(Predicate, IdentityPredicateHelper):
    """Predicate for requiring a group."""
    __module__ = __name__
    error_message = 'Not member of group: %(group_name)s'

    def __init__(self, group_name):
        self.group_name = group_name

    def eval_with_object(self, identity, errors=None):
        if self.group_name in identity.groups:
            return True
        self.append_error_message(errors)
        return False


class in_all_groups(All, IdentityPredicateHelper):
    """Predicate for requiring membership in a number of groups."""
    __module__ = __name__

    def __init__(self, *groups):
        group_predicates = [ in_group(g) for g in groups ]
        super(in_all_groups, self).__init__(*group_predicates)


class in_any_group(Any, IdentityPredicateHelper):
    """Predicate for requiring membership in at least one group."""
    __module__ = __name__
    error_message = 'Not member of any group: %(group_list)s'

    def __init__(self, *groups):
        self.group_list = (', ').join(groups)
        group_predicates = [ in_group(g) for g in groups ]
        super(in_any_group, self).__init__(*group_predicates)


class not_anonymous(Predicate, IdentityPredicateHelper):
    """Predicate for checking whether current visitor is anonymous."""
    __module__ = __name__
    error_message = 'Anonymous access denied'

    def eval_with_object(self, identity, errors=None):
        if identity.anonymous:
            self.append_error_message(errors)
            return False
        return True


class has_permission(Predicate, IdentityPredicateHelper):
    """Predicate for checking whether visitor has a particular permission."""
    __module__ = __name__
    error_message = 'Permission denied: %(permission_name)s'

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def eval_with_object(self, identity, errors=None):
        """Determine whether the visitor has the specified permission."""
        if self.permission_name in identity.permissions:
            return True
        self.append_error_message(errors)
        return False


class has_all_permissions(All, IdentityPredicateHelper):
    """Predicate for checking whether the visitor has all permissions."""
    __module__ = __name__

    def __init__(self, *permissions):
        permission_predicates = [ has_permission(p) for p in permissions ]
        super(has_all_permissions, self).__init__(*permission_predicates)


class has_any_permission(Any, IdentityPredicateHelper):
    """Predicate for checking whether visitor has at least one permission."""
    __module__ = __name__
    error_message = 'No matching permissions: %(permission_list)s'

    def __init__(self, *permissions):
        self.permission_list = (', ').join(permissions)
        permission_predicates = [ has_permission(p) for p in permissions ]
        super(has_any_permission, self).__init__(*permission_predicates)


def _remoteHost():
    if not request_available():
        raise RequestRequiredException()
    else:
        return request.headers.get('X-Forwarded-For', request.headers.get('Remote-Addr', '')).rsplit(',', 1)[(-1)].strip() or None
    return


class from_host(Predicate, IdentityPredicateHelper):
    """Predicate for checking whether the visitor's host is a permitted host.

    Note: We never want to announce what the list of allowed hosts is, because
    it is way too easy to spoof an IP address in a TCP/IP packet.

    """
    __module__ = __name__
    error_message = 'Access from this host is not permitted.'

    def __init__(self, host):
        self.host = host

    def eval_with_object(self, obj, errors=None):
        """Match the visitor's host against the criteria."""
        ip = _remoteHost()
        if ip and match_ip(self.host, ip):
            return True
        self.append_error_message(errors)
        return False


class from_any_host(Any, IdentityPredicateHelper):
    """Predicate for checking the visitor against a number of allowed hosts."""
    __module__ = __name__
    error_message = 'Access from this host is not permitted.'

    def __init__(self, hosts):
        host_predicates = [ from_host(h) for h in hosts ]
        super(from_any_host, self).__init__(*host_predicates)


def require(predicate, obj=None):
    """Function decorator checking requirements for the current user.

    This function decorator checks whether the current user is a member
    of the groups specified and has the permissions required.

    """

    def entangle(fn):

        def require(func, self, *args, **kwargs):
            try:
                errors = []
                if predicate is None or predicate.eval_with_object(current, errors):
                    return fn(self, *args, **kwargs)
            except IdentityException, e:
                errors = [
                 str(e)]

            raise IdentityFailure(errors)
            return

        fn._require = predicate
        return require

    return weak_signature_decorator(entangle)


def _check_method(obj, fn, predicate):

    def _wrapper(*args, **kw):
        errors = []
        if predicate.eval_with_object(current, errors):
            return fn(*args, **kw)
        else:
            raise IdentityFailure(errors)

    _wrapper.exposed = True
    return _wrapper


class SecureResource(object):
    __module__ = __name__

    def __getattribute__(self, name):
        if name.startswith('_cp') or name == 'require':
            return object.__getattribute__(self, name)
        try:
            value = object.__getattribute__(self, name)
            try:
                predicate = object.__getattribute__(self, 'require')
            except AttributeError:
                predicate = config.get('identity.require', None)

            if predicate is None:
                raise AttributeError("SecureResource requires a 'require' attribute either on the controller class itself or in the config file")
            errors = []
            if isinstance(value, MethodType) and hasattr(value, 'exposed'):
                return _check_method(self, value, predicate)
            from turbogears.controllers import Controller
            if isinstance(value, Controller):
                return SecureObject(value, predicate)
            return value
        except IdentityException, e:
            errors = [
             str(e)]

        raise IdentityFailure(errors)
        return


class SecureObject(object):
    __module__ = __name__

    def __init__(self, obj, require, exclude=[]):
        self._object = obj
        self._require = require
        self._exclude = exclude

    def __getattribute__(self, name):
        if name in ('_object', '_require', '_exclude'):
            return object.__getattribute__(self, name)
        try:
            obj = object.__getattribute__(self, '_object')
            value = getattr(obj, name)
            errors = []
            predicate = object.__getattribute__(self, '_require')
            if name in object.__getattribute__(self, '_exclude'):
                return value
            if isinstance(value, MethodType) and hasattr(value, 'exposed'):
                return _check_method(obj, value, predicate)
            from turbogears.controllers import Controller
            if isinstance(value, Controller):
                return SecureObject(value, predicate)
            return value
        except IdentityException, e:
            errors = [
             str(e)]

        raise IdentityFailure(errors)

    def __setattr__(self, name, value):
        if name in ('_object', '_require', '_exclude'):
            super(SecureObject, self).__setattr__(name, value)
        else:
            setattr(self._object, name, value)