# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/tools.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 637 bytes
import uuid

def unique_file_name(self, file_name):
    """
    Generates Unique name for uploaded filess
    :param self: Filefield object Class
    :param file_name: uploaded file name
    :return: file path with the new filename
    """
    result = file_name.split('.')
    basename, ext = result[0], '.'.join(result[-1:])
    basename = 'uploads/' + basename
    path, file_actual_name = basename.rsplit('/', 1)
    new_name = str(uuid.uuid4())
    file_name = new_name + '.' + ext
    self.original_name = file_actual_name + '.' + ext
    return path + '/' + file_name