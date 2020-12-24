# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sessions/serializers.py
# Compiled at: 2019-02-14 00:35:16
from django.core.signing import JSONSerializer as BaseJSONSerializer
try:
    from django.utils.six.moves import cPickle as pickle
except ImportError:
    import pickle

class PickleSerializer(object):
    """
    Simple wrapper around pickle to be used in signing.dumps and
    signing.loads.
    """

    def dumps(self, obj):
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    def loads(self, data):
        return pickle.loads(data)


JSONSerializer = BaseJSONSerializer