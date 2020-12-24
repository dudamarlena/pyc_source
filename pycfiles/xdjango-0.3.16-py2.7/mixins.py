# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/rest_framework/mixins.py
# Compiled at: 2016-06-05 11:22:58
from django.http import Http404

class SecureGetObjectMixin(object):
    """
    Secure get object avoiding information leaks.
    """

    def get_object(self):
        try:
            return super(SecureGetObjectMixin, self).get_object()
        except:
            raise Http404