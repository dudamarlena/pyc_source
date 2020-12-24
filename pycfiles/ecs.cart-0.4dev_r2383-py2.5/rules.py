# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/rules/rules.py
# Compiled at: 2009-01-13 06:18:21
"""Model class for building rules class"""

class Rules(object):
    """Rules object to manage a caddy
       Basic object, take a rule object instance in init"""

    def __init__(self, rule=None):
        self.parent_rule = rule

    def rule(self, value, *args, **kwarg):
        """ standart rule, need to be overload """
        return value

    def __call__(self, value, *args, **kwarg):
        """ this method is the motor for link all the child class """
        value = self.rule(value, *args, **kwarg)
        if self.parent_rule is not None:
            value = self.parent_rule(value, *args, **kwarg)
        return value