# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niedbalski/src/vcs/vcs/utils/filesize.py
# Compiled at: 2016-04-08 09:25:43


def filesizeformat(bytes, sep=' '):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 B, 2.3 GB etc).

    Grabbed from Django (http://www.djangoproject.com), slightly modified.

    :param bytes: size in bytes (as integer)
    :param sep: string separator between number and abbreviation
    """
    try:
        bytes = float(bytes)
    except (TypeError, ValueError, UnicodeDecodeError):
        return '0%sB' % sep

    if bytes < 1024:
        size = bytes
        template = '%.0f%sB'
    elif bytes < 1048576:
        size = bytes / 1024
        template = '%.0f%sKB'
    elif bytes < 1073741824:
        size = bytes / 1024 / 1024
        template = '%.1f%sMB'
    else:
        size = bytes / 1024 / 1024 / 1024
        template = '%.2f%sGB'
    return template % (size, sep)