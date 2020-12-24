# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/listener_method.py
# Compiled at: 2013-04-04 15:36:37
"""Registered event listener."""
import inspect, logging
from muntjac.util import IEventListener
from muntjac.util import getSuperClass
logger = logging.getLogger(__name__)

class ListenerMethod(IEventListener):
    """One registered event listener. This class contains the listener object
    reference, listened event type, the trigger method to call when the event
    fires, and the optional argument list to pass to the method and the index
    of the argument to replace with the event object.

    This Class provides several constructors that allow omission of the
    optional arguments, and giving the listener method directly, or having the
    constructor to reflect it using merely the name of the method.

    It should be pointed out that the method L{receiveEvent} is the one that
    filters out the events that do not match with the given event type and thus
    do not result in calling of the trigger method.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def writeObject(self, out):
        raise NotImplementedError
        try:
            out.defaultWriteObject()
            name = self._method.__name__
            paramTypes = self._method.getParameterTypes()
            out.writeObject(name)
            out.writeObject(paramTypes)
        except Exception as e:
            logger.warning('Error in serialization of the application: Class ' + self._target.__class__.__name__ + ' must implement serialization.')
            raise e

    def readObject(self, in_):
        raise NotImplementedError
        in_.defaultReadObject()
        try:
            name = in_.readObject()
            paramTypes = in_.readObject()
            self._method = self.findHighestMethod(self._target.__class__, name, paramTypes)
        except Exception:
            logger.critical('Internal deserialization error')

    @classmethod
    def findHighestMethod(cls, klass, method, paramTypes):
        ifaces = klass.getInterfaces()
        for i in range(len(ifaces)):
            ifaceMethod = cls.findHighestMethod(ifaces[i], method, paramTypes)
            if ifaceMethod is not None:
                return ifaceMethod

        if getSuperClass(klass) is not None:
            parentMethod = cls.findHighestMethod(getSuperClass(klass), method, paramTypes)
            if parentMethod is not None:
                return parentMethod
        methods = klass.getMethods()
        for i in range(len(methods)):
            if methods[i].getName() == method:
                return methods[i]

        return

    def __init__(self, eventType, target, method, arguments=None, eventArgumentIndex=None):
        """Constructs a new event listener from a trigger method, it's
        arguments and the argument index specifying which one is replaced with
        the event object when the trigger method is called.

        This constructor gets the trigger method as a parameter so it does not
        need to reflect to find it out.

        @param eventType:
                   the event type that is listener listens to. All events of
                   this kind (or its subclasses) result in calling the trigger
                   method.
        @param target:
                   the object instance that contains the trigger method
        @param method:
                   the trigger method or the name of the trigger method. If
                   the object does not contain the method a C{ValueError} is
                   thrown.
        @param arguments:
                   the arguments to be passed to the trigger method
        @param eventArgumentIndex:
                   An index to the argument list. This index points out the
                   argument that is replaced with the event object before the
                   argument set is passed to the trigger method. If the
                   eventArgumentIndex is negative, the triggering event object
                   will not be passed to the trigger method, though it is still
                   called.
        @raise ValueError:
                    if C{method} is not a member of C{target}
        """
        self._eventType = None
        self._target = None
        self._method = None
        self._arguments = None
        self._eventArgumentIndex = None
        if arguments is None:
            if isinstance(method, basestring):
                methodName = method
                method = getattr(target, methodName)
                self._eventType = eventType
                self._target = target
                self._method = methodName
                self._eventArgumentIndex = -1
                params, _, _, _ = inspect.getargspec(method)
                if len(params) == 1:
                    self._arguments = []
                elif len(params) == 2:
                    self._arguments = [
                     None]
                    self._eventArgumentIndex = 0
                else:
                    raise ValueError
            else:
                if target is not None and not issubclass(target.__class__, method.im_class):
                    raise ValueError, '%s : %s' % (target.__class__,
                     method.im_class)
                self._eventType = eventType
                self._target = target
                if target is None:
                    self._method = method
                else:
                    self._method = method.im_func.func_name
                self._eventArgumentIndex = -1
                params, _, _, _ = inspect.getargspec(method)
                nparam = len(params)
                if self._target is not None:
                    nparam = nparam - 1
                if nparam == 0:
                    self._arguments = []
                elif nparam == 1:
                    self._arguments = [
                     None]
                    self._eventArgumentIndex = 0
                else:
                    raise ValueError, 'listener takes too many arguments'
        elif eventArgumentIndex is None:
            if isinstance(method, basestring):
                methodName = method
                method = getattr(target, methodName)
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
            else:
                if target is not None and not issubclass(target.__class__, method.im_class):
                    raise ValueError, '%s : %s' % (target.__class__,
                     method.im_class)
                self._eventType = eventType
                self._target = target
                self._method = method
                self._arguments = arguments
                self._eventArgumentIndex = -1
        elif isinstance(method, basestring):
            methodName = method
            method = getattr(target, methodName)
            if eventArgumentIndex >= 0 and arguments[eventArgumentIndex] is not None:
                raise ValueError, 'event argument not None'
            self._eventType = eventType
            self._target = target
            self._method = method
            self._arguments = arguments
            self._eventArgumentIndex = eventArgumentIndex
        else:
            if target is not None and not issubclass(target.__class__, method.im_class):
                raise ValueError, '%s : %s' % (target.__class__,
                 method.im_class)
            if eventArgumentIndex >= 0 and arguments[eventArgumentIndex] is not None:
                raise ValueError, 'event argument not None'
            self._eventType = eventType
            self._target = target
            self._method = method
            self._arguments = arguments
            self._eventArgumentIndex = eventArgumentIndex
        return

    def receiveEvent(self, event):
        """Receives one event from the C{EventRouter} and calls the trigger
        method if it matches with the criteria defined for the listener. Only
        the events of the same or subclass of the specified event class result
        in the trigger method to be called.

        @param event:
                   the fired event. Unless the trigger method's argument list
                   and the index to the to be replaced argument is specified,
                   this event will not be passed to the trigger method.
        """
        if issubclass(event.__class__, self._eventType):
            if self._target is None:
                m = self._method
            else:
                m_name = self._method
                m = getattr(self._target, m_name)
            if self._eventArgumentIndex >= 0:
                if self._eventArgumentIndex == 0 and len(self._arguments) == 1:
                    m(event)
                else:
                    arg = list(self._arguments)
                    arg[self._eventArgumentIndex] = event
                    m(*arg)
            else:
                m(*self._arguments)
        return

    def matches(self, eventType, target, method=None):
        """Checks if the given object and event match with the ones stored in
        this listener.

        @param target:
                   the object to be matched against the object stored by this
                   listener.
        @param eventType:
                   the type to be tested for equality against the type stored
                   by this listener.
        @param method:
                   the method to be tested for equality against the method
                   stored by this listener.
        @return: C{True} if C{target} is the same object as
                the one stored in this object, C{eventType} equals
                with the event type stored in this object and
                C{method} equals with the method stored in this
                object
        """
        if method is None:
            return self._target == target and eventType == self._eventType
        else:
            if target is None:
                return self._target == target and eventType == self._eventType and method == self._method
            else:
                return self._target == target and eventType == self._eventType and method.im_func.func_name == self._method

            return

    def __hash__(self):
        hsh = 7
        hsh = 31 * hsh + self._eventArgumentIndex
        hsh = 31 * hsh + (0 if self._eventType is None else hash(self._eventType))
        hsh = 31 * hsh + (0 if self._target is None else hash(self._target))
        hsh = 31 * hsh + (0 if self._method is None else hash(self._method))
        return hsh

    def __eq__(self, obj):
        if obj is None or obj.__class__ != self.__class__:
            return False
        return self._eventArgumentIndex == obj._eventArgumentIndex and self._eventType == obj._eventType and self._target == obj._target and self._method == obj._method and self._arguments == obj._arguments

    def isType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType:
                   The type to compare with
        @return: true if this type of this ListenerMethod matches the given
                type, false otherwise
        """
        return self._eventType == eventType

    def isOrExtendsType(self, eventType):
        """Compares the type of this ListenerMethod to the given type

        @param eventType:
                   The type to compare with
        @return: true if this event type can be assigned to the given type,
                false otherwise
        """
        return issubclass(self._eventType, eventType)

    def getTarget(self):
        """Returns the target object which contains the trigger method.

        @return: The target object
        """
        return self._target


class MethodException(RuntimeError):
    """Exception that wraps an exception thrown by an invoked method. When
    C{ListenerMethod} invokes the target method, it may throw arbitrary
    exception. The original exception is wrapped into MethodException instance
    and rethrown by the C{ListenerMethod}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, message, cause):
        super(MethodException, self).__init__(message)
        self._cause = cause

    def getCause(self):
        """Retrieves the cause of this throwable or C{None} if the
        cause does not exist or not known.

        @return: the cause of this throwable or C{None} if the cause
                is nonexistent or unknown.
        """
        return self._cause

    def getMessage(self):
        """Returns the error message string of this throwable object.

        @return: the error message.
        @see: Exception.message
        """
        return self._message

    def __str__(self):
        msg = super(MethodException, self).__str__()
        if self._cause is not None:
            msg += '\nCause: ' + str(self._cause)
        return msg