# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cacore/ws/proxy.py
# Compiled at: 2010-06-24 14:29:31


class WSBean(object):

    def __init__(self, holder, service=None, **kwargs):
        self.cache = {}
        self.holder = holder
        self.service = service
        for k in kwargs:
            if k in self.__class__.__dict__:
                setattr(self, k, kwargs[k])
            else:
                raise AttributeError("'%s' has no attribute '%s'" % (self.className, k))


class ProxyAttr(object):

    def __init__(self, name):
        self.name = name
        self.uname = name[0].capitalize() + name[1:]

    def __get__(self, obj, type=None):
        return getattr(obj.holder, self.uname)

    def __set__(self, obj, value):
        setattr(obj.holder, self.uname, value)

    def __delete__(self, obj):
        raise AttributeError('Cannot delete attributes in proxy')


class ProxyAssoc(object):

    def __init__(self, name, isCollection):
        self.name = name
        self.uname = name[0].capitalize() + name[1:]
        self.isCollection = isCollection

    def getAssociation(self, obj, associationName):
        if not obj.service:
            raise Exception('Object is not bound to a service. Retrieve the ' + 'object instance from a service first.')
        if 'getAssociation' not in dir(obj.service):
            raise Exception('This service does not support the getAssociation method.')
        ret = obj.service.getAssociation(obj, associationName, 0)
        if self.isCollection:
            return ret
        else:
            if not ret:
                return None
            if len(ret) > 1:
                raise Exception("Expected single object for '%s' but got collection." % associationName)
            return ret[0]

    def __get__(self, obj, type=None):
        if obj.cache.has_key(self.name):
            return obj.cache[self.name]
        arrayHolder = getattr(obj.holder, self.uname)
        if arrayHolder:
            if self.isCollection:
                assoc = [ obj.service.wrap(i) for i in arrayHolder.get_element_item() ]
            else:
                assoc = obj.service.wrap(arrayHolder)
        else:
            assoc = self.getAssociation(obj, self.name)
        obj.cache[self.name] = assoc
        return assoc

    def __set__(self, obj, value):
        obj.cache[self.name] = value
        if self.isCollection:
            array = obj.arrayType()
            array.Item = [ v.holder for v in value ]
            setattr(obj.holder, self.uname, array)
        else:
            setattr(obj.holder, self.uname, value.holder)

    def __delete__(self, obj):
        del obj.cache[self.name]