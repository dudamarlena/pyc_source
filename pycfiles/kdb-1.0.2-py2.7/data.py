# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/data.py
# Compiled at: 2014-04-26 09:00:59
"""Data Handling"""
from attrdict import AttrDict

class Data(AttrDict):
    """An attribute access data dictionary

    An `attrdict <https://pypi.python.org/pypi/attrdict>`_
    attribute access style dictionary with a way to
    "initialize" the dictionary with another non-overriding
    dict preserving any already existing keys.
    """

    def init(self, D):
        """Data.init(D)

        Initializes ``Data`` with keys and values
        from ``D`` only if they do not already exist
        in ``Data``. Similar to ``dict.update`` but
        with non-overriding behavior. Useful for
        populating a dict with some initial data.

        :param dict D: non-overriding data to populate with
        :return: the updated dictionary
        :rtype: dict
        """
        for k, v in D.items():
            if k not in self:
                self[k] = v