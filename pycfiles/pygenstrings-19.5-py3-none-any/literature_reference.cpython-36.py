# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/literature_reference.py
# Compiled at: 2019-04-04 13:26:37
# Size of source mod 2**32: 1197 bytes
__doc__ = '\nCreated by: Lee Bergstrand (2017)\n\nDescription: The literature reference class.\n'

class LiteratureReference(object):
    """LiteratureReference"""

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