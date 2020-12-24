# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/deepak.unni3/GIT/mvp-module-library-master/env/lib/python3.7/site-packages/SimSearch/simsearch_client.py
# Compiled at: 2019-09-12 20:29:16
# Size of source mod 2**32: 3897 bytes
import requests, pandas as pd

class SimSearchWrapper:
    SIMSEARCH_API = 'https://monarchinitiative.org/simsearch/phenotype'

    def get_phenotypically_similar_genes(self, input_gene, phenotypes, taxon):
        """
        :param input_gene: gene with phenotypes
        :param phenotypes: list of phenotype curies
        :param taxon: an ncbi taxid (e.g. "10090")
        :param return_all:
        :return:
        """
        headers = {'Accept-Encoding':'gzip, deflate, br', 
         'Accept-Language':'en-US,en;q=0.8', 
         'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
         'Accept':'application/json, text/javascript, */*; q=0.01'}
        data = {'input_items':' '.join(phenotypes), 
         'target_species':taxon}
        r = requests.get((self.SIMSEARCH_API), params=data, headers=headers)
        d = r.json()
        return SimSearchResult(input_gene, d)


class SimSearchResult:

    def __init__(self, input_gene, d):
        self.d = d
        self.input_gene = input_gene
        self.matches = []
        if 'b' in self.d:
            for x in self.d['b']:
                self.matches.append(SimScoreMatch(x))

    def get_results(self):
        results = list()
        for smatch in self.matches:
            try:
                results.append((self.input_gene, smatch.get_id(), smatch.get_score(), smatch.get_label(), smatch.explain_match()))
            except Exception as e:
                try:
                    print(e, smatch)
                finally:
                    e = None
                    del e

        return pd.DataFrame(results, columns=['input_id', 'id', 'score', 'label', 'explanation'])

    def explain_match(self, _id):
        match = [m for m in self.matches if m.get_id() == _id][0]
        return match.explain_match()


class SimScoreMatch:
    __doc__ = " a match looks like:\n    {\n      'id': 'MGI:1914792',\n      'label': 'Cog6',\n      'matches': [{'a': {'IC': 4.758053613685234,\n         'id': 'HP:0001903',\n         'label': 'Anemia'},\n        'b': {'IC': 12.3826428380023,\n         'id': 'MP:0013022',\n         'label': 'increased Ly6C high monocyte number'},\n        'lcs': {'IC': 3.6863721977964343,\n         'id': 'MP:0013658',\n         'label': 'abnormal myeloid cell morphology'}},\n       {'a': {'IC': 6.047802632643478,\n         'id': 'HP:0001679',\n         'label': 'Abnormal aortic morphology'},\n        'b': {'IC': 10.936619714893055,\n         'id': 'MP:0011683',\n         'label': 'dual inferior vena cava'},\n        'lcs': {'IC': 5.823930299277827,\n         'id': 'UBERON:0003519PHENOTYPE',\n         'label': 'thoracic cavity blood vessel phenotype'}}],\n      'score': {'metric': 'combinedScore', 'rank': 93, 'score': 70},\n      'taxon': {'id': 'NCBITaxon:10090', 'label': 'Mus musculus'},\n      'type': 'gene'\n    }\n  "

    def __init__(self, match):
        self.match = match

    def get_score(self):
        return self.match['score']['score']

    def get_label(self):
        return self.match['label']

    def get_id(self):
        return self.match['id']

    def explain_match(self):
        s = []
        for m in self.match['matches']:
            s.append('{} -> {} <- {}'.format(m['a']['label'], m['lcs']['label'], m['b']['label']))

        return '\n'.join(s)


class test_SimSearchWrapper:

    def test(self):
        phenotypes = [
         'HP:0001679', 'HP:0001903']
        taxon = '10090'
        w = SimSearchWrapper()
        ssr = w.get_phenotypically_similar_genes(phenotypes, taxon)
        ssr.get_results()
        ssr.explain_match('MGI:3030214')