# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/vocabulary.py
# Compiled at: 2016-12-26 08:43:51
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import IVocabularyFactory
from ztfy.media.interfaces import IMediaVideoConverter, IMediaAudioConverter
from zope.component import getUtilitiesFor
from zope.interface import classProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

class VideoConvertersVocabulary(SimpleVocabulary):
    """Video converters vocabulary"""
    classProvides(IVocabularyFactory)

    def __init__(self, context=None):
        terms = [ SimpleTerm(name, name, adapter.label) for name, adapter in getUtilitiesFor(IMediaVideoConverter) ]
        super(VideoConvertersVocabulary, self).__init__(terms)


class AudioConvertersVocabulary(SimpleVocabulary):
    """Video converters vocabulary"""
    classProvides(IVocabularyFactory)

    def __init__(self, context=None):
        terms = [ SimpleTerm(name, name, adapter.label) for name, adapter in getUtilitiesFor(IMediaAudioConverter) ]
        super(AudioConvertersVocabulary, self).__init__(terms)