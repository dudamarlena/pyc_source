# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/include.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 1631 bytes
"""PyAMS_apm.include module

This module is used for Pyramid integration
"""
import elasticapm
from elasticapm.instrumentation import register
from pyramid.events import subscriber
from pyramid.interfaces import IApplicationCreated
__docformat__ = 'restructuredtext'

@subscriber(IApplicationCreated)
def handle_apm_application(event):
    """Register custom instrumentations on application startup"""
    register.register('pyams_apm.packages.ldap3.LDAP3OpenInstrumentation')
    register.register('pyams_apm.packages.ldap3.LDAP3BindInstrumentation')
    register.register('pyams_apm.packages.ldap3.LDAP3SearchInstrumentation')
    register.register('pyams_apm.packages.ldap3.LDAP3GetResponseInstrumentation')
    register.register('pyams_apm.packages.chameleon.ChameleonCookingInstrumentation')
    register.register('pyams_apm.packages.chameleon.ChameleonRenderingInstrumentation')
    elasticapm.instrument()


def include_package(config):
    """Pyramid package include"""
    config.add_tween('pyams_apm.tween.elastic_apm_tween_factory')
    config.scan()