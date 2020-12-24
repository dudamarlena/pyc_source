# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/arxiv.py
# Compiled at: 2017-06-15 12:59:20
import logging, utopia.citation, utopia.tools.arxiv

class ArXivExpander(utopia.citation.Resolver):
    """From an ArXiv ID, expand the citations"""

    def resolve(self, citations, document=None):
        citation = {}
        arxiv_id = utopia.citation.pick_from(citations, 'identifiers[arxiv]', None, record_in=citation)
        if arxiv_id is not None:
            citation.update(utopia.tools.arxiv.resolve(arxiv_id))
        return citation

    def provenance(self):
        return {'whence': 'arxiv'}

    def purposes(self):
        return 'expand'

    def weight(self):
        return 10