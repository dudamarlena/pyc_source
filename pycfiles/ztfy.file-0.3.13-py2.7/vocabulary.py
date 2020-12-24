# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/vocabulary.py
# Compiled at: 2013-05-14 08:51:01
import mimetypes, os.path
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import classProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

class MIMETypesVocabulary(SimpleVocabulary):
    """MIME types vocabulary"""
    classProvides(IVocabularyFactory)

    def __init__(self, context):
        terms = (SimpleTerm(ext, ext, '%s (%s)' % (mimetype, ext)) for ext, mimetype in mimetypes.types_map.iteritems())
        super(MIMETypesVocabulary, self).__init__(sorted(terms, key=lambda x: x.title))


class MagicTypesVocabulary(SimpleVocabulary):
    """libmagic types vocabulary"""
    classProvides(IVocabularyFactory)

    def __init__(self, context):
        dirname, _filename = os.path.split(__file__)
        with open(os.path.join(dirname, 'magic', 'mime.types')) as (f):
            terms = [ SimpleTerm(mime, mime) for mime in f.read().split() ]
        super(MagicTypesVocabulary, self).__init__(terms)