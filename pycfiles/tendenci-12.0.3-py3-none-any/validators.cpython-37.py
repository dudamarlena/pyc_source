# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/files/validators.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 3717 bytes
import magic
from os.path import splitext
from django.core.exceptions import ValidationError
import django.utils.translation as _
from django.template.defaultfilters import filesizeformat
from tendenci.apps.files.utils import get_max_file_upload_size, get_allowed_upload_file_exts, get_allowed_mimetypes

class FileValidator(object):
    __doc__ = "\n    Validator for files, checking the size, extension and mimetype.\n\n    Initialization parameters:\n        allowed_extensions: iterable with allowed file extensions\n            ie. ('.txt', '.doc')\n        allowd_mimetypes: iterable with allowed mimetypes\n            ie. ('image/png', )\n        min_size: minimum number of bytes allowed\n            ie. 100\n        max_size: maximum number of bytes allowed\n            ie. 24*1024*1024 for 24 MB\n\n    Usage example:\n\n        file = forms.FileField(validators=[FileValidator(allowed_extensions=('.pdf', '.doc',))], ...)\n\n    "
    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', get_allowed_upload_file_exts())
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', get_allowed_mimetypes(self.allowed_extensions))
        self.max_size = kwargs.pop('max_size', get_max_file_upload_size(file_module=True))

    def __call__(self, values):
        """
        Check the extension, content type and file size.
        """
        if not isinstance(values, list):
            values = [
             values]
        for value in values:
            if ',' in value.name:
                raise ValidationError(_('Invalid file name - comma is not allowed.'))
            if '..' in value.name:
                raise ValidationError(_('Invalid file name - two consecutive dots are not allowed.'))
            ext = splitext(value.name)[1].lower()
            if self.allowed_extensions:
                if ext not in self.allowed_extensions:
                    message = self.extension_message % {'extension':ext, 
                     'allowed_extensions':', '.join(self.allowed_extensions)}
                    raise ValidationError(message)
                else:
                    try:
                        mime_type = magic.from_buffer((value.read(1024)), mime=True)
                        if self.allowed_mimetypes:
                            if mime_type not in self.allowed_mimetypes:
                                message = self.mime_message % {'mimetype':mime_type, 
                                 'allowed_mimetypes':', '.join(self.allowed_mimetypes)}
                                raise ValidationError(message)
                    except AttributeError:
                        raise ValidationError(_('File type is not valid'))

                filesize = len(value)
                if self.max_size and filesize > self.max_size:
                    message = self.max_size_message % {'size':filesizeformat(filesize), 
                     'allowed_size':filesizeformat(self.max_size)}
                    raise ValidationError(message)