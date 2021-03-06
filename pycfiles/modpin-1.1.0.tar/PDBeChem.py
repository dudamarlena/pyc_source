# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/src/archdb/src/PDBeChem.py
# Compiled at: 2018-02-02 06:39:02
from SBI.data import Element, element_dic
from SBI.databases import PDBeChem
tables = {'hetero': 'hetero', 'hparent': 'hetero_parent', 
   'formula': 'hetero_formula', 
   'atom': 'atom'}

class Element(Element):

    def __init__(self, number, symbol, name):
        super(Element, self).__init__(number, symbol, name)

    def toSQL(self):
        return ('INSERT INTO {0} VALUES ("{1.symbol}", "{1.name}", {1.number});').format(tables['atom'], self)


class PDBeChem(PDBeChem):
    """
    """

    def __init__(self, cif_file):
        super(PDBeChem, self).__init__(cif_file)

    def toSQL(self):
        data = []
        self._name = self.name.replace('"', '\\"')
        values = ('("{0.id}","{0.name}","{0.formula}",{0.weight},{0.formal_charge})').format(self)
        data.append(('INSERT INTO {0} VALUES {1};').format(tables['hetero'], values))
        if self.parent is not None:
            for p in self.parent:
                if p != '':
                    data.append(('INSERT INTO {0} VALUES ("{1}","{2}");').format(tables['hparent'], self.id, p))

        for atom in self.full_formula:
            data.append(('INSERT INTO {0} VALUES ("{1.id}","{2}",{3});').format(tables['formula'], self, atom, self.full_formula[atom]))

        return ('\n').join(data)