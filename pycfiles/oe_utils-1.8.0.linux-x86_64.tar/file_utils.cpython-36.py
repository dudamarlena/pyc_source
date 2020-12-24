# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/utils/file_utils.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 1098 bytes
import datetime, math, os

def get_last_modified_date(filename):
    """
    Get the last modified date of a given file.

    :param filename: string: pathname of a file
    :return: Date
    """
    if os.path.isfile(filename):
        t = os.path.getmtime(filename)
        return datetime.date.fromtimestamp(t).strftime('%d/%m/%Y')


def get_file_size(filename):
    """
    Get the file size of a given file.

    :param filename: string: pathname of a file
    :return: human readable filesize
    """
    if os.path.isfile(filename):
        return convert_size(os.path.getsize(filename))


def convert_size(size_bytes):
    """
    Transform bytesize to a human readable filesize.

    :param size_bytes: bytesize
    :return: human readable filesize
    """
    if size_bytes == 0:
        return '0B'
    else:
        size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return '%s %s' % (s, size_name[i])