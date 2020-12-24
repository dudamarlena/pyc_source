# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/schema.py
# Compiled at: 2020-01-08 07:15:03
# Size of source mod 2**32: 10795 bytes
"""PyAMS_file.schema module

This module provides all custom file-related schema fields.
"""
from zope.interface import Attribute, Interface, implementer
from zope.schema import Bytes
from zope.schema.interfaces import IBytes, RequiredMissing, WrongType
from pyams_file.interfaces import IAudioFile, IBaseImageFile, IFile, IMediaFile, IVideoFile
from pyams_i18n.schema import I18nField, II18nField
from pyams_utils.interfaces.form import IDataManager, NOT_CHANGED, TO_BE_DELETED
from pyams_utils.registry import get_current_registry
__docformat__ = 'restructuredtext'

class IThumbnailField(Interface):
    __doc__ = 'Generic field interface with thumbnail'


class IFileField(IBytes):
    __doc__ = 'File object field interface'
    schema = Attribute('Required value schema')


class IMediaField(IFileField):
    __doc__ = 'Media file object field interface'


class IThumbnailMediaField(IMediaField, IThumbnailField):
    __doc__ = 'Media object field with thumbnail interface'


class IImageField(IMediaField):
    __doc__ = 'Image file object field interface'


class IThumbnailImageField(IImageField, IThumbnailField):
    __doc__ = 'Image object field with thumbnail interface'


class IVideoField(IMediaField):
    __doc__ = 'Video file field interface'


class IThumbnailVideoField(IVideoField, IThumbnailField):
    __doc__ = 'Video object field with thumbnail interface'


class IAudioField(IMediaField):
    __doc__ = 'Audio file field interface'


@implementer(IFileField)
class FileField(Bytes):
    __doc__ = 'Custom field used to handle file-like properties'
    schema = IFile

    def _validate(self, value):
        if value is TO_BE_DELETED:
            if self.required and not self.default:
                raise RequiredMissing
        else:
            if value is NOT_CHANGED:
                return
            if isinstance(value, tuple):
                try:
                    filename, stream = value
                    if not isinstance(filename, str):
                        raise WrongType(filename, str, '{0}.filename'.format(self.__name__))
                    if not hasattr(stream, 'read'):
                        raise WrongType(stream, '<file-like object>', self.__name__)
                except ValueError:
                    raise WrongType(value, tuple, self.__name__)

            if not self.schema.providedBy(value):
                raise WrongType(value, self.schema, self.__name__)


@implementer(IMediaField)
class MediaField(FileField):
    __doc__ = 'Custom field used to store media-like properties'
    schema = IMediaFile


@implementer(IThumbnailMediaField)
class ThumbnailMediaField(MediaField):
    __doc__ = 'Custom field used to store media properties with thumbnail selection'


@implementer(IImageField)
class ImageField(MediaField):
    __doc__ = 'Custom field used to handle image properties'
    schema = IBaseImageFile


@implementer(IThumbnailImageField)
class ThumbnailImageField(ImageField):
    __doc__ = 'Custom field used to handle images properties with square selection'


@implementer(IVideoField)
class VideoField(MediaField):
    __doc__ = 'Custom field used to store video file'
    schema = IVideoFile


@implementer(IThumbnailVideoField)
class ThumbnailVideoField(VideoField):
    __doc__ = 'Custom field used to store video properties with thumbnail selection'


@implementer(IAudioField)
class AudioField(MediaField):
    __doc__ = 'Custom field used to store audio file'
    schema = IAudioFile


class II18nFileField(II18nField):
    __doc__ = 'I18n file field marker interface'


@implementer(II18nFileField)
class I18nFileField(I18nField):
    __doc__ = 'I18n file field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=FileField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)

    def _validate(self, value):
        if self.required:
            if self.default:
                return
            if not value:
                raise RequiredMissing
            has_value = False
            registry = get_current_registry()
            for lang, lang_value in value.items():
                if lang_value is NOT_CHANGED:
                    adapter = registry.getMultiAdapter((self.context, self), IDataManager)
                    try:
                        old_value = adapter.query() or {}
                    except TypeError:
                        old_value = None
                    else:
                        old_value = old_value.get(lang)
                    has_value = has_value or bool(old_value)
                    if has_value:
                        break
                elif lang_value is not TO_BE_DELETED:
                    has_value = True
                    break

            if not has_value:
                raise RequiredMissing
            for lang_value in value.values():
                if lang_value in (NOT_CHANGED, TO_BE_DELETED):
                    return
                if isinstance(lang_value, tuple):
                    try:
                        filename, stream = lang_value
                        if not isinstance(filename, str):
                            raise WrongType(filename, str, '{0}.filename'.format(self.__name__))
                        if not hasattr(stream, 'read'):
                            raise WrongType(stream, '<file-like object>', self.__name__)
                    except ValueError:
                        raise WrongType(lang_value, tuple, self.__name__)

                elif not self.value_type.schema.providedBy(lang_value):
                    raise WrongType(lang_value, self.value_type.schema, self.__name__)


class II18nMediaField(II18nFileField):
    __doc__ = 'I18n media field marker interface'


@implementer(II18nMediaField)
class I18nMediaField(I18nFileField):
    __doc__ = 'I18n media field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=MediaField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nThumbnailMediaField(II18nMediaField):
    __doc__ = 'I18n field for media with thumbnail'


@implementer(II18nThumbnailMediaField)
class I18nThumbnailMediaField(I18nMediaField):
    __doc__ = 'I18n media field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=ThumbnailMediaField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nImageField(II18nFileField):
    __doc__ = 'I18n image field marker interface'


@implementer(II18nImageField)
class I18nImageField(I18nMediaField):
    __doc__ = 'I18n image field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=ImageField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nThumbnailImageField(II18nImageField):
    __doc__ = 'I18n field for image with thumbnail marker interface'


@implementer(II18nThumbnailImageField)
class I18nThumbnailImageField(I18nImageField):
    __doc__ = 'I18n field for image with thumbnail'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=ThumbnailImageField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nVideoField(II18nMediaField):
    __doc__ = 'I18n video field marker interface'


@implementer(II18nVideoField)
class I18nVideoField(I18nMediaField):
    __doc__ = 'I18n video field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=VideoField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nThumbnailVideoField(II18nVideoField):
    __doc__ = 'I18n field for video with thumbnail marker interface'


@implementer(II18nThumbnailVideoField)
class I18nThumbnailVideoField(I18nFileField):
    __doc__ = 'I18n field for video with thumbnail'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=ThumbnailVideoField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)


class II18nAudioField(II18nMediaField):
    __doc__ = 'I18n audio field marker interface'


@implementer(II18nAudioField)
class I18nAudioField(I18nMediaField):
    __doc__ = 'I18n audio field'

    def __init__(self, key_type=None, value_type=None, value_min_length=None, value_max_length=None, **kwargs):
        super(I18nFileField, self).__init__(value_type=AudioField(min_length=value_min_length, max_length=value_max_length, required=False), **kwargs)