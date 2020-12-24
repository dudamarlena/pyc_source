# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/fields/files.py
# Compiled at: 2019-02-14 00:35:17
import datetime, os, posixpath, warnings
from django import forms
from django.core import checks
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.db.models import signals
from django.db.models.fields import Field
from django.utils import six
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_str, force_text
from django.utils.translation import ugettext_lazy as _

class FieldFile(File):

    def __init__(self, instance, field, name):
        super(FieldFile, self).__init__(None, name)
        self.instance = instance
        self.field = field
        self.storage = field.storage
        self._committed = True
        return

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return self.name == other.name
        return self.name == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def _require_file(self):
        if not self:
            raise ValueError("The '%s' attribute has no file associated with it." % self.field.name)

    def _get_file(self):
        self._require_file()
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    def _set_file(self, file):
        self._file = file

    def _del_file(self):
        del self._file

    file = property(_get_file, _set_file, _del_file)

    @property
    def path(self):
        self._require_file()
        return self.storage.path(self.name)

    @property
    def url(self):
        self._require_file()
        return self.storage.url(self.name)

    @property
    def size(self):
        self._require_file()
        if not self._committed:
            return self.file.size
        return self.storage.size(self.name)

    def open(self, mode='rb'):
        self._require_file()
        if hasattr(self, '_file') and self._file is not None:
            self.file.open(mode)
        else:
            self.file = self.storage.open(self.name, mode)
        return

    open.alters_data = True

    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(name, content, max_length=self.field.max_length)
        setattr(self.instance, self.field.name, self.name)
        self._committed = True
        if save:
            self.instance.save()

    save.alters_data = True

    def delete(self, save=True):
        if not self:
            return
        else:
            if hasattr(self, '_file'):
                self.close()
                del self.file
            self.storage.delete(self.name)
            self.name = None
            setattr(self.instance, self.field.name, self.name)
            self._committed = False
            if save:
                self.instance.save()
            return

    delete.alters_data = True

    @property
    def closed(self):
        file = getattr(self, '_file', None)
        return file is None or file.closed

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()
        return

    def __getstate__(self):
        return {'name': self.name, 'closed': False, '_committed': True, '_file': None}


class FileDescriptor(object):
    """
    The descriptor for the file attribute on the model instance. Returns a
    FieldFile when accessed so you can do stuff like::

        >>> from myapp.models import MyModel
        >>> instance = MyModel.objects.get(pk=1)
        >>> instance.file.size

    Assigns a file object on assignment so you can do::

        >>> with open('/path/to/hello.world', 'r') as f:
        ...     instance.file = File(f)
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        else:
            if self.field.name in instance.__dict__:
                file = instance.__dict__[self.field.name]
            else:
                instance.refresh_from_db(fields=[self.field.name])
                file = getattr(instance, self.field.name)
            if isinstance(file, six.string_types) or file is None:
                attr = self.field.attr_class(instance, self.field, file)
                instance.__dict__[self.field.name] = attr
            elif isinstance(file, File) and not isinstance(file, FieldFile):
                file_copy = self.field.attr_class(instance, self.field, file.name)
                file_copy.file = file
                file_copy._committed = False
                instance.__dict__[self.field.name] = file_copy
            elif isinstance(file, FieldFile) and not hasattr(file, 'field'):
                file.instance = instance
                file.field = self.field
                file.storage = self.field.storage
            elif isinstance(file, FieldFile) and instance is not file.instance:
                file.instance = instance
            return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class FileField(Field):
    attr_class = FieldFile
    descriptor_class = FileDescriptor
    description = _('File')

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        self._primary_key_set_explicitly = 'primary_key' in kwargs
        self.storage = storage or default_storage
        self.upload_to = upload_to
        kwargs['max_length'] = kwargs.get('max_length', 100)
        super(FileField, self).__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super(FileField, self).check(**kwargs)
        errors.extend(self._check_primary_key())
        errors.extend(self._check_upload_to())
        return errors

    def _check_primary_key(self):
        if self._primary_key_set_explicitly:
            return [
             checks.Error("'primary_key' is not a valid argument for a %s." % self.__class__.__name__, obj=self, id='fields.E201')]
        else:
            return []

    def _check_upload_to(self):
        if isinstance(self.upload_to, six.string_types) and self.upload_to.startswith('/'):
            return [
             checks.Error("%s's 'upload_to' argument must be a relative path, not an absolute path." % self.__class__.__name__, obj=self, id='fields.E202', hint='Remove the leading slash.')]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(FileField, self).deconstruct()
        if kwargs.get('max_length') == 100:
            del kwargs['max_length']
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return (
         name, path, args, kwargs)

    def get_internal_type(self):
        return 'FileField'

    def get_prep_value(self, value):
        """Returns field's value prepared for saving into a database."""
        value = super(FileField, self).get_prep_value(value)
        if value is None:
            return
        else:
            return six.text_type(value)

    def pre_save(self, model_instance, add):
        """Returns field's value just before saving."""
        file = super(FileField, self).pre_save(model_instance, add)
        if file and not file._committed:
            file.save(file.name, file.file, save=False)
        return file

    def contribute_to_class(self, cls, name, **kwargs):
        super(FileField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_directory_name(self):
        warnings.warn('FileField now delegates file name and folder processing to the storage. get_directory_name() will be removed in Django 2.0.', RemovedInDjango20Warning, stacklevel=2)
        return os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(self.upload_to))))

    def get_filename(self, filename):
        warnings.warn('FileField now delegates file name and folder processing to the storage. get_filename() will be removed in Django 2.0.', RemovedInDjango20Warning, stacklevel=2)
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))

    def generate_filename(self, instance, filename):
        """
        Apply (if callable) or prepend (if a string) upload_to to the filename,
        then delegate further processing of the name to the storage backend.
        Until the storage layer, all file paths are expected to be Unix style
        (with forward slashes).
        """
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            dirname = force_text(datetime.datetime.now().strftime(force_str(self.upload_to)))
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)

    def save_form_data(self, instance, data):
        if data is not None:
            if not data:
                data = ''
            setattr(instance, self.name, data)
        return

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FileField, 'max_length': self.max_length}
        if 'initial' in kwargs:
            defaults['required'] = False
        defaults.update(kwargs)
        return super(FileField, self).formfield(**defaults)


class ImageFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for ImageFields. The only difference is
    assigning the width/height to the width_field/height_field, if appropriate.
    """

    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(ImageFileDescriptor, self).__set__(instance, value)
        if previous_file is not None:
            self.field.update_dimension_fields(instance, force=True)
        return


class ImageFieldFile(ImageFile, FieldFile):

    def delete(self, save=True):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super(ImageFieldFile, self).delete(save)


class ImageField(FileField):
    attr_class = ImageFieldFile
    descriptor_class = ImageFileDescriptor
    description = _('Image')

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        super(ImageField, self).__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super(ImageField, self).check(**kwargs)
        errors.extend(self._check_image_library_installed())
        return errors

    def _check_image_library_installed(self):
        try:
            from PIL import Image
        except ImportError:
            return [
             checks.Error('Cannot use ImageField because Pillow is not installed.', hint='Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".', obj=self, id='fields.E210')]

        return []

    def deconstruct(self):
        name, path, args, kwargs = super(ImageField, self).deconstruct()
        if self.width_field:
            kwargs['width_field'] = self.width_field
        if self.height_field:
            kwargs['height_field'] = self.height_field
        return (
         name, path, args, kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super(ImageField, self).contribute_to_class(cls, name, **kwargs)
        if not cls._meta.abstract:
            signals.post_init.connect(self.update_dimension_fields, sender=cls)

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        """
        Updates field's width and height fields, if defined.

        This method is hooked up to model's post_init signal to update
        dimensions after instantiating a model instance.  However, dimensions
        won't be updated if the dimensions fields are already populated.  This
        avoids unnecessary recalculation when loading an object from the
        database.

        Dimensions can be forced to update with force=True, which is how
        ImageFileDescriptor.__set__ calls this method.
        """
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields or self.attname not in instance.__dict__:
            return
        file = getattr(instance, self.attname)
        if not file and not force:
            return
        else:
            dimension_fields_filled = not (self.width_field and not getattr(instance, self.width_field) or self.height_field and not getattr(instance, self.height_field))
            if dimension_fields_filled and not force:
                return
            if file:
                width = file.width
                height = file.height
            else:
                width = None
                height = None
            if self.width_field:
                setattr(instance, self.width_field, width)
            if self.height_field:
                setattr(instance, self.height_field, height)
            return

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ImageField}
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)