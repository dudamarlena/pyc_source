# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/storage.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 987 bytes
from django.conf import settings
from django.core.files.storage import get_storage_class

def get_default_storage():
    """
    Get a default storage class.
    """
    return get_storage_class(settings.DEFAULT_FILE_STORAGE)()


def get_static_storage():
    """
    Get a static storage class.
    """
    return get_storage_class(settings.STATICFILES_STORAGE)()


def get_file_content(name, storage_type='default'):
    """
    Get the file content from the specified storage.
    """
    if storage_type == 'static':
        storage = get_static_storage()
    else:
        storage = get_default_storage()
    f = storage.open(name)
    content = f.read()
    f.close()
    return content


def save_file_content(name, content, storage_type='default'):
    """
    Save the file content to the specified storage.
    """
    if storage_type == 'static':
        storage = get_static_storage()
    else:
        storage = get_default_storage()
    return storage.save(name, content)