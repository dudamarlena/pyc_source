# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/registries/mixins.py
# Compiled at: 2019-06-12 01:17:17
"""Utility mixins for registries."""
from __future__ import unicode_literals
from djblets.registries.errors import ItemLookupError

class ExceptionFreeGetterMixin(object):
    """A mixin that prevents lookups from throwing errors."""

    def get(self, attr_name, attr_value):
        """Return the requested registered item.

        Args:
            attr_name (unicode):
                The attribute name.

            attr_value (object):
                The attribute value.

        Returns:
            object:
            The matching registered item, if found. Otherwise, ``None`` is
            returned.
        """
        try:
            return super(ExceptionFreeGetterMixin, self).get(attr_name, attr_value)
        except ItemLookupError:
            return

        return