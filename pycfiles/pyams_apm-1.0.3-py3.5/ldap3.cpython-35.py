# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/packages/ldap3.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 2877 bytes
"""PyAMS_apm.packages.ldap3 module

This module adds APM instrumentation to LDAP3 package
"""
from elasticapm.instrumentation.packages.base import AbstractInstrumentedModule
from elasticapm.traces import capture_span
__docformat__ = 'restructuredtext'

class LDAP3OpenInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'LDAP3 connection opening instrumentation'
    name = 'ldap.open'
    instrument_list = [
     ('ldap3.strategy.base', 'BaseStrategy.open'),
     ('ldap3.strategy.reusable', 'ReusableStrategy.open')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.OPEN', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3BindInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'LDAP3 bind instrumentation'
    name = 'ldap.bind'
    instrument_list = [
     ('ldap3', 'Connection.bind')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.BIND', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3SearchInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'LDAP3 search instrumentation'
    name = 'ldap.search'
    instrument_list = [
     ('ldap3', 'Connection.search')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.SEARCH', 'db.ldap', {'db': {'type': 'ldap', 
                'statement': kwargs.get('search_filter') or args[1]}}, leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3GetResponseInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'LDAP3 response getter instrumentation'
    name = 'ldap.get_response'
    instrument_list = [
     ('ldap3.strategy.base', 'BaseStrategy.get_response'),
     ('ldap3.strategy.reusable', 'ReusableStrategy.get_response')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.GET_RESPONSE', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)