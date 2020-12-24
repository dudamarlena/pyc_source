# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/shortcuts.py
# Compiled at: 2012-12-12 10:05:53
from sorl.thumbnail import default

def get_thumbnail(file_, geometry_string, **options):
    """
    A shortcut for the Backend ``get_thumbnail`` method
    """
    return default.backend.get_thumbnail(file_, geometry_string, **options)


def delete(file_, delete_file=True):
    """
    A shortcut for the Backend ``delete`` method
    """
    return default.backend.delete(file_, delete_file)