# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/PyNOAAGeoMagIndiceHandler/decorator.py
# Compiled at: 2012-09-18 11:22:18


def DictAssign(DictName, KeyNode=None):
    """
    This Decorator will create a Byteplay Statck known to Add Exception List in head of
    decorated function... Instead of adding raiser ( NotImplementedYet, Is ready ) This byteplay decorator
    will add it naturally, By playing with StackModule Level implemented close to here...

    See instruction on http://pypi.python.org/pypi/byteplay/N.N = ( 0.2 )

    The marshaller computes a key from function arguments
    """

    def decorator(func):

        def inner(*args, **kwargs):
            if KeyNode == None:
                kwargs.update(MainDict=getattr(self, DictName))
            func(*args, **kwargs)
            return

        return inner

    return decorator