# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/deepak.unni3/GIT/mvp-module-library-master/env/lib/python3.7/site-packages/CTD/CTD_wrapper.py
# Compiled at: 2019-09-12 20:29:16
# Size of source mod 2**32: 532 bytes
import requests

class CTDWrapper(object):

    def __init__(self):
        self.url = 'https://ctdapi.renci.org/'

    def gene2chem(self, gene_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_GeneID/{1}/'.format(self.url, gene_curie)
        results = requests.get(call, params)
        return results.json()

    def chem2gene(self, chem_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_ChemicalID/{1}/'.format(self.url, chem_curie)
        results = requests.get(call, params)
        return results.json()