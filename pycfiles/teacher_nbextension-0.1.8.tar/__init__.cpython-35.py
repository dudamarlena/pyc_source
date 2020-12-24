# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/i/LABS/teacher_nbextension/teacher_nbextension/__init__.py
# Compiled at: 2018-05-23 19:56:28
# Size of source mod 2**32: 591 bytes
from .handlers import load_jupyter_server_extension

def _jupyter_nbextension_paths():
    return [
     dict(section='notebook', src='static', dest='teacher_nbextension', require='teacher_nbextension/main')]


def _jupyter_server_extension_paths():
    """API for server extension installation on notebook 4.2"""
    return [
     {'module': 'teacher_nbextension'}]