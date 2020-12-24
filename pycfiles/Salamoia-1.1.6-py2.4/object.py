# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/object.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.h2o.object import Object
from salamoia.nacl.backend import Backend
from salamoia.h2o.exception import *
from salamoia.h2o.logioni import Ione
import salamoia.h2o.acl
from salamoia.h2o.attribute import *

class NACLObject(Object):
    __module__ = __name__
    hookMap = {}
    creationHooks = []
    modificationHooks = []

    def fetchOwner(self):
        if not hasattr(self, '_service'):
            return
        c = self._service
        if not c:
            return
        try:
            if not self.schema.containerClass:
                Ione.log('Root element has no owner')
                return
            res = c.fetch(self.ownerId())
            return res
        except FetchError:
            Ione.error('FEEEEEEEEETCH EEEEEEEEEEEEEEEEEERRROR')
        except:
            Ione.exception('fetchOwner EXCEPTION')

        return

    def templateFetch(self):
        Ione.log('template fetch')
        for attr in self.schema.attributes:
            initial = attr.evalInitial(self)
            if initial and (attr.required or getattr(self, attr.name)):
                Ione.log('SETTING INITIAL', attr, initial)
                setattr(self, attr.name, initial)

        return self

    def ownerId(self):
        raise NotImplementedError, 'to be overriden'

    def setIdHook(self):
        self.owner = self.fetchOwner()
        if self.owner:
            for i in self.owner.acl:
                self.acl.append(i)

    def typeSpec(self):
        raise NotImplementedError, 'to be overriden'

    def __getstate__(self):
        Ione.log('GETTING STATE for pickle')
        return self.__dict__

    def __getattr__(self, name):
        if name == '_attributes':
            state = self.__dict__
            attrs = {}
            for name in [ x for x in state if x[0] != '_' ]:
                attrs[name] = Attribute(name, state[name], self.mapAttributeType(name))

            state['_attributes'] = attrs
            return attrs
        try:
            return self.__dict__[name]
        except:
            raise AttributeError, name


from salamoia.tests import *
runDocTests()