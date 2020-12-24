# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/branching.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import node

class IfThenApply(node.Node):
    """
    This node applies the function on the input data: if the outcome is true,
    then it applies the function_true function the data, otherwise the
    function_false function
    Requirements:
      condition --> condition function to be evaluated
      data --> data to be fed to the condition function and branching functions
      function_true --> function to be executed if the condition is true
      function_false --> function to be executed if the condition is false
    Eg:
      If(data=7,
         condition=lambda x: x>=0,
         function_true=lambda x: math.sqrt(x),
         function_false=lambda x: 0)
    """
    _reqs = [
     'data', 'condition', 'function_true', 'function_false']

    def output(self):
        if self._params['condition'](self._params['data']):
            return self._params['function_true'](self._params['data'])
        return self._params['function_false'](self._params['data'])


class IfThenReturn(node.Node):
    """
    This node applies the function on the input data: if the outcome is true,
    then it returns the function_true function, otherwise the
    function_false function
    Requirements:
      condition --> condition function to be evaluated
      data --> data to be fed to the condition function
      function_true --> function to be returned if the condition is true
      function_false --> function to be returned if the condition is false
    Eg:
      If(data='word',
         condition=lambda x: len(x) >= 2,
         function_true=lambda x: x[0:2],
         function_false=lambda x: x)
    """
    _reqs = [
     'data', 'condition', 'function_true', 'function_false']

    def output(self):
        if self._params['condition'](self._params['data']):
            return self._params['function_true']
        return self._params['function_false']