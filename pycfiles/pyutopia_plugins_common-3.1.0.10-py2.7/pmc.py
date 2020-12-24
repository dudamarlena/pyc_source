# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/pmc.py
# Compiled at: 2017-06-19 05:31:59
import utopia.citation, utopia.tools.pmc

class PMCResolver(utopia.citation.Resolver):
    """Resolve PDF link from a PMC ID"""

    def resolve(self, citations, document=None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'pmc'}):
            pmcid = utopia.citation.pick_from(citations, 'identifiers/pmc', default=None)
            if pmcid is None:
                doi = utopia.citation.pick_from(citations, 'identifiers/doi', default=None, record_in=citation)
                pmid = utopia.citation.pick_from(citations, 'identifiers/pubmed', default=None, record_in=citation)
                if doi is not None and pmcid is None:
                    pmcid = utopia.tools.pmc.identify(doi, 'doi')
                if pmid is not None and pmcid is None:
                    pmcid = utopia.tools.pmc.identify(pmid, 'pmid')
            if pmcid is not None:
                pdf_url = ('http://www.ncbi.nlm.nih.gov/pmc/articles/{0}/pdf/').format(pmcid)
                citation.update({'links': [
                           {'url': pdf_url, 
                              'mime': 'application/pdf', 
                              'type': 'article', 
                              'title': 'Download article from PubMed Central'}], 
                   'identifiers': {'pmc': pmcid}})
                return citation
        return

    def provenance(self):
        return {'whence': 'pmc'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 104