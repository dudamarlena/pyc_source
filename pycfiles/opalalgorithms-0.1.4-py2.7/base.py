# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opalalgorithms/core/base.py
# Compiled at: 2018-04-24 11:50:48
"""Base class for implementing any algorithms for OPAL computation."""

class OPALAlgorithm(object):
    """Base class for OPAL Algorithms.

    The class can be used in the following way::

        algo = OPALAlgorithm()
        result = algo.map(params, bandicoot_user)

    """

    def __init__(self):
        """Initialize the base class."""
        pass

    def map(self, params, bandicoot_user):
        """Map users data to a single result.

        Args:
            params(dict): Parameters to be used by each map of the algorithm.
            bandicoot_user (bandicoot.user): `Bandicoot user <http://
                bandicoot.mit.edu/docs/reference/generated/bandicoot.User.html#bandicoot.User>`_.

        Returns:
            dict: A dictionary representing with keys as string or tuple, and
            values as int or float which will be aggregated by the reducer.

        """
        raise NotImplementedError