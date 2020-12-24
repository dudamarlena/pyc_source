# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/basic/xdserver.py
# Compiled at: 2008-10-01 10:39:53
from types import StringType, UnicodeType
import logging, thread, threading
logging = logging.getLogger('xooof.xmldispatcher.servers.basic')
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.servers.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *

def _checkInstanceId(instanceId):
    if not isinstance(instanceId, (StringType, UnicodeType)):
        raise TypeError, 'instanceId must be string (was %s)' % type(instanceId)
    if not instanceId:
        raise ValueError, 'instanceId must not be empty'


class XMLDispatcherContext(IXMLDispatcherContext):
    __module__ = __name__

    def __init__(self):
        self.__session = None
        self.__classFactory = PackageClassFactory.instance('bos')
        self.__userData = None
        self.__cache = {}
        return

    def setClassFactory(self, classFactory):
        self.__classFactory = classFactory

    def getSession(self):
        return self.__session

    def setSession(self, session):
        self.__session = session

    def getUserData(self):
        return self.__userData

    def setUserData(self, userData):
        self.__userData = userData

    def flushCache(self, willRollback=0):
        instances = self.__cache.values()
        self.__cache.clear()
        for instance in instances:
            instance.deactivate(willRollback)

        if len(self.__cache):
            logging.warn('Instance cache is not empty: deactivation reactivated some objects')

    def getClass(self, className):
        return self.__classFactory.getClass(className)

    def getInstance(self, className, instanceId):
        _checkInstanceId(instanceId)
        key = (className, instanceId)
        try:
            return self.__cache[key]
        except KeyError:
            instance = self.getClass(className)()
            instance.activate(instanceId)
            self.__cache[key] = instance
            return instance

    def _getNewInstance(self, className, instanceId):
        _checkInstanceId(instanceId)
        instance = self.getClass(className)()
        instance.activateNew(instanceId)
        self.__cache[(className, instanceId)] = instance
        return instance

    def notifyDestroy(self, instance):
        del self.__cache[(instance.getClassName(), instance.getInstanceId())]


class PackageClassFactory(IXMLDispatcherClassFactory):
    __module__ = __name__
    __instances = None
    __lock = threading.Lock()

    def __init__(self, packageName):
        self.__packageName = packageName

    def instance(klass, packageName):
        klass.__lock.acquire()
        try:
            if klass.__instances == None:
                klass.__instances = {}
            pCF = klass.__instances.get(packageName, PackageClassFactory(packageName))
            klass.__instances[packageName] = pCF
            return pCF
        finally:
            klass.__lock.release()
        return

    instance = classmethod(instance)

    def getClass(self, className):
        return getattr(self, className)

    def __getattr__(self, className):
        moduleName = self.__packageName + '.' + className
        try:
            module = __import__(moduleName)
            for part in moduleName.split('.')[1:]:
                module = getattr(module, part)

            klass = getattr(module, className)
        except:
            logging.error('Could not import %s' % moduleName, exc_info=1)
            raise XMLDispatcherUserException('Invalid class name: %s (see server log for details)' % className, code='XDE_DSP_NOT_A_CLASS')

        self.__dict__[className] = klass
        return klass


class Request(object):
    """Request objects hold data about an XMLDispatcher request.

    Requests are handled by a chain of RequestHandlers, each handler
    in the chain modifying the request object.

    Requests are initialized with the following attributes:
        - verb: the verb
        - appName: the application name
        - className: the business class
        - methodName: the business method
        - instanceId: the business object instance id
        - xmlRqst: the marshalled request arguments (as string, not unicode)
        - sessionData: the packed session data

    The following attributes must be set when the processing finishes:
        - xmlRply: the marshalled reply (as string, not unicode)
        - sessionData: the packed session data

    The following attributes may be set by some handlers:
        - xdCtx: the XMLDispatcherContext
        - session: the unpacked session
        - rqst: the unmarshalled request arguments
        - rply: the unmarshalled reply
    """
    __module__ = __name__


class RequestHandlerBase:
    """Base class for all request handlers."""
    __module__ = __name__

    def __init__(self, nextHandler):
        self.__nextHandler = nextHandler

    def processNext(self, request):
        """Invoke the next handler in the chain."""
        if self.__nextHandler is not None:
            self.__nextHandler.process(request)
        return

    def process(self, request):
        """Process the request and invoke the next handler in the chain."""
        self.processNext(request)


class XMLDispatcher(IXMLDispatcher):
    __module__ = __name__

    def __init__(self, appName, handlersHead, requestClass=Request):
        self.__appName = appName
        self.__handlersHead = handlersHead
        self.__requestClass = requestClass

    def _dispatch(self, verb, className, methodName, instanceId, xmlRqst, sessionData):
        request = self.__requestClass()
        request.verb = verb
        request.appName = self.__appName
        request.className = className
        request.methodName = methodName
        request.instanceId = instanceId
        request.xmlRqst = xmlRqst
        request.sessionData = sessionData
        self.__handlersHead.process(request)
        return (request.xmlRply, request.sessionData)

    def dispatchClassMethodXML(self, className, methodName, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_CLASS_METHOD, className, methodName, None, xmlRqst, sessionData)

    def dispatchNewInstanceMethodXML(self, className, methodName, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_NEW_INSTANCE_METHOD, className, methodName, None, xmlRqst, sessionData)

    def dispatchInstanceMethodXML(self, className, methodName, instanceId, xmlRqst, sessionData):
        return self._dispatch(XD_VERB_INSTANCE_METHOD, className, methodName, instanceId, xmlRqst, sessionData)