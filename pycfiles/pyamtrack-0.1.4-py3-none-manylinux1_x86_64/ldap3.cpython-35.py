# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/packages/ldap3.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 2877 bytes
__doc__ = 'PyAMS_apm.packages.ldap3 module\n\nThis module adds APM instrumentation to LDAP3 package\n'
from elasticapm.instrumentation.packages.base import AbstractInstrumentedModule
from elasticapm.traces import capture_span
__docformat__ = 'restructuredtext'

class LDAP3OpenInstrumentation(AbstractInstrumentedModule):
    """LDAP3OpenInstrumentation"""
    name = 'ldap.open'
    instrument_list = [
     ('ldap3.strategy.base', 'BaseStrategy.open'),
     ('ldap3.strategy.reusable', 'ReusableStrategy.open')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.OPEN', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3BindInstrumentation(AbstractInstrumentedModule):
    """LDAP3BindInstrumentation"""
    name = 'ldap.bind'
    instrument_list = [
     ('ldap3', 'Connection.bind')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.BIND', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3SearchInstrumentation(AbstractInstrumentedModule):
    """LDAP3SearchInstrumentation"""
    name = 'ldap.search'
    instrument_list = [
     ('ldap3', 'Connection.search')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.SEARCH', 'db.ldap', {'db': {'type': 'ldap', 
                'statement': kwargs.get('search_filter') or args[1]}}, leaf=True):
            return wrapped(*args, **kwargs)


class LDAP3GetResponseInstrumentation(AbstractInstrumentedModule):
    """LDAP3GetResponseInstrumentation"""
    name = 'ldap.get_response'
    instrument_list = [
     ('ldap3.strategy.base', 'BaseStrategy.get_response'),
     ('ldap3.strategy.reusable', 'ReusableStrategy.get_response')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('LDAP.GET_RESPONSE', 'db.ldap', leaf=True):
            return wrapped(*args, **kwargs)