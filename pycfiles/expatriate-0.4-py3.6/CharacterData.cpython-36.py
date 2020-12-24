# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\CharacterData.py
# Compiled at: 2018-01-18 12:27:16
# Size of source mod 2**32: 2382 bytes
import logging
from .Node import Node
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CharacterData(Node):
    __doc__ = '\n    Class representing XML character data\n\n    :param str data: The contents of this CharacterData\n    :param bool cdata_block: True if this CharacterData should be generated with CDATA block wrapping\n    :param parent: The node to use as the parent to this node\n    :type parent: expatriate.Parent or None\n    '

    def __init__(self, data, cdata_block=False, parent=None):
        super().__init__(parent=parent)
        self.data = data
        self.cdata_block = cdata_block

    def produce(self):
        """
        Produce an XML str (not encoded) from the contents of this
        node

        :rtype: str
        """
        s = ''
        if self.cdata_block:
            s += '<![CDATA[' + self.data.replace(']]>', ']]&gt;') + ']]>'
        else:
            s += self.escape(self.data)
        return s

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
        return 'text'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.data == other
        else:
            if isinstance(other, int) or isinstance(other, float) or isinstance(other, bool):
                return self.data == str(other)
            return object.__eq__(self, other)