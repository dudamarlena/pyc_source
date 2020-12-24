# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/lib/Probe/Thermo/NNModel.py
# Compiled at: 2017-03-25 14:51:21


class NNModel:
    """Defines common interface and shared code for all variants of the
    nearest-neighbor model (DNA-DNA, RNA-RNA, and DNA-RNA)
    Parameters:
    -----------
    Tref: Float
          reference temperature for thermo data
    R: Float
       gas constant in kcal/mol/K
    pairs: Python dict()
           posible pairs for DNA
    rpairs: Python dict()
            posible pairs for RNA

    Notes:
    ------
    Pairs are written in 5' -> 3' direction
    """

    def __init__(self):
        self.Tref = 310.15
        self.R = 0.001987
        self.pairs = [
         'AA', 'AT', 'AC', 'AG', 'TA', 'TT', 'TC', 'TG',
         'CA', 'CT', 'CC', 'CG', 'GA', 'GT', 'GC', 'GG']
        self.rpairs = ['AA', 'AU', 'AC', 'AG', 'UA', 'UU', 'UC', 'UG',
         'CA', 'CU', 'CC', 'CG', 'GA', 'GU', 'GC', 'GG']