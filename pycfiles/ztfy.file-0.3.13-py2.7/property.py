# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/property.py
# Compiled at: 2014-11-13 09:53:29
import mimetypes
from z3c.form.interfaces import NOT_CHANGED
from zope.app.file.interfaces import IFile, IImage
from zope.location.interfaces import ILocation
from zope.schema.interfaces import IField
from ztfy.file.interfaces import IFilePropertiesContainer, IFilePropertiesContainerAttributes, ICthumbImageFieldData, IThumbnailGeometry
from zope.app.file import File, Image
from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectCreatedEvent, ObjectAddedEvent, ObjectRemovedEvent
from zope.location import locate
from zope.publisher.browser import FileUpload
from zope.security.proxy import removeSecurityProxy
from ztfy.extfile import getMagicContentType
from ztfy.file import _
_marker = object()

class FileProperty(object):
    """Property class used to handle files"""
    interface = IFile

    def __init__(self, field, name=None, klass=File, img_klass=None, **args):
        if not IField.providedBy(field):
            raise ValueError, _('Provided field must implement IField interface...')
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        self.__klass = klass
        self.__img_klass = img_klass
        self.__args = args
        return

    def __get__(self, instance, klass):
        if instance is None:
            return self
        else:
            value = instance.__dict__.get(self.__name, _marker)
            if value is _marker:
                field = self.__field.bind(instance)
                value = getattr(field, 'default', _marker)
                if value is _marker:
                    raise AttributeError(self.__name)
            return value

    def __set__(self, instance, value):
        if value is NOT_CHANGED:
            return
        else:
            if value is not None:
                filename = None
                if isinstance(value, tuple):
                    value, filename = value
                if isinstance(value, FileUpload):
                    value = value.read()
                if not self.interface.providedBy(value):
                    content_type = getMagicContentType(value) or 'text/plain'
                    if filename and content_type.startswith('text/'):
                        content_type = mimetypes.guess_type(filename)[0] or content_type
                    if self.__img_klass is not None and content_type.startswith('image/'):
                        f = self.__img_klass(**self.__args)
                    else:
                        f = self.__klass(**self.__args)
                    notify(ObjectCreatedEvent(f))
                    f.data = value
                    f.contentType = content_type
                    value = f
            field = self.__field.bind(instance)
            field.validate(value)
            if field.readonly and instance.__dict__.has_key(self.__name):
                raise ValueError(self.__name, _('Field is readonly'))
            old_value = instance.__dict__.get(self.__name, _marker)
            if old_value != value:
                if old_value is not _marker and old_value is not None:
                    notify(ObjectRemovedEvent(old_value))
                if value is not None:
                    filename = '++file++%s' % self.__name
                    if value.contentType:
                        filename += mimetypes.guess_extension(value.contentType) or ''
                    locate(value, removeSecurityProxy(instance), filename)
                    alsoProvides(value, ILocation)
                    alsoProvides(instance, IFilePropertiesContainer)
                    IFilePropertiesContainerAttributes(instance).attributes.add(self.__name)
                    notify(ObjectAddedEvent(value, instance, filename))
            instance.__dict__[self.__name] = value
            return

    def __getattr__(self, name):
        return getattr(self.__field, name)


class ImageProperty(FileProperty):
    """Property class used to handle images"""
    interface = IImage

    def __init__(self, field, name=None, klass=Image, img_klass=None, **args):
        super(ImageProperty, self).__init__(field, name, klass, img_klass, **args)

    def __set__(self, instance, value):
        data = ICthumbImageFieldData(value, None)
        if data is not None:
            value = data.value
            geom = data.geometry
        super(ImageProperty, self).__set__(instance, value)
        if data is not None:
            new_value = instance.__dict__.get(self.__name, _marker)
            if new_value is not _marker:
                geometry = IThumbnailGeometry(new_value)
                if geometry is not None:
                    geometry.position = geom.position
                    geometry.size = geom.size
        return