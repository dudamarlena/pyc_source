# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/resource.py
# Compiled at: 2013-09-22 07:52:41
__docformat__ = 'restructuredtext'
from persistent import Persistent
from z3c.language.switch.interfaces import II18n
from zope.annotation.interfaces import IAnnotations
from zope.schema.interfaces import IVocabularyFactory
from ztfy.blog.interfaces.resource import IResource, IResourceContainer, IResourceContainerTarget
from zope.component import adapter
from zope.container.contained import Contained
from zope.interface import implementer, implements, classProvides
from zope.location import locate
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getName
from ztfy.base.ordered import OrderedContainer
from ztfy.extfile.blob import BlobFile, BlobImage
from ztfy.file.property import FileProperty
from ztfy.i18n.property import I18nTextProperty
from ztfy.utils.traversing import getParent

class Resource(Persistent, Contained):
    implements(IResource)
    title = I18nTextProperty(IResource['title'])
    description = I18nTextProperty(IResource['description'])
    content = FileProperty(IResource['content'], klass=BlobFile, img_klass=BlobImage)
    filename = FieldProperty(IResource['filename'])
    language = FieldProperty(IResource['language'])


class ResourceContainer(OrderedContainer):
    implements(IResourceContainer)


RESOURCES_ANNOTATIONS_KEY = 'ztfy.blog.resource.container'

@adapter(IResourceContainerTarget)
@implementer(IResourceContainer)
def ResourceContainerFactory(context):
    """Resources container adapter"""
    annotations = IAnnotations(context)
    container = annotations.get(RESOURCES_ANNOTATIONS_KEY)
    if container is None:
        container = annotations[RESOURCES_ANNOTATIONS_KEY] = ResourceContainer()
        locate(container, context, '++static++')
    return container


class ResourceContainerResourcesVocabulary(SimpleVocabulary):
    """List of resources of a given content"""
    classProvides(IVocabularyFactory)

    def __init__(self, context):
        container = getParent(context, IResourceContainerTarget)
        terms = [ SimpleTerm(removeSecurityProxy(r), getName(r), II18n(r).queryAttribute('title') or '{{ %s }}' % r.filename) for r in IResourceContainer(container).values() ]
        super(ResourceContainerResourcesVocabulary, self).__init__(terms)