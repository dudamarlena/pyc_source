# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/checkpermission/check.py
# Compiled at: 2009-11-06 11:57:19
from AccessControl import Unauthorized
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getMultiAdapter
from collective.checkpermission.interfaces import ICheckPermission

class CheckPermission(object):
    __module__ = __name__
    implements(ICheckPermission)
    adapts(Interface, Interface)

    def __init__(self, context, view):
        self.context = context
        self.view = view

    def check(self, permission):
        """ """
        membership = getMultiAdapter((self.context, self.context.REQUEST), name='plone_tools').membership()
        if membership.checkPermission(permission, self.context):
            return True
        return False


def check_permission(perm):
    """
      You can decorate your browser view methods adding a:
      @check_permission('Modify portal content')
      This should check you against the given permission.
      If you don't have such permission on the given context an
      Unauthorized exception will be raised.
      This way you can protect your browser view methods.

      >>> 2+2
      4

    """

    def decorator(fun):

        def replacement(*args, **kwargs):
            view = args[0]
            context = view.context
            adapted = getMultiAdapter((context, view), name='check_permission')
            if adapted:
                if adapted.check(perm):
                    return fun(*args, **kwargs)
            raise Unauthorized("You don't have the %s permission on %s" % (perm, context.absolute_url()))

        return replacement

    return decorator