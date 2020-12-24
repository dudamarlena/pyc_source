# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/organisminfo/species.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 3011 bytes
import urllib.parse, requests, time

def eprint(*args, **kwargs):
    print(*args, **kwargs)


class Species:
    ensembl_server = 'http://rest.ensembl.org/taxonomy/classification/'

    def __init__(self, species):
        """
        """
        self.species = species.lower()
        self.ensembl_response = Species.get_ensembl_tax(self.species)
        self.ensembl_dict = self.ensembl_list_to_dict(self.ensembl_response)
        self.tax_tuple = self.get_taxonomy_as_tuple(self.ensembl_dict)
        self.tax_dict = self.get_taxonomy_as_dict(self.tax_tuple)

    def ensembl_list_to_dict(self, ensembl_response):
        """
        """
        ensembl_dict = {self.species: None}
        for dict in ensembl_response:
            name = dict['scientific_name'].lower()
            child_name = dict['children'][0]['scientific_name'].lower()
            ensembl_dict[name] = child_name

        return ensembl_dict

    @staticmethod
    def get_ensembl_tax(species):
        """
        """
        ensembl_query = '{}{}?'.format(Species.ensembl_server, urllib.parse.quote(species, safe=''))
        try:
            r = requests.get(ensembl_query, headers={'Content-Type': 'application/json'})
            time.sleep(1)
        except Exception as e:
            print('Error while interacting ENSEMBEL REST API')
            print('Error: {}'.format(e))
            raise Exception('Error while interacting ENSEMBEL REST API')

        if not r.ok:
            eprint('Possible source of error: Missing or misspelling of organism name.')
            eprint('Query was: {}'.format(query))
            eprint('r url: {}'.format(r.url))
            eprint('r text: {}'.format(r.text))
            raise Exception('Possible source of error: Missing or misspelling of organism name.')
        return r.json()

    @staticmethod
    def get_taxonomy_as_tuple(ensembl_dict):
        """
        """
        root = None
        children = tuple(ensembl_dict.values())
        for name in ensembl_dict:
            if name not in children:
                root = name
                break

        out_lst = [
         root]
        parent = root
        child = ''
        while True:
            child = ensembl_dict.get(parent, None)
            if child is None:
                break
            out_lst.append(child)
            parent = child
            child = ''

        return tuple(out_lst)

    @staticmethod
    def get_taxonomy_as_dict(tax_tuple):
        """
        """
        return {'domain': tax_tuple[0], 
         'phylum': tax_tuple[1], 
         'class': tax_tuple[2], 
         'order': tax_tuple[3], 
         'family': tax_tuple[4], 
         'genus': tax_tuple[5], 
         'species': tax_tuple[6]}