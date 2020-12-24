# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/index.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
from persistent import Persistent
from z3c.language.switch.interfaces import II18n
from zope.annotation.interfaces import IAnnotations
from zope.schema.interfaces import IVocabularyFactory
from ztfy.gallery.interfaces import IGalleryIndex, IGalleryIndexManager, IGalleryContainer, IGalleryImageBaseInfo, IGalleryImageIndexInfo, IGalleryImage
from zope.component import adapter
from zope.container.contained import Contained
from zope.interface import implementer, implements, alsoProvides, noLongerProvides, classProvides
from zope.location.location import locate
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.traversing import api as traversing_api
from ztfy.i18n.property import I18nTextProperty
from ztfy.utils.traversing import getParent

class GalleryIndexEntry(object):
    """Gallery index entry"""
    implements(IGalleryImageBaseInfo)
    title = I18nTextProperty(IGalleryImageBaseInfo['title'])
    description = I18nTextProperty(IGalleryImageBaseInfo['description'])


class GalleryIndex(Persistent, Contained):
    """Gallery index class"""
    implements(IGalleryIndex)
    _values = FieldProperty(IGalleryIndex['values'])

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, data):
        self._values = data
        gallery = traversing_api.getParent(self)
        if data:
            alsoProvides(gallery, IGalleryIndexManager)
        elif IGalleryIndexManager.providedBy(gallery):
            noLongerProvides(gallery, IGalleryIndexManager)

    def clear(self):
        if self.values:
            self.values.clear()


GALLERY_INDEX_ANNOTATIONS_KEY = 'ztfy.gallery.index'

@adapter(IGalleryContainer)
@implementer(IGalleryIndex)
def GalleryIndexFactory(context):
    """Gallery index adapter"""
    annotations = IAnnotations(context)
    index = annotations.get(GALLERY_INDEX_ANNOTATIONS_KEY)
    if index is None:
        index = annotations[GALLERY_INDEX_ANNOTATIONS_KEY] = GalleryIndex()
        locate(index, context, '++index++')
    return index


class GalleryIndexValuesVocabulary(SimpleVocabulary):
    classProvides(IVocabularyFactory)

    def __init__(self, context):
        terms = []
        if IGalleryImageIndexInfo.providedBy(context):
            context = context.context
        gallery = getParent(context, IGalleryContainer)
        if gallery is not None:
            index = IGalleryIndex(gallery)
            if index is not None and index.values:
                terms = [ SimpleTerm(v, title='%s - %s' % (v, II18n(t).queryAttribute('title'))) for v, t in index.values.iteritems() ]
                terms.sort(key=lambda x: x.value)
        super(GalleryIndexValuesVocabulary, self).__init__(terms)
        return


class GalleryImageIndexInfo(Persistent):
    """Gallery image index info"""
    implements(IGalleryImageIndexInfo)
    _ids = FieldProperty(IGalleryImageIndexInfo['ids'])

    def __init__(self, context):
        self.context = context

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, values):
        self._ids = values
        if values:
            gallery = getParent(self.context, IGalleryContainer)
            if gallery is not None:
                index = IGalleryIndex(gallery)
                title = {}
                description = {}
                for key in values:
                    for lang, value in index.values[key].title.items():
                        if value:
                            if lang in title:
                                title[lang] += ', ' + value
                            else:
                                title[lang] = value

                    for lang, value in index.values[key].description.items():
                        if value:
                            if lang in description:
                                description[lang] += ', ' + value
                            else:
                                description[lang] = value

                self.context.title = title
                self.context.description = description
        return


@adapter(IGalleryImage)
@implementer(IGalleryImageIndexInfo)
def GalleryImageIndexFactory(context):
    """Gallery image index adapter"""
    annotations = IAnnotations(context)
    index = annotations.get(GALLERY_INDEX_ANNOTATIONS_KEY)
    if index is None:
        index = annotations[GALLERY_INDEX_ANNOTATIONS_KEY] = GalleryImageIndexInfo(context)
    return index