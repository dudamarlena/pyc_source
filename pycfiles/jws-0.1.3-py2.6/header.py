# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/jws/header.py
# Compiled at: 2015-03-10 10:18:32
from __future__ import absolute_import
import jws.algos as algos
from .exceptions import AlgorithmNotImplemented, ParameterNotImplemented, ParameterNotUnderstood, RouteMissingError

class HeaderBase(object):

    def __init__(self, name, value, data):
        self.name = name
        self.value = self.clean(value)
        self.data = data

    def sign(self):
        return self.value

    def verify(self):
        return self.value

    def clean(self, value):
        return value


class GenericString(HeaderBase):

    def clean(self, value):
        return str(value)


class SignNotImplemented(HeaderBase):

    def sign(self):
        raise ParameterNotImplemented('Header Parameter %s not implemented in the context of signing' % self.name)


class VerifyNotImplemented(HeaderBase):

    def verify(self):
        raise ParameterNotImplemented('Header Parameter %s not implemented in the context of verifying' % self.name)


class NotImplemented(HeaderBase):

    def clean(self, *a):
        raise ParameterNotUnderstood("Could not find an action for Header Parameter '%s'" % self.name)


class Algorithm(HeaderBase):

    def clean(self, value):
        try:
            self.methods = algos.route(value)
        except RouteMissingError, e:
            raise AlgorithmNotImplemented('"%s" not implemented.' % value)

    def sign(self):
        self.data['signer'] = self.methods['sign']

    def verify(self):
        self.data['verifier'] = self.methods['verify']


KNOWN_HEADERS = {'alg': Algorithm, 
   'typ': GenericString, 
   'jku': VerifyNotImplemented, 
   'kid': VerifyNotImplemented, 
   'x5u': VerifyNotImplemented, 
   'x5t': VerifyNotImplemented}

def process(data, step):
    for param in data['header']:
        cls = KNOWN_HEADERS.get(param, NotImplemented)
        instance = cls(param, data['header'][param], data)
        procedure = getattr(instance, step)
        procedure()

    return data