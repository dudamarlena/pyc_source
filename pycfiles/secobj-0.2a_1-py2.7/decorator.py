# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/decorator.py
# Compiled at: 2012-08-23 10:07:44
import functools, inspect, itertools
from secobj.localization import _
from secobj.logger import getlogger
from secobj.permission import getpermission, Permission
from secobj.principal import SYSTEM
from secobj.principal import Principal
from secobj.provider import getprovider
from secobj.rule import Rule
from secobj.utils import error

def decorate_function(func, acl, permission=None, inherit=True, owner=SYSTEM, callback=None):

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if callback:
            resource = callback(*args, **kwargs)
        else:
            resource = decorator
        getprovider().checkaccess(resource, permission=decorator.__acl_permission__, args=args, kwargs=kwargs)
        return func(*args, **kwargs)

    if isinstance(permission, basestring):
        permission = getpermission(permission)
    assert inspect.isfunction(func)
    assert isinstance(acl, tuple)
    assert isinstance(inherit, bool)
    assert isinstance(permission, Permission) or permission is None
    assert isinstance(owner, Principal)
    decorator.__acl__ = acl
    decorator.__acl_owner__ = owner
    decorator.__acl_inherit__ = inherit
    decorator.__acl_permission__ = permission
    return decorator


def decorate_class(cls, acl, permission=None, inherit=True, owner=SYSTEM, callback=None):

    def constructor(self, *args, **kwargs):
        if callback:
            resource = callback(self, *args, **kwargs)
        else:
            resource = self
        getprovider().checkaccess(resource, permission=self.__acl_permission__)
        self.__acl_decorated_init__(*args, **kwargs)

    if isinstance(permission, basestring):
        permission = getpermission(permission)
    assert inspect.isclass(cls)
    assert isinstance(acl, tuple)
    assert isinstance(inherit, bool)
    assert isinstance(permission, Permission) or permission is None
    assert isinstance(owner, Principal)
    cls.__acl_decorated_init__ = cls.__init__
    cls.__acl_permission__ = permission
    chain = [acl]
    if inherit:
        for base in cls.__bases__:
            if cls.__acl_permission__ is None:
                cls.__acl_permission__ = getattr(base, '__acl_permission__', None)
            chain.append(getattr(base, '__acl__', []))

    if cls.__acl_permission__ is None:
        cls.__acl_permission__ = getpermission(('{modulename}.{classname}').format(modulename=cls.__module__, classname=cls.__name__))
    cls.__acl__ = tuple(itertools.chain(*chain))
    cls.__acl_owner__ = owner
    cls.__acl_inherit__ = inherit
    cls.__init__ = constructor
    members = dict()
    for mro in inspect.getmro(cls):
        if mro == cls:
            continue
        for name, member in inspect.getmembers(mro, inspect.ismethod):
            if name in members:
                continue
            if hasattr(member.im_func, '__acl__'):
                members[name] = (
                 member.im_func.__acl__, member.im_func.__acl_permission__)
            else:
                members[name] = (None, None)

    for name, member in inspect.getmembers(cls, inspect.ismethod):
        inherit_acl, inherit_permission = members.get(name, (None, None))
        if hasattr(member.im_func, '__acl__'):
            delattr(member.im_func, '__acl_owner__')
            member.im_func.__acl_class__ = cls
            if member.im_func.__acl_permission__ is None:
                member.im_func.__acl_permission__ = inherit_permission
            if member.im_func.__acl_inherit__ and inherit_acl:
                member.im_func.__acl__ = tuple(itertools.chain(member.im_func.__acl__, inherit_acl))
        elif inherit_acl:
            member.im_func = decorate_function(member.im_func, inherit_acl, inherit_permission, True, owner)
            member.im_func.__acl_class__ = outer

    return cls


def access(*rules, **kwargs):
    inherit = kwargs.get('inherit', True)
    permission = kwargs.get('permission', None)
    owner = kwargs.get('owner', SYSTEM)
    callback = kwargs.get('callback', None)

    def factory(outer):
        acl = list()
        for rule in rules:
            if isinstance(rule, basestring):
                acl.extend(getprovider().getnamedacl(rule))
            else:
                acl.append(Rule(*rule))

        acl = tuple(acl)
        if inspect.isclass(outer):
            return decorate_class(outer, acl, permission, inherit, owner, callback)
        if inspect.isfunction(outer):
            return decorate_function(outer, acl, permission, inherit, owner, callback)
        raise error(ValueError, getLogger('decorator'), _('Invalid decoratee: {decoratee}').format(outer))

    if len(rules) == 1 and (inspect.isclass(rules[0]) or inspect.isfunction(rules[0])) and not kwargs:
        outer = rules[0]
        rules = tuple()
        return factory(outer)
    else:
        return factory
        return