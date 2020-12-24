# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/kend.py
# Compiled at: 2017-06-16 10:47:22
import kend.client, kend.model, utopia.citation

class DocumentIdentifierResolver(utopia.citation.Resolver):
    """Resolve a Utopia URI for this document."""

    def _unidentifiedDocumentRef(self, document):
        """Compile a document reference from a document's fingerprints"""
        evidence = [ kend.model.Evidence(type='fingerprint', data=f, srctype='document') for f in document.fingerprints()
                   ]
        return kend.model.DocumentReference(evidence=evidence)

    def _identifyDocumentRef(self, documentref):
        """Find a URI from a document reference, resolving it if necessary"""
        id = getattr(documentref, 'id', None)
        if id is None:
            documentref = kend.client.Client().documents(documentref)
            id = getattr(documentref, 'id', None)
        return id

    def _resolveDocumentId(self, document):
        """Return the document URI for the given document"""
        documentref = self._unidentifiedDocumentRef(document)
        return self._identifyDocumentRef(documentref)

    def resolve(self, citations, document=None):
        if document is not None:
            utopia_id = utopia.citation.pick_from(citations, 'identifiers[utopia]', None)
            if utopia_id is None:
                utopia_id = utopia.tools.utils.metadata(document, 'identifiers[utopia]')
                if utopia_id is None:
                    utopia_id = self._resolveDocumentId(document)
                    return {'identifiers': {'utopia': utopia_id}}
        return

    def provenance(self):
        return {'whence': 'kend'}

    def purposes(self):
        return 'identify'

    def weight(self):
        return -10000