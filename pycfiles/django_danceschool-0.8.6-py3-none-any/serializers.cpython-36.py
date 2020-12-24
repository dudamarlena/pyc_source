# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/utils/serializers.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 831 bytes
from dynamic_preferences.serializers import BaseSerializer, UNSET

class PageModelSerializer(BaseSerializer):
    __doc__ = "\n    The Page selector field needs its own serializer, which accepts a Page object,\n    but returns an int.  So, when accessing the value of the DefaultAdminSuccessPage\n    constant, one must use Page.objects.get(pk=getConstant('general__defaultAdminSuccessPage')).\n     "

    @classmethod
    def to_python(cls, value, **kwargs):
        if not value or value == UNSET:
            return
        try:
            return int(value)
        except ValueError:
            raise cls.exception('Value {0} cannot be converted to int')

    @classmethod
    def to_db(cls, value, **kwargs):
        if not value or value == UNSET:
            return
        else:
            return str(value.pk)