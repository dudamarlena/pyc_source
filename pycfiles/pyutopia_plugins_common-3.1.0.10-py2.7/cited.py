# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/cited.py
# Compiled at: 2017-06-15 12:59:20
import json, hashlib, urllib2, utopia.citation, utopia.tools.cited

class CitedUnstructuredIdentifier(utopia.citation.Resolver):
    """Give unstructured citations a hash identifier"""

    def resolve(self, citations, document=None):
        for citation in citations:
            unstructured = utopia.citation.pick(citation, 'unstructured', default=None)
            if unstructured is not None:
                unstructured = unstructured.strip()
                print ('Found unstructured: {}').format(repr(unstructured))
                hash = hashlib.sha256(unstructured.encode('utf8')).hexdigest()
                print ('Generated hash: {}').format(hash)
                utopia.citation.set_by_keyspec(citation, 'identifiers[unstructured]', hash)

        return

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9200


class CitedResolver(utopia.citation.Resolver):
    """Submit citation identifiers to cited for resolution"""

    def resolve(self, citations, document=None):
        identifiers = utopia.citation.pick_from(citations, 'identifiers', default={})
        if len(identifiers) > 0:
            return utopia.tools.cited.resolve(**identifiers)

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9100


class CitedParser(utopia.citation.Resolver):
    """Submit unstructured citations to cited for parsing"""

    def resolve(self, citations, document=None):
        for citation in citations:
            if utopia.citation.pick(citation, 'provenance/whence', default=None) == 'cermine':
                return

        structure_keys = set(['title', 'authors', 'year'])
        citation = {}
        unstructured = utopia.citation.pick_from(citations, 'unstructured', default=None, record_in=citation)
        if unstructured is not None and len(structure_keys & set(unstructured.citation.keys())) == 0:
            structured = utopia.tools.cited.parse(unstructured)
            if len(structured) > 0:
                citation.update(structured[0])
                return citation
        return

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9000


class CitedSubmitter(utopia.citation.Resolver):
    """Submit citation information to cited"""

    def resolve(self, citations, document=None):
        utopia.tools.cited.submit(citations)

    def provenance(self):
        return {'whence': 'cited'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 100000