# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/configuration/node.py
# Compiled at: 2014-01-08 15:34:56
import logging
log = logging.getLogger(__name__)
__all__ = [
 'Node']

class Node(object):
    """
                Node oject for acls
        """

    def __init__(self, perm, add):
        super(Node, self).__init__()
        self.attrs = {'type': perm, 'cidr': add}

    def todict(self):
        """
                        Create a dict so it can be converted/serialized
                """
        return {'tag': 'node', 'attrs': self.attrs}