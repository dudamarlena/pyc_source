# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/permission.py
# Compiled at: 2012-08-22 03:32:54
import re
from secobj.localization import _
NAME = re.compile('^[a-zA-Z0-9_][a-zA-Z0-9_\\.]*$')

def getpermission(value):
    if isinstance(value, basestring):
        return Permission.get(value)
    if isinstance(value, Permission):
        return value
    raise ValueError, _('Invalid permission')


class PermissionMeta(type):

    def __call__(cls, *args, **kwargs):
        raise NotImplementedError, 'Permissions may only be instantiated through get()'


class Permission(object):
    __metaclass__ = PermissionMeta
    _permissions = dict()

    def __new__(cls, *args, **kwargs):
        return super(Permission, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name):
        assert isinstance(name, basestring)
        if NAME.match(name) is None:
            raise ValueError, _('Invalid permission name: {name}').format(name=name)
        self._name = name
        return

    @classmethod
    def get(cls, name, *args, **kwargs):
        try:
            return cls._permissions[name]
        except KeyError:
            if 'instanceclass' in kwargs:
                instanceclass = kwargs['instanceclass']
                if not issubclass(instanceclass, Permission):
                    raise TypeError, _('Must be a subclass of Permission')
                del kwargs['instanceclass']
            else:
                instanceclass = Permission
            instance = instanceclass.__new__(instanceclass, *args, **kwargs)
            instance.__init__(name, *args, **kwargs)
            cls._permissions[name] = instance
            return instance

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return ('<secobj.permission.Permission: {name}>').format(name=self._name)

    def __eq__(self, other):
        if isinstance(other, basestring):
            other = getpermission(other)
        if isinstance(other, AllPermission):
            return True
        if isinstance(other, Permission):
            return self._name == other._name
        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, basestring):
            other = getpermission(other)
        if isinstance(other, AllPermission):
            return False
        if isinstance(other, Permission):
            return self._name != other.__name
        raise NotImplementedError


class AllPermission(Permission):

    def __repr__(self):
        return '<secobj.permission.AllPermission>'

    def __eq__(self, other):
        if isinstance(other, basestring):
            other = getpermission(other)
        if isinstance(other, Permission):
            return True
        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, basestring):
            other = getpermission(other)
        if isinstance(other, Permission):
            return False
        raise NotImplementedError


ALL = Permission.get('all', instanceclass=AllPermission)