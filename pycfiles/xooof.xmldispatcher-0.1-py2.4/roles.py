# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/tools/roles.py
# Compiled at: 2008-10-01 10:39:52
from xml.sax import ContentHandler

class IRoleChecker:
    __module__ = __name__
    rcsOneByOne = 1
    rcsAllAtOnce = 2

    def getPreferredStrategy(self):
        raise RuntimeError, 'getPreferredStrategy must be implemented by subclass'

    def isUserInOneRole(self, xdCtx, roles):
        raise RuntimeError, 'isUserInOneRole must be implemented by subclass'


class IRoleDefs:
    __module__ = __name__

    def isAllowedByRole(self, xdCtx, roleChecker, className, methodName, stateName=None):
        """Check that the call is allowed by the role-based security

           Note: roleChecker must implement IRoleChecker.
        """
        raise RuntimeError, 'isAllowedByRole must be implemented by subclass'


class SimpleRoleDefs(IRoleDefs):
    __module__ = __name__

    def __init__(self):
        self.reset()

    def reset(self):
        self.__applicationRoles = []
        self.__classRoles = {}
        self.__methodRoles = {}
        self.__transitionRoles = {}

    def allowApplication(self, role):
        self.__applicationRoles.append(role)

    def allowClass(self, role, className):
        self.__classRoles.setdefault(className, []).append(role)

    def allowMethod(self, role, className, methodName):
        self.__methodRoles.setdefault((className, methodName), []).append(role)

    def allowTransition(self, role, className, methodName, stateName):
        self.__transitionRoles.setdefault((className, methodName, stateName), []).append(role)

    def isAllowedByRole(self, xdCtx, roleChecker, className, methodName, stateName=None):
        allRoles = []
        rcs = roleChecker.getPreferredStrategy()
        assert rcs in (IRoleChecker.rcsOneByOne, IRoleChecker.rcsAllAtOnce)
        roles = self.__applicationRoles
        if rcs == IRoleChecker.rcsOneByOne:
            if roleChecker.isUserInOneRole(xdCtx, roles):
                return 1
        else:
            allRoles += roles
        try:
            roles = self.__classRoles[className]
        except KeyError:
            pass
        else:
            if rcs == IRoleChecker.rcsOneByOne:
                if roleChecker.isUserInOneRole(xdCtx, roles):
                    return 1
            else:
                allRoles += roles

        try:
            roles = self.__methodRoles[(className, methodName)]
        except KeyError:
            pass
        else:
            if rcs == IRoleChecker.rcsOneByOne:
                if roleChecker.isUserInOneRole(xdCtx, roles):
                    return 1
            else:
                allRoles += roles

        if stateName:
            try:
                roles = self.__transitionRoles[(className, methodName, stateName)]
            except KeyError:
                pass
            else:
                if rcs == IRoleChecker.rcsOneByOne:
                    if roleChecker.isUserInOneRole(xdCtx, roles):
                        return 1
                else:
                    allRoles += roles
        if rcs == IRoleChecker.rcsAllAtOnce and len(allRoles):
            if roleChecker.isUserInOneRole(xdCtx, allRoles):
                return 1
        return 0


class SimpleRoleDefsLoaderSAXHandler(ContentHandler):
    """Populate a SimpleRoleDefs instance from a SAX stream

       Assumes the SAX events are from a valid roles.dtd instance.
    """
    __module__ = __name__

    def __init__(self, roleDefs):
        self.roleDefs = roleDefs
        self.__callCtx = []

    def _push(self, callable, args):
        self.__callCtx.insert(0, (callable, args))

    def _pop(self):
        del self.__callCtx[0]

    def _top(self):
        return self.__callCtx[0]

    def startElement(self, name, atts):
        if name == 'application':
            args = ()
            self._push(self.roleDefs.allowApplication, args)
        elif name == 'class':
            args = self._top()[1] + (str(atts['name']),)
            self._push(self.roleDefs.allowClass, args)
        elif name == 'method':
            args = self._top()[1] + (str(atts['name']),)
            self._push(self.roleDefs.allowMethod, args)
        elif name == 'state':
            args = self._top()[1] + (str(atts['name']),)
            self._push(self.roleDefs.allowTransition, args)
        elif name == 'role-ref':
            (callable, args) = self._top()
            apply(callable, (str(atts['name']),) + args)

    def endElement(self, name):
        if name in ('application', 'class', 'method', 'state'):
            self._pop()