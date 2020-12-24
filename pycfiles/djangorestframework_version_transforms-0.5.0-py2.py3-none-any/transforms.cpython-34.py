# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matthardwick/workspace/drf-representation-transforms/django-rest-framework-version-transforms/rest_framework_transforms/transforms.py
# Compiled at: 2015-10-31 16:18:50
# Size of source mod 2**32: 930 bytes


class BaseTransform(object):
    __doc__ = "\n    All transforms should extend 'BaseTransform', overriding the two\n    methods '.forwards()' and '.backwards()' to provide forwards and backwards\n    conversions between representation versions.\n    "

    def forwards(self, data, request):
        """
        Converts from this transform's base version to the targeted version of the representation.

        :returns: Dictionary with the correct structure for the targeted version of the representation.
        """
        raise NotImplementedError('.forwards() must be overridden.')

    def backwards(self, data, request, instance):
        """
        Converts from the targeted version back to this transform's base version of the representation.

        :returns: Dictionary with the correct structure for the base version of the representation.
        """
        raise NotImplementedError('.backwards() must be overridden.')