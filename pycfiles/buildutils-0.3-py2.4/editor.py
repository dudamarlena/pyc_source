# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/editor.py
# Compiled at: 2007-08-08 19:58:56
"""
Routines for bringing up an external editor on a string or file.
"""
import os
from tempfile import NamedTemporaryFile
EDITOR = None

def get_editor():
    """
    Figure out which editing program to use.

    - This module's EDITOR attribute.
    - The EDITOR environment variable.
    - The VISUAL environment variable.
    - vi
    """
    editors = [
     EDITOR, os.getenv('EDITOR'), os.getenv('VISUAL'), 'vi']
    for e in editors:
        if e:
            return e


def edit_string(content):
    """
    Spawn an editor and return edited string content.

    Take a string, dump it to a tempfile, spawn the editor,
    read the modified tempfile, and close the tempfile.

    If the editor is interrupted, ``None`` is returned.
    """
    fd = NamedTemporaryFile()
    fd.write(content)
    fd.flush()
    rslt = edit_file(fd)
    fd.close()
    return rslt


def edit_file(filehandle):
    """
    Spawn an editor and return edited file content.
    
    Expects a filehandle as returned by ``tempfile.NamedTemporaryFile()``.
    Note that filehandle is not closed. The caller is responsible for
    managing the filehandle.
    """
    editor = get_editor()
    try:
        x = os.spawnlp(os.P_WAIT, editor, editor, filehandle.name)
    except KeyboardInterrupt:
        return
    else:
        if x != 0:
            return

    filehandle.seek(0)
    return filehandle.read()


__all__ = [
 'EDITOR', 'get_editor', 'edit_string', 'edit_file']