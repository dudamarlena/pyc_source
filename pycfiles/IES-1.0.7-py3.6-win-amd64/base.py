# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\loaders\base.py
# Compiled at: 2018-01-14 22:14:26
# Size of source mod 2**32: 405 bytes
"""
Base class for Pipeline API data loaders.
"""
from abc import ABCMeta, abstractmethod
from six import with_metaclass

class PipelineLoader(with_metaclass(ABCMeta)):
    __doc__ = '\n    ABC for classes that can load data for use with zipline.pipeline APIs.\n\n    TODO: DOCUMENT THIS MORE!\n    '

    @abstractmethod
    def load_adjusted_array(self, columns, dates, assets, mask):
        pass