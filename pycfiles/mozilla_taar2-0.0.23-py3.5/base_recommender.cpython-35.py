# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/recommenders/base_recommender.py
# Compiled at: 2018-02-12 11:06:15
# Size of source mod 2**32: 591 bytes
from abc import ABCMeta, abstractmethod

class BaseRecommender:
    __doc__ = 'Base class for recommenders.\n\n    Subclasses must implement can_recommend and recommend.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def can_recommend(self, client_data, extra_data={}):
        """Tell whether this recommender can recommend the given client."""
        pass

    @abstractmethod
    def recommend(self, client_data, limit, extra_data={}):
        """Return a list of recommendations for the given client."""
        pass

    def __str__(self):
        return self.__class__.__name__