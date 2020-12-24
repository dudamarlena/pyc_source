# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/compat.py
# Compiled at: 2020-04-27 20:27:30
# Size of source mod 2**32: 362 bytes
from six import text_type as unicode
import six
unicode
if six.PY3:
    import shutil

    def is_command(cmd):
        return bool(shutil.which(cmd))


    def open_for_csv(*args, **kw):
        kw['newline'] = ''
        return open(*args, **kw)


else:
    from webbrowser import _iscommand
    is_command = _iscommand
    open_for_csv = open