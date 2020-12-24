# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/utils/cache.py
# Compiled at: 2012-01-25 12:13:51
import time

class CachedMethod(object):
    """caches the result of a class method inside the instance
    """

    def __init__(self, method):
        if not isinstance(method, property):
            self._method = method
            self._name = method.__name__
            self._isProperty = False
        else:
            self._method = method.fget
            self._name = method.fget.__name__
            self._isProperty = True
        self._obj = None
        return

    def __get__(self, inst, cls):
        """use __get__ to get the instance object and create the attributes
        
        if it is a property call __call__
        """
        self._obj = inst
        if not hasattr(self._obj, self._name + '._data'):
            setattr(self._obj, self._name + '._data', None)
            setattr(self._obj, self._name + '._lastQueryTime', 0)
            setattr(self._obj, self._name + '._maxTimeDelta', 60)
        if self._isProperty:
            return self.__call__()
        else:
            return self
            return

    def __call__(self, *args, **kwargs):
        """
        """
        delta = time.time() - getattr(self._obj, self._name + '._lastQueryTime')
        if delta > getattr(self._obj, self._name + '._maxTimeDelta') or getattr(self._obj, self._name + '._data') is None:
            data = self._method(self._obj, *args, **kwargs)
            setattr(self._obj, self._name + '._data', data)
            setattr(self._obj, self._name + '._lastQueryTime', time.time())
        return getattr(self._obj, self._name + '._data')

    def __repr__(self):
        """Return the function's representation
        """
        objectsRepr = str(self._obj)
        objectsName = objectsRepr.split(' ')[0].split('.')[(-1)]
        cachedObjectsRepr = '<cached bound method ' + objectsName + '.' + self._name + ' of ' + objectsRepr + '>'
        return cachedObjectsRepr


class InputBasedCachedMethod(object):
    """caches the result of a class method inside the instance based on the input parameters
    """

    def __init__(self, method):
        self._method = method
        self._name = method.__name__
        self._obj = None
        return

    def __get__(self, inst, cls):
        """use __get__ just to get the instance object
        """
        self._obj = inst
        if not hasattr(self._obj, self._name + '._outputData'):
            setattr(self._obj, self._name + '._outputData', list())
            setattr(self._obj, self._name + '._inputData', list())
        return self

    def __call__(self, *args, **keys):
        """for now it uses only one argument
        """
        outputData = getattr(self._obj, self._name + '._outputData')
        inputData = getattr(self._obj, self._name + '._inputData')
        argsKeysCombined = list()
        argsKeysCombined.append(args)
        argsKeysCombined.append(keys)
        if argsKeysCombined not in inputData or outputData is None:
            data = self._method(self._obj, *args, **keys)
            inputData.append(argsKeysCombined)
            outputData.append(data)
            setattr(self._obj, self._name + '._inputdata', inputData)
            setattr(self._obj, self._name + '._outputData', outputData)
            return data
        else:
            return outputData[inputData.index(argsKeysCombined)]
            return

    def __repr__(self):
        """Return the function's repr
        """
        objectsRepr = str(self._obj)
        objectsName = objectsRepr.split(' ')[0].split('.')[(-1)]
        cachedObjectsRepr = '<cached bound method ' + objectsName + '.' + self._name + ' of ' + objectsRepr + '>'
        return cachedObjectsRepr