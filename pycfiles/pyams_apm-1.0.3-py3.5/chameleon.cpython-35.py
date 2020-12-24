# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/packages/chameleon.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 2147 bytes
"""PyAMS_apm.packages.chameleon module

This module adds APM instrumentation for Chameleon package
"""
from elasticapm.instrumentation.packages.base import AbstractInstrumentedModule
from elasticapm.traces import capture_span
__docformat__ = 'restructuredtext'

class ChameleonCookingInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'Chameleon cooking instrumentation'
    name = 'chameleon_cooking'
    instrument_list = [
     ('chameleon.template', 'BaseTemplate.cook')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('COOK', span_type='template', span_subtype='chameleon', span_action='cook', extra={'filename': instance.filename}, leaf=False):
            return wrapped(*args, **kwargs)


class ChameleonRenderingInstrumentation(AbstractInstrumentedModule):
    __doc__ = 'Chameleon rendering instrumentation'
    name = 'chameleon_rendering'
    instrument_list = [
     ('chameleon.template', 'BaseTemplate.render')]

    def call(self, module, method, wrapped, instance, args, kwargs):
        """Wrapped method call"""
        with capture_span('RENDER', span_type='template', span_subtype='chameleon', span_action='render', extra={'filename': instance.filename}, leaf=False):
            return wrapped(*args, **kwargs)