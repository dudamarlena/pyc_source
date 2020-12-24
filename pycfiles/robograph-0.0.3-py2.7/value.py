# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/value.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import node

class Value(node.Node):
    """
    This node returns an arbitrary value.
    Requirements:
      value --> any Python datatype
    Eg:
      Value(value=dict(number=3))
      Value(value=dict(int_list=[1, 6, 9]))
      Value(value=dict(word1='blabla', word2='bleble'))
    """
    _reqs = [
     'value']

    def output(self):
        return self._params['value']