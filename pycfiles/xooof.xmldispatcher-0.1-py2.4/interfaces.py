# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/interfaces.py
# Compiled at: 2008-10-01 10:39:59


class IXMLDispatcherClassFactory:
    __module__ = __name__

    def getClass(self, className):
        pass


class IXMLDispatcherState:
    __module__ = __name__

    def getState(self):
        """Get the object state."""
        pass

    def _setState(self, state):
        """Set the object state.

        This method should not be called directly."""
        pass


class IXMLDispatcherObject:
    __module__ = __name__

    def getInstanceId(self):
        """Get the instance primary key."""
        pass

    def getClassName(self):
        """Get the business class name."""
        pass

    def activate(self, instanceId):
        """Called when an existing instance is activated.

        Activate is called before invoking the instance method,
        the first time the object is loaded during a transaction."""
        pass

    def activateNew(self, instanceId):
        """Called when an new instance is activated.

        Assume a constructor named 'create'. First 'create' is
        called as a class method; it must return the instance id.
        Then activateNew is called on a fresh instance. Then
        'postCreate' is called on the next instance."""
        pass

    def deactivate(self, willRollback):
        """Called at the end of the request."""
        pass


class IXMLDispatcherContext:
    __module__ = __name__

    def getSession(self):
        pass

    def setSession(self):
        pass

    def getUserData(self):
        pass

    def setUserData(self):
        pass

    def getClass(self, className):
        pass

    def getInstance(self, className, instanceId):
        pass

    def _getNewInstance(self, className, instanceId):
        pass

    def notifyDestroy(self, className, instanceId):
        pass

    def flushCache(self, willRollback=0):
        pass