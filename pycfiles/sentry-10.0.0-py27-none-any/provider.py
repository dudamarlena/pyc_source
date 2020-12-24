# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/identity/vsts_extension/provider.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.identity.vsts.provider import VSTSIdentityProvider

class VstsExtensionIdentityProvider(VSTSIdentityProvider):
    """
    Functions exactly the same as ``VSTSIdentityProvider``.

    This class is necessary because of how Integration Pipelines look up
    sibling/dependent classes using ``key``.

    The IntegrationProvider for the VSTS Extension is slightly different from
    the VSTS version, so it requires a new class. Hence, the Identity portion
    also requires a new class; this one.
    """
    key = 'vsts-extension'