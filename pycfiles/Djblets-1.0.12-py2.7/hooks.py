# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/consent/hooks.py
# Compiled at: 2019-06-12 01:17:17
"""Extension hooks for consent requirements."""
from __future__ import unicode_literals
from django.utils import six
from djblets.extensions.hooks import BaseRegistryHook, ExtensionHookPoint
from djblets.privacy.consent.registry import get_consent_requirements_registry

@six.add_metaclass(ExtensionHookPoint)
class ConsentRequirementHook(BaseRegistryHook):
    """Registers a ConsentRequirement for use of personal data."""

    @property
    def registry(self):
        """The registry that the hook interfaces with."""
        return get_consent_requirements_registry()