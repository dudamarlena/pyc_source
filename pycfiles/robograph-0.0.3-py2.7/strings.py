# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/strings.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import node

class TemplatedString(node.Node):
    """
    This node returns a string by filling a string template with named parameters
    Requirements:
      template --> a str template, containing named labels. Format is
      parameters --> dict with named parameters to be replaced into the template
    Eg:
      TemplatedString(template='After {p1} comes {p2}', parameters=dict(p1='one', p2='two'))
    """
    _reqs = [
     'template', 'parameters']

    def output(self):
        return self._params['template'].format(**self._params['parameters'])