# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/evidence.py
# Compiled at: 2020-02-12 23:26:22
# Size of source mod 2**32: 4012 bytes
__doc__ = '\nCreated by: Lee Bergstrand (2017)\n\nDescription: The evidence class.\n'
from pygenprop.functional_element import FunctionalElement

class Evidence(object):
    """Evidence"""

    def __init__(self, evidence_identifiers=None, gene_ontology_terms=None, sufficient=False, parent: FunctionalElement=None):
        """
        Creates a new Evidence object.

        :param evidence_identifiers: A list of identifiers of proteins or processes supporting the existence of a
                                     FunctionalElement (i.e a list of Intro Consortium IDs or GenProp Accessions).
        :param gene_ontology_terms: The ids for gene ontology (GO) terms defining the protein or process supporting
                                    the existence of a FunctionalElement.
        :param sufficient: Can this evidence alone prove the existence of FunctionalElement?
        """
        if evidence_identifiers is None:
            evidence_identifiers = []
        else:
            if gene_ontology_terms is None:
                gene_ontology_terms = []
            if sufficient is None:
                sufficient = False
        self.evidence_identifiers = evidence_identifiers
        self.gene_ontology_terms = gene_ontology_terms
        self.sufficient = sufficient
        self.parent = parent

    def __repr__(self):
        repr_data = [
         'Evidence_IDs: ' + str(self.evidence_identifiers),
         'GO Terms: ' + str(self.gene_ontology_terms),
         'Sufficient: ' + str(self.sufficient)]
        return '(' + ', '.join(repr_data) + ')'

    @property
    def has_genome_property(self):
        """
        Is the evidence a genome property?

        :return: Return True if evidence is a genome property.
        """
        genome_property = False
        for identifier in self.evidence_identifiers:
            if 'genprop' in identifier.lower():
                genome_property = True
                break

        return genome_property

    @property
    def property_identifiers(self):
        """
        Gets the genome properties identifiers representing a piece of evidence.

        :return: A list of genome property identifiers.
        """
        genome_property_identifiers = []
        for identifier in self.evidence_identifiers:
            if 'genprop' in identifier.lower():
                genome_property_identifiers.append(identifier)

        return genome_property_identifiers

    @property
    def interpro_identifiers(self):
        """
        Gets the InterPro (IPRXXXXXX) identifiers representing a piece of evidence.

        :return: A list of genome property identifiers.
        """
        genome_property_identifiers = []
        for identifier in self.evidence_identifiers:
            if 'ipr' in identifier.lower():
                genome_property_identifiers.append(identifier)

        return genome_property_identifiers

    @property
    def consortium_identifiers(self):
        """
         Gets the InterPro consortium signature identifiers (PFAM, TIGRFAM, etc.) representing a piece of evidence.

        :return: A set of genome property identifiers.
        """
        genome_property_identifiers = []
        for identifier in self.evidence_identifiers:
            lowercase_identifier = identifier.lower()
            if 'genprop' not in lowercase_identifier and 'ipr' not in lowercase_identifier:
                genome_property_identifiers.append(identifier)

        return genome_property_identifiers

    @property
    def genome_properties(self):
        """
        Get genome properties that are used by this evidence.

        :return: A list of genome properties.
        """
        parent_genome_property = self.parent.parent.parent
        return [genome_property for genome_property in parent_genome_property.children if genome_property.id in self.property_identifiers]