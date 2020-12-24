# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/crossref.py
# Compiled at: 2017-06-20 22:47:25
import logging, re, utopia.citation, utopia.tools.crossref
from utopia.log import logger
try:
    import spineapi
except ImportError:
    logger.info('spineapi not imported: document verification of CrossRef results will be unavailable')
    spineapi = None

class CrossRefIdentifier(utopia.citation.Resolver):
    """Given a title, try to identify the document."""

    def resolve(self, citations, document=None):
        citation = {}
        doi = utopia.citation.pick_from(citations, 'identifiers[doi]', default=None, record_in=citation)
        title = utopia.citation.pick_from(citations, 'title', default=None, record_in=citation)
        if doi is not None or title is not None:
            if doi is None:
                xref_results = utopia.tools.crossref.search(title)
                if len(xref_results) == 1:
                    best = xref_results[0]
                    xref_title = best.get('title', '').strip(' .')
                    if len(xref_title) > 0:
                        matched = False
                        if document is not None and spineapi is not None:
                            xref_title = re.sub('[^--~\xad֊־᐀᠆‐-―⁓⁻₋−⸗⸺⸻〜〰゠︱︲﹘﹣－]+', lambda x: re.escape(x.group(0)), xref_title)
                            xref_title = re.sub('[-~\xad֊־᐀᠆‐-―⁓⁻₋−⸗⸺⸻〜〰゠︱︲﹘﹣－-]+', lambda x: ('\\p{{Pd}}{{{0}}}').format(len(x.group(0))), xref_title)
                            matches = document.search(xref_title, spineapi.RegExp + spineapi.IgnoreCase)
                            matched = len(matches) > 0
                        else:
                            matched = xref_title.lower() == title
                        if matched:
                            citation.update(best)
                            doi = citation.get('identifiers', {}).get('doi')
                            if doi is not None and doi.startswith('http://dx.doi.org/'):
                                doi = doi[18:]
                                citation['identifiers']['doi'] = doi
            if doi is not None:
                if None not in (document, title):
                    try:
                        xref_results = utopia.tools.crossref.resolve(doi)
                        xref_title = xref_results.get('title', '')
                        if len(xref_title) > 0:
                            print 'crossref: resolved title:', xref_title.encode('utf8')
                            if re.sub('[^\\w]+', ' ', title).strip() == re.sub('[^\\w]+', ' ', xref_title).strip():
                                print 'crossref: titles match precisely'
                                citation.update(xref_results)
                            else:
                                matches = document.findInContext('', xref_title, '')
                                if len(matches) > 0:
                                    citation.update(xref_results)
                                    print 'crossref: overriding scraped title with crossref title'
                                else:
                                    print 'crossref: ignoring resolved citations'
                    except Exception as e:
                        import traceback
                        traceback.print_exc()

        return citation

    def provenance(self):
        return {'whence': 'crossref'}

    def purposes(self):
        return 'identify'

    def weight(self):
        return 0


class CrossRefExpander(utopia.citation.Resolver):
    """From a DOI, expand the citations"""

    def resolve(self, citations, document=None):
        citation = {}
        doi = utopia.citation.pick_from(citations, 'identifiers[doi]', default=None, record_in=citation)
        if doi is not None:
            citation.update(utopia.tools.crossref.resolve(doi))
        return citation

    def provenance(self):
        return {'whence': 'crossref'}

    def purposes(self):
        return 'expand'

    def weight(self):
        return 12


class DOIResolver(utopia.citation.Resolver):
    """Resolve a URL from a DOI"""

    def resolve(self, citations, document=None):
        citation = {}
        doi = utopia.citation.pick_from(citations, 'identifiers[doi]', default=None, record_in=citation)
        if doi is not None and not utopia.citation.has_link(citations, {'type': 'article'}, {'whence': 'crossref'}):
            citation['links'] = [
             {'url': ('http://dx.doi.org/{0}').format(doi), 'mime': 'text/html', 
                'type': 'article', 
                'title': "Show on publisher's website"}]
        return citation

    def provenance(self):
        return {'whence': 'crossref'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 100