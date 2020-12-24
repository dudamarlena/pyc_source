# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/bundleglobals.py
# Compiled at: 2012-10-12 07:02:39
import coils.core

def get_note_path(note_id):
    return '%s/documents/%d.txt' % (Backend.fs_root(), note_id)


def delete_file(name):
    path = '%s/documents/%s' % (Backend.fs_root(), name)
    os.remove(path)