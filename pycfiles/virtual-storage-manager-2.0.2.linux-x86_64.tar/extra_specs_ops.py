# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/scheduler/filters/extra_specs_ops.py
# Compiled at: 2016-06-13 14:11:03
import operator
from vsm.openstack.common import strutils
_op_methods = {'=': lambda x, y: float(x) >= float(y), 
   '<in>': lambda x, y: y in x, 
   '<is>': lambda x, y: strutils.bool_from_string(x) is strutils.bool_from_string(y), 
   '==': lambda x, y: float(x) == float(y), 
   '!=': lambda x, y: float(x) != float(y), 
   '>=': lambda x, y: float(x) >= float(y), 
   '<=': lambda x, y: float(x) <= float(y), 
   's==': operator.eq, 
   's!=': operator.ne, 
   's<': operator.lt, 
   's<=': operator.le, 
   's>': operator.gt, 
   's>=': operator.ge}

def match(value, req):
    words = req.split()
    op = method = None
    if words:
        op = words.pop(0)
        method = _op_methods.get(op)
    if op != '<or>' and not method:
        return value == req
    else:
        if value is None:
            return False
        if op == '<or>':
            while True:
                if words.pop(0) == value:
                    return True
                if not words:
                    break
                op = words.pop(0)
                if not words:
                    break

            return False
        try:
            if words and method(value, words[0]):
                return True
        except ValueError:
            pass

        return False