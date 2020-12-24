# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/deepak.unni3/GIT/mvp-module-library-master/env/lib/python3.7/site-packages/OwlSim3/owlsim_wrapper.py
# Compiled at: 2019-09-12 20:29:16
# Size of source mod 2**32: 816 bytes
import requests

class SimSearch(object):

    def __init__(self):
        self.sim_endpoint = 'http://owlsim3.monarchinitiative.org/api/'

    def phenotype_search(self, phenotype_set, matcher='phenodigm'):
        phenotype_set = SimSearch.filter_bl_phenotypes(phenotype_set)
        match = 'match/{}'.format(matcher)
        url = '{0}{1}'.format(self.sim_endpoint, match)
        params = {'id': phenotype_set}
        results = requests.get(url=url, params=params)
        package = results.json()
        return package

    @staticmethod
    def filter_bl_phenotypes(phenotype_list):
        phenotype_blacklist = ['HP:0025023']
        for elem in phenotype_blacklist:
            if elem in phenotype_list:
                phenotype_list.remove(elem)

        return phenotype_list