# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/logics.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import apply

class Not(apply.Apply):
    """
    This node negates the truth value of the items of an argument sequence
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=lambda predicates: map(lambda x: not x, predicates), argument=args.get('argument', None), name=args.get('name', None))
        return


class And(apply.Apply):
    """
    This node performs a logical AND on the items of an argument sequence
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=lambda predicates: reduce(lambda p1, p2: p1 and p2, predicates), argument=args.get('argument', None), name=args.get('name', None))
        return


class Or(apply.Apply):
    """
    This node performs a logical OR on the items of an argument sequence
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=lambda predicates: reduce(lambda p1, p2: p1 or p2, predicates), argument=args.get('argument', None), name=args.get('name', None))
        return


class All(apply.Apply):
    """
    This node tells if all the items of the argument sequence have a truth value
    of true
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=all, argument=args.get('argument', None), name=args.get('name', None))
        return


class Nil(apply.Apply):
    """
    This node tells if all the items of the argument sequence have a truth value
    of false
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=lambda predicates: not any(predicates), argument=args.get('argument', None), name=args.get('name', None))
        return


class Any(apply.Apply):
    """
    This node tells if at least one item in the argument sequence has a truth value
    of true
    """

    def __init__(self, **args):
        apply.Apply.__init__(self, function=any, argument=args.get('argument', None), name=args.get('name', None))
        return