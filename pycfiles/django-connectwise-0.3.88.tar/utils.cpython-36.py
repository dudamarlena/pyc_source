# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/utils.py
# Compiled at: 2020-03-04 20:06:07
# Size of source mod 2**32: 2996 bytes
import hashlib, re
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.storage import default_storage
from django.conf import settings
_underscorer1 = re.compile('(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
FILENAME_EXTENSION_RE = re.compile('\\.([\\w]*)$')

def camel_to_snake(s):
    """
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    subbed = _underscorer1.sub('\\1_\\2', s)
    return _underscorer2.sub('\\1_\\2', subbed).lower()


def snake_to_camel(snake_case_text):
    tokens = snake_case_text.split('_')
    return ''.join(word.capitalize() for word in tokens)


def get_hash(content):
    """Return the hex SHA-1 hash of the given content."""
    return hashlib.sha1(content).hexdigest()


def get_filename_extension(filename):
    """From the given filename, return the extension,
    or None if it can't be parsed.
    """
    m = FILENAME_EXTENSION_RE.search(filename)
    if m:
        return m.group(1)


def generate_filename(size, current_filename, extension):
    img_dimensions = 'x'.join([str(i) for i in size])
    filename = '{}{}.{}'.format(current_filename, img_dimensions, extension)
    return filename


def remove_thumbnail(avatar_filename):
    thumbnail_size = {'avatar':(80, 80), 
     'micro_avatar':(20, 20)}
    extension = get_filename_extension(avatar_filename)
    for size in thumbnail_size:
        filename = generate_filename(thumbnail_size[size], avatar_filename, extension)
        default_storage.delete(filename)

    default_storage.delete(avatar_filename)


def generate_thumbnail(avatar, size, extension, filename):
    filename = generate_filename(size, filename, extension)
    avatar_image = Image.open(BytesIO(avatar))
    thumbnail = ImageOps.fit(avatar_image, size, Image.ANTIALIAS)
    if extension.lower() == 'jpg':
        extension = 'jpeg'
    byte_stream = BytesIO()
    thumbnail.save(byte_stream, format=extension)
    avatar_file = ContentFile(byte_stream.getvalue())
    return (
     avatar_file, filename)


class DjconnectwiseSettings:

    def get_settings(self):
        request_settings = {'timeout':30.0, 
         'batch_size':50, 
         'max_attempts':3, 
         'schedule_entry_conditions_size':0, 
         'response_version':'2019.5', 
         'sync_child_tickets':True, 
         'sync_time_and_note_entries':True}
        if hasattr(settings, 'DJCONNECTWISE_CONF_CALLABLE'):
            request_settings.update(settings.DJCONNECTWISE_CONF_CALLABLE())
        return request_settings