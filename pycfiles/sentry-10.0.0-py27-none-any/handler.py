# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/features/handler.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
__all__ = ['FeatureHandler']

class FeatureHandler(object):
    features = set()

    def __call__(self, feature, actor):
        if feature.name not in self.features:
            return None
        else:
            return self.has(feature, actor)

    def has(self, feature, actor):
        raise NotImplementedError