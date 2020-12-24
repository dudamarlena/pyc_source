# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mproxygen.py
# Compiled at: 2017-08-11 20:26:07
from mrlpy.mproxy import MProxy
import mrlpy.mcommand

def MClassFactory(qualName, methods, BaseClass=MProxy):

    def __init__(self, simpleName, name):
        BaseClass.__init__(self, simpleName, name)

    newclass = type(str(qualName), (BaseClass,), dict({'__init__': __init__}, **methods))
    return newclass


def methodListToDict(names, methods):
    if len(names) != len(methods):
        raise ValueError('The size of names and methods must be equivalent; Mapping cannot continue!')
    ret = {}
    for x in range(0, len(names) - 1):
        ret.update({names[x]: methods[x]})

    return ret


def genProxy(data):
    """
        Generate proxy service class
        """
    qualName = str(data['serviceClass'])
    simpleName = str(data['simpleName'] + '_Proxy')
    name = str(data['name'])
    methodSet = mrlpy.mcommand.callServiceWithJson(name, 'getMethodNames', [])
    methodList = map(lambda x: str(x), methodSet)
    proxyMethods = map(lambda x: lambda self, *args: mrlpy.mcommand.callService(name, x, list(args) if len(args) > 0 else None), methodList)
    methodDict = methodListToDict(methodList, proxyMethods)
    exec simpleName + ' = ' + 'MClassFactory(simpleName, methodDict)' in globals(), locals()
    exec 'instance = ' + simpleName + '(simpleName, name)' in globals(), locals()
    for methodName in methodDict:
        bind(instance, methodDict[methodName], methodName)

    return instance


bind = lambda instance, func, asname: setattr(instance, asname, func.__get__(instance, instance.__class__))