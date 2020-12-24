# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/literature_reference.py
# Compiled at: 2019-04-04 13:26:37
# Size of source mod 2**32: 1197 bytes
"""
Created by: Lee Bergstrand (2017)

Description: The literature reference class.
"""

class LiteratureReference(object):
    __doc__ = 'A class representing a literature reference supporting the existence of a genome property.'

    def __init__(self, number, pubmed_id, title, authors, citation):
        """
        Creates a Reference object.

        :param number: The position of the reference.
        :param pubmed_id: The PubMed identify of the literature reference.
        :param title: The title of the literature reference.
        :param authors: The author list of the literature reference.
        :param citation: A citation for the literature reference.
        """
        self.number = int(number)
        self.pubmed_id = int(pubmed_id)
        self.title = title
        self.authors = authors
        self.citation = citation

    def __repr__(self):
        repr_data = [
         'Ref ' + str(self.number),
         'Pubmed ID: ' + str(self.pubmed_id),
         'Title: ' + str(self.title),
         'Authors: ' + str(self.authors),
         'Citation: ' + str(self.citation)]
        return ', '.join(repr_data)