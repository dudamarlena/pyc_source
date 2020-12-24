# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\Comment.py
# Compiled at: 2018-01-18 12:27:20
# Size of source mod 2**32: 1696 bytes
import logging
from .Node import Node
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Comment(Node):
    __doc__ = '\n    Class representing a XML comment\n\n    :param str data: The contents of this Comment\n    :param parent: The node to use as the parent to this node\n    :type parent: expatriate.Parent or None\n    '

    def __init__(self, data, parent=None):
        super().__init__(parent=parent)
        self.data = data

    def produce(self):
        """
        Produce an XML str (not encoded) from the contents of this
        node

        :rtype: str
        """
        return '<!--' + self.data + '-->'

    def get_string_value(self):
        """
        Return the string value of the node

        :rtype: str
        """
        return self.data

    def get_type(self):
        """
        Return the type of the node

        :rtype: str
        """
        return 'comment'