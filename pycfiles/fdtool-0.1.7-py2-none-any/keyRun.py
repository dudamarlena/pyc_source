# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\keyRun.py
# Compiled at: 2018-06-19 13:38:40
from dbschema import dbschema
from string import ascii_lowercase

def f(U, alphaString, FD_Store):
    FD_Str = (',').join([ ('').join([str(k[0]), '->', str(k[1])]) for k in FD_Store ])
    dbschemaNotation = (
     alphaString, FD_Str)
    attrastxt, abhastxt = dbschemaNotation
    attrs, abhh = dbschema.ScanAttrAbh(attrastxt, abhastxt)
    abhh = dbschema.mincoverage(abhh)
    primattr, keys = dbschema.keysTreeAlg(attrs, abhh, 2)
    KeyList = map(dbschema.attr2str, keys)
    Column_Dict = {ascii_lowercase.upper()[i]:U[i] for i in range(len(U))}
    KeyList = [ str('{' + (', ').join([ Column_Dict[char] for char in KeyList[k] ]) + '}') for k in range(len(KeyList)) ]
    return KeyList