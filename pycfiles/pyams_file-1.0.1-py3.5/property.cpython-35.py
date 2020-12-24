# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/property.py
# Compiled at: 2019-12-20 06:53:21
# Size of source mod 2**32: 8598 bytes
"""PyAMS_file.property module

This module defines files properties which can be used to automatically handle all the magic
behind external files management; this includes blobs management and their references counting.
"""
from pyramid.threadlocal import get_current_registry
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectAddedEvent, ObjectCreatedEvent, ObjectRemovedEvent
from zope.location import locate
from zope.schema.interfaces import IField
from pyams_file.file import FileFactory
from pyams_file.interfaces import IFile, IFileFieldContainer, IFileInfo
from pyams_utils.adapter import get_annotation_adapter
from pyams_utils.interfaces.form import NOT_CHANGED, TO_BE_DELETED
__docformat__ = 'restructuredtext'
FILE_CONTAINER_ATTRIBUTES = 'pyams_file.file.attributes'
_MARKER = object()

class FileProperty:
    __doc__ = 'Property class used to handle files'

    def __init__(self, field, name=None, klass=None, **args):
        if not IField.providedBy(field):
            raise ValueError('Provided field must implement IField interface...')
        if name is None:
            name = field.__name__
        self._FileProperty__field = field
        self._FileProperty__name = name
        self._FileProperty__klass = klass
        self._FileProperty__args = args

    def __get__(self, instance, klass):
        if instance is None:
            return self
        value = instance.__dict__.get(self._FileProperty__name, _MARKER)
        if value is _MARKER:
            field = self._FileProperty__field.bind(instance)
            value = getattr(field, 'default', _MARKER)
            if value is _MARKER:
                raise AttributeError(self._FileProperty__name)
        return value

    def __set__(self, instance, value):
        if value is NOT_CHANGED:
            return
        registry = get_current_registry()
        if value is not None and value is not TO_BE_DELETED:
            filename = None
            if isinstance(value, tuple):
                filename, value = value
            if not IFile.providedBy(value):
                factory = self._FileProperty__klass or FileFactory
                file = factory(value, **self._FileProperty__args)
                registry.notify(ObjectCreatedEvent(file))
                if not file.get_size():
                    value.seek(0)
                    file.data = value
                value = file
            if filename is not None:
                info = IFileInfo(value)
                if info is not None:
                    info.filename = filename
            field = self._FileProperty__field.bind(instance)
            field.validate(value)
            if field.readonly and instance.__dict__.has_key(self._FileProperty__name):
                raise ValueError(self._FileProperty__name, 'Field is readonly')
            old_value = instance.__dict__.get(self._FileProperty__name, _MARKER)
            if old_value != value:
                if old_value is not _MARKER and old_value is not None:
                    registry.notify(ObjectRemovedEvent(old_value))
                if value is TO_BE_DELETED:
                    pass
                if self._FileProperty__name in instance.__dict__:
                    del instance.__dict__[self._FileProperty__name]
        else:
            name = '++attr++{0}'.format(self._FileProperty__name)
            if value is not None:
                locate(value, instance, name)
            instance.__dict__[self._FileProperty__name] = value
            if not IFileFieldContainer.providedBy(instance):
                alsoProvides(instance, IFileFieldContainer)
            attributes = get_annotation_adapter(instance, FILE_CONTAINER_ATTRIBUTES, set, notify=False, locate=False)
            attributes.add(self._FileProperty__name)
            registry.notify(ObjectAddedEvent(value, instance, name))


class I18nFileProperty:
    __doc__ = 'I18n property class used to handle files'

    def __init__(self, field, name=None, klass=None, **args):
        if not IField.providedBy(field):
            raise ValueError('Provided field must implement IField interface...')
        if name is None:
            name = field.__name__
        self._I18nFileProperty__field = field
        self._I18nFileProperty__name = name
        self._I18nFileProperty__klass = klass
        self._I18nFileProperty__args = args

    def __get__(self, instance, klass):
        if instance is None:
            return self
        value = instance.__dict__.get(self._I18nFileProperty__name, _MARKER)
        if value is _MARKER:
            field = self._I18nFileProperty__field.bind(instance)
            value = getattr(field, 'default', _MARKER)
            if value is _MARKER:
                raise AttributeError(self._I18nFileProperty__name)
        return value

    def __set__(self, instance, value):
        registry = get_current_registry()
        for lang in value:
            lang_value = value[lang]
            if lang_value is TO_BE_DELETED or lang_value is NOT_CHANGED:
                pass
            elif lang_value is not None:
                filename = None
                if isinstance(lang_value, tuple):
                    filename, lang_value = lang_value
                if not IFile.providedBy(lang_value):
                    factory = self._I18nFileProperty__klass or FileFactory
                    file = factory(lang_value, **self._I18nFileProperty__args)
                    registry.notify(ObjectCreatedEvent(file))
                    if not file.get_size():
                        lang_value.seek(0)
                        file.data = lang_value
                    lang_value = file
                if filename is not None:
                    info = IFileInfo(lang_value)
                    if info is not None:
                        info.filename = filename
                    value[lang] = lang_value

        field = self._I18nFileProperty__field.bind(instance)
        field.validate(value)
        if field.readonly and instance.__dict__.has_key(self._I18nFileProperty__name):
            raise ValueError(self._I18nFileProperty__name, 'Field is readonly')
        old_value = instance.__dict__.get(self._I18nFileProperty__name, _MARKER)
        if old_value != value:
            if old_value is _MARKER:
                old_value = {}
            for lang in value:
                new_lang_value = value.get(lang)
                if new_lang_value is NOT_CHANGED:
                    pass
                else:
                    old_lang_value = old_value.get(lang, _MARKER)
                    if old_lang_value is not _MARKER and old_lang_value is not None:
                        registry.notify(ObjectRemovedEvent(old_lang_value))
                    if new_lang_value is TO_BE_DELETED:
                        if self._I18nFileProperty__name in instance.__dict__:
                            del old_value[lang]
                    else:
                        name = '++i18n++{0}:{1}'.format(self._I18nFileProperty__name, lang)
                        if new_lang_value is not None:
                            locate(new_lang_value, instance, name)
                        old_value[lang] = new_lang_value
                        if not IFileFieldContainer.providedBy(instance):
                            alsoProvides(instance, IFileFieldContainer)
                        attributes = get_annotation_adapter(instance, FILE_CONTAINER_ATTRIBUTES, set, notify=False, locate=False)
                        attributes.add('{0}::{1}'.format(self._I18nFileProperty__name, lang))
                        registry.notify(ObjectAddedEvent(new_lang_value, instance, name))
                instance.__dict__[self._I18nFileProperty__name] = old_value