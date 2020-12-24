# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/files.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 1534 bytes
import six
from mediagoblin import mg_globals

def delete_media_files(media):
    """
    Delete all files associated with a MediaEntry

    Arguments:
     - media: A MediaEntry document
    """
    no_such_files = []
    for listpath in six.itervalues(media.media_files):
        try:
            mg_globals.public_store.delete_file(listpath)
        except OSError:
            no_such_files.append('/'.join(listpath))

    for attachment in media.attachment_files:
        try:
            mg_globals.public_store.delete_file(attachment['filepath'])
        except OSError:
            no_such_files.append('/'.join(attachment['filepath']))

    if no_such_files:
        raise OSError(', '.join(no_such_files))