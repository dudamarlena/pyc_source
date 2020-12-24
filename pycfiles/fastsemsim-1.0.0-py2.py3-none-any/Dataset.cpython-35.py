# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/ext800/projects/fastsemsim/fastsemsim/fastsemsim/data/Dataset.py
# Compiled at: 2019-03-10 10:01:33
# Size of source mod 2**32: 7976 bytes
from __future__ import print_function
try:
    unicode
except (NameError, AttributeError):
    unicode = str

import pandas as pd, os
from fastsemsim import ontology
ontology_aliases = {'GeneOntology': 'GeneOntology', 
 'geneontology': 'GeneOntology', 
 'GO': 'GeneOntology', 
 'go': 'GeneOntology', 
 'DiseaseOntology': 'DiseaseOntology', 
 'diseaseontology': 'DiseaseOntology', 
 'DO': 'DiseaseOntology', 
 'do': 'DiseaseOntology', 
 'CellOntology': 'CellOntology', 
 'cellontology': 'CellOntology', 
 'CO': 'CellOntology', 
 'co': 'CellOntology', 
 'FFOntology': 'FFOntology', 
 'FF': 'FFOntology', 
 'GenericOntology': 'GenericOntology', 
 'Ontology': 'Ontology'}

class Dataset(object):
    __doc__ = "\n\tThe class Dataset keeps track of the ontologies and annotation corpora (ACs) included in fastsemsim.\n\tThe class includes all the methods to create and browse the dataset of available ontologies and ACs.\n\tEach ontology or AC is represented by a 'descriptor' inside Dataset.\n\tDescriptors returned to the user through the API functions can be fed to the other functions of fastsemsim\n\tto load ontologies and ac.\n\tUpon creation, unless otherwise specified through the parameter 'descriptor', a Dataset object will load the standard dataset\n\tshipped with fastsemsim (file data/dataset.txt).\n\t"

    def __init__(self, descriptor=None):
        self.populate(descriptor)

    def populate(self, descriptor=None):
        """
                Initialize object structures, loading their content from a file describing the dataset.
                This function is called on class instantiation. By default, the file data/dataset.txt will be loaded.
                The 'descriptor' parameter allows the user to use a custom dataset descriptor file.
                """
        descriptor_null = False
        if descriptor is None:
            descriptor_null = True
        if descriptor_null:
            program_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
            descriptor = program_dir + '/dataset.txt'
        self.dataset = pd.read_csv(descriptor, sep='\t', comment='#', header=0).dropna(how='all')
        self.dataset.index = self.dataset['name']
        if descriptor_null:
            program_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/'
            self.dataset['file'] = program_dir + self.dataset['file']

    def get_descriptor(self, name):
        """
                Return the descriptor of the required ontology or ac, if it exists in the loaded dataset.
                """
        return self.dataset.loc[(self.dataset['name'] == name)]

    def list_ontologies(self):
        """
                List all the ontologies in the dataset. Each row of the returned pandas table is a valid descriptor.
                """
        return self.dataset.loc[(self.dataset['type'] == 'O')]

    def get_ontology(self, ontology_name=None, ontology_type='GeneOntology'):
        """
                Return the descriptor(s) of the required ontology, if it exists in the loaded dataset.
                The user can require a specific ontology by name and/or ontology type. Either the name or the type has to be specified.
                
                Parameters
                ----------
                ontology_name : str, optional
                        Name of the desired ontology

                ontology_type : str, optional
                        Type of ontology (e.g. GeneOntology, CellOntology, ...)

                Returns
                -------
                pandas table
                        Table of descriptors of ontologies compatible with input query. Each row is a valid descriptor.

                """
        if (ontology_name is None) & (ontology_type is None):
            raise Exception('At least one between ontology_type and ontology_name must be provided.')
        if ontology_type in ontology_aliases:
            ontology_type = ontology_aliases[ontology_type]
        current_options = self.dataset.loc[(self.dataset['type'] == 'O')]
        if ontology_type is not None:
            current_options = current_options.loc[(current_options['ontology'] == ontology_type)]
        if ontology_name is not None:
            current_options = current_options.loc[(current_options['name'] == ontology_name)]
        return current_options

    def get_default_ontology(self, ontology_type='GeneOntology'):
        """
                Return the default ontology consistent with the required type.
                Note that, differently fomr get_ontology, this method always returns 1 ontology descriptor (if it exists).

                Parameters
                ----------
                ontology_type : str
                        Type of ontology (e.g. GeneOntology, CellOntology, ...)

                Returns
                -------
                pandas Series
                        Descriptor of ontology compatible with input query.

                """
        selected = self.get_ontology(ontology_name=None, ontology_type=ontology_type)
        if selected.shape[0] == 0:
            return
        return selected.iloc[0]

    def list_acs(self):
        """
                List all the annotation corpora in the dataset. Each row of the returned pandas table is a valid descriptor.
                """
        return self.dataset.loc[(self.dataset['type'] == 'AC')]

    def get_annotation_corpus(self, ac_name=None, ontology_type=None, ac_species=None):
        """
                Return the descriptor(s) of the required ACs, if it exists in the loaded dataset.
                The user can require a specific AC by name and/or ontology type. Either the name or the type has to be specified.
                
                Parameters
                ----------
                ontology_name : str, optional
                        Name of the desired AC

                ontology_type : str, optional
                        Type of ontology (e.g. GeneOntology, CellOntology, ...)

                ac_species : str, optional
                        Require species (e.g. human, fly, ...)

                Returns
                -------
                pandas table
                        Table of descriptors of ACs compatible with input query. Each row is a valid descriptor.

                """
        if (ac_name is None) & (ontology_type is None):
            raise Exception('At least one between ontology_type and ac_name must be provided.')
        if ontology_type in ontology_aliases:
            ontology_type = ontology_aliases[ontology_type]
        current_options = self.dataset.loc[(self.dataset['type'] == 'AC')]
        if ontology_type is not None:
            current_options = current_options.loc[(current_options['ontology'] == ontology_type)]
        if ac_name is not None:
            current_options = current_options.loc[(current_options['name'] == ac_name)]
        if ac_species is not None:
            current_options = current_options.loc[(current_options['species'] == ac_species)]
        return current_options

    def get_default_annotation_corpus(self, ontology_type='GeneOntology', ac_species='human'):
        """
                Return the default AC consistent with the required type.
                Note that, differently fomr get_annotation_corpus, this method always returns 1 ac descriptor (if it exists).

                Parameters
                ----------
                ontology_type : str
                        Type of ontology (e.g. GeneOntology, CellOntology, ...)

                ac_species : str
                        Require species (e.g. human, fly, ...)

                Returns
                -------
                pandas Series
                        Descriptor of AC compatible with input query.

                """
        selected = self.get_annotation_corpus(ac_name=None, ontology_type=ontology_type, ac_species=ac_species)
        if selected.shape[0] == 0:
            return
        return selected.iloc[0]