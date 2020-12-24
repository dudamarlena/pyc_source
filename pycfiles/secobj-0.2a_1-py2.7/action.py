# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/action.py
# Compiled at: 2012-08-22 05:53:48
from abc import ABCMeta, abstractmethod
from secobj.exceptions import UnknownActionError
from secobj.localization import _

class Action(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def allowed(self, subject, resource, *permissions):
        raise NotImplementedError

    def denied(self, subject, resource, *permissions):
        return not self.allowed(subject, resource, *permissions)


class Allow(Action):

    def allowed(self, subject, resource, *permissions):
        return True

    def __str__(self):
        return 'allow'

    def __repr__(self):
        return '<secobj.action.Allow>'

    def __eq__(self, other):
        if isinstance(other, Allow):
            return True
        if isinstance(other, Action):
            return False
        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, Allow):
            return False
        if isinstance(other, Action):
            return True
        raise NotImplementedError


ALLOW = Allow()

class Deny(Action):

    def allowed(self, subject, resource, *permissions):
        return False

    def __str__(self):
        return 'deny'

    def __repr__(self):
        return '<secobj.action.Deny>'

    def __eq__(self, other):
        if isinstance(other, Deny):
            return True
        if isinstance(other, Action):
            return False
        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, Deny):
            return False
        if isinstance(other, Action):
            return True
        raise NotImplementedError


DENY = Deny()

def getaction(name):
    if name.upper() == 'ALLOW':
        return ALLOW
    if name.upper() == 'DENY':
        return DENY
    raise UnknownActionError, _('Invalid action name: {name}').format(name)