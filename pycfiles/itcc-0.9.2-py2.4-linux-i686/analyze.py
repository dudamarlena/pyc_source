# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tinker/analyze.py
# Compiled at: 2008-04-20 13:19:45
from itcc.molecule import relalist
from itcc.tinker import molparam
__revision__ = '$Rev$'

def gettortype(mol, tor):
    assert len(tor) == 4
    return tuple([ mol.atoms[idx].type for idx in tor ])


def gettorsbytype(mol, types):
    types = [ molparam.torsion_uni(type_) for type_ in types ]
    result = {}
    for typ in types:
        result[typ] = []

    mol.confirmconnect()
    tors = relalist.genD(relalist.genconns(mol.connect))
    for tor in tors:
        typ = molparam.torsion_uni(gettortype(mol, tor))
        if typ in types:
            result[typ].append(tor)

    return result