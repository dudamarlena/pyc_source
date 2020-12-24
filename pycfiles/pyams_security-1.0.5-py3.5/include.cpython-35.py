# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/include.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3494 bytes
"""PyAMS_security.include module

This module is used for Pyramid integration.
"""
import jwt
from zope.password.interfaces import IPasswordManager
from zope.password.password import MD5PasswordManager, PlainTextPasswordManager, SHA1PasswordManager, SSHAPasswordManager
from pyams_security.permission import register_permission
from pyams_security.plugin import PluginSelector
from pyams_security.plugin.jwt import create_jwt_token, get_jwt_claims
from pyams_security.role import RoleSelector, register_role
from pyams_security.utility import get_principal
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_security:locales')
    config.registry.registerUtility(factory=PlainTextPasswordManager, provided=IPasswordManager, name='Plain Text')
    config.registry.registerUtility(factory=MD5PasswordManager, provided=IPasswordManager, name='MD5')
    config.registry.registerUtility(factory=SHA1PasswordManager, provided=IPasswordManager, name='SHA1')
    config.registry.registerUtility(factory=SSHAPasswordManager, provided=IPasswordManager, name='SSHA')
    config.add_directive('register_permission', register_permission)
    config.add_directive('register_role', register_role)
    config.add_request_method(get_principal, 'principal', reify=True)
    config.add_request_method(create_jwt_token, 'create_jwt_token')
    config.add_request_method(get_jwt_claims, 'jwt_claims', reify=True)
    config.add_subscriber_predicate('role_selector', RoleSelector)
    config.add_subscriber_predicate('plugin_selector', PluginSelector)
    config.add_route('oauth_login', '/login/oauth/{provider_name}')
    config.add_route('jwt_login', '/login/jwt')
    try:
        import pycrypto
    except ImportError:
        pass
    else:
        from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
        jwt.unregister_algorithm('RS256')
        jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
        jwt.unregister_algorithm('RS512')
        jwt.register_algorithm('RS512', RSAAlgorithm(RSAAlgorithm.SHA512))
    try:
        import ecdsa
    except ImportError:
        pass
    else:
        from jwt.contrib.algorithms.py_ecdsa import ECAlgorithm
        jwt.unregister_algorithm('ES256')
        jwt.register_algorithm('ES256', ECAlgorithm(ECAlgorithm.SHA256))
        jwt.unregister_algorithm('ES512')
        jwt.register_algorithm('ES512', ECAlgorithm(ECAlgorithm.SHA512))
    config.scan()