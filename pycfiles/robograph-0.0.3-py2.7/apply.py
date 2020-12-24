# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/apply.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import node

class Apply(node.Node):
    """
    This node executes an arbitrary function on a given argument
    Requirements:
      function --> function to be executed
      argument --> argument for the function
    Eg:
      Apply(function=lambda x: x+1, argument=8)
      Apply(function=sum, argument=[8, 13, 6])
    """
    _reqs = [
     'function', 'argument']

    def output(self):
        return self._params['function'](self._params['argument'])