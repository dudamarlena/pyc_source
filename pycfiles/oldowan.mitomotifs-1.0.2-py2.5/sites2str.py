# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-ppc/egg/oldowan/mitomotifs/sites2str.py
# Compiled at: 2008-08-24 10:54:34
from types import StringType, ListType
from seq2sites import Polymorphism

def sites2str(sites):
    """Transform a list of Polymorphisms to a string.

    """
    processing = []
    for x in sites:
        if isinstance(x, Polymorphism):
            processing.append(str(x))
        elif type(x) == ListType:
            current = []
            for y in x:
                if type(y) == ListType:
                    if len(y) == 1:
                        current.append(str(y[0]))
                    elif len(y) > 1:
                        as_str = list((str(x) for x in y))
                        interior = (' ').join(as_str)
                        current.append('(' + interior + ')')
                    else:
                        raise Exception('format error in sites2str')
                else:
                    raise Exception('format error in sites2str')

            interior = (' or ').join(current)
            processing.append('(' + interior + ')')
        else:
            raise Exception('format error in sites2str')

    return (' ').join(processing)