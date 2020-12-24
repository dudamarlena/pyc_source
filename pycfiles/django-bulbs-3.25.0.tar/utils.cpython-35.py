# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/super_features/utils.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 2578 bytes
from importlib import import_module
from django.conf import settings

def get_superfeature_model():
    module = getattr(settings, 'BULBS_SUPERFEATURE_MODEL_MODULE', None)
    model = getattr(settings, 'BULBS_SUPERFEATURE_MODEL', None)
    if model is None or module is None:
        from bulbs.super_features.models import BaseSuperFeature
        return BaseSuperFeature
    else:
        mod = import_module(module)
        return getattr(mod, model)


def get_superfeature_serializer():
    module = getattr(settings, 'BULBS_SUPERFEATURE_SERIALIZER_MODULE', None)
    serializer = getattr(settings, 'BULBS_SUPERFEATURE_SERIALIZER', None)
    if serializer is None or module is None:
        from bulbs.super_features.serializers import BaseSuperFeatureSerializer
        return BaseSuperFeatureSerializer
    else:
        mod = import_module(module)
        return getattr(mod, serializer)


def get_superfeature_partial_serializer():
    module = getattr(settings, 'BULBS_SUPERFEATURE_SERIALIZER_MODULE', None)
    serializer = getattr(settings, 'BULBS_SUPERFEATURE_PARTIAL_SERIALIZER', None)
    if serializer is None or module is None:
        from bulbs.super_features.serializers import BaseSuperFeaturePartialSerializer
        return BaseSuperFeaturePartialSerializer
    else:
        mod = import_module(module)
        return getattr(mod, serializer)


def get_superfeature_metadata():
    module = getattr(settings, 'BULBS_SUPERFEATURE_METADATA_MODULE', None)
    metadata = getattr(settings, 'BULBS_SUPERFEATURE_METADATA', None)
    if metadata is None or module is None:
        from bulbs.super_features.metadata import BaseSuperFeatureMetadata
        return BaseSuperFeatureMetadata
    else:
        mod = import_module(module)
        return getattr(mod, metadata)


def get_superfeature_choices():
    from bulbs.super_features.models import BASE_CHOICES
    configured_superfeatures = getattr(settings, 'BULBS_CUSTOM_SUPERFEATURE_CHOICES', ())
    for sf in configured_superfeatures:
        if type(sf[0]) is not str or type(sf[1]) is not str:
            raise ValueError('Super Feature choices must be a string. {0} is not valid'.format(sf))

    return BASE_CHOICES + configured_superfeatures