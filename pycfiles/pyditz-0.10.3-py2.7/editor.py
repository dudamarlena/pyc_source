# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/editor.py
# Compiled at: 2016-11-27 06:27:17
"""
Text editor.
"""
from __future__ import print_function
import os, yaml, tempfile
from . import util
from .files import read_file, read_yaml_file
from .util import DitzError

class DitzEditor(object):
    """
    An editor for Ditz objects.
    """
    prefix = 'tmp-'
    suffix = '.yaml'
    textmode = False
    filetag = '<input>'

    def __init__(self, path):
        self.original = read_file(path)
        self.text = self.original
        self.error = None
        return

    def edit(self):
        """Edit the text and return it."""
        program = util.editor()
        if not program:
            raise DitzError('no text editor is configured')
        fp, filename = tempfile.mkstemp(prefix=self.prefix, suffix=self.suffix, text=self.textmode)
        os.write(fp, self.text.encode('utf-8'))
        os.close(fp)
        try:
            util.run_editor(program, filename)
            self.text = read_file(filename)
            err = self.validate(filename)
            if err:
                self.error = err.replace(filename, self.filetag)
            else:
                self.error = None
        finally:
            os.remove(filename)

        return self.text

    def validate(self, path):
        """Return validation error text or None."""
        try:
            obj = read_yaml_file(path)
            obj.normalize()
        except yaml.error.YAMLError as err:
            return str(err)
        except DitzError as err:
            return str(err)

        return

    @property
    def modified(self):
        """Whether text has been modified."""
        return self.text != self.original


if __name__ == '__main__':
    path = '../bugs/issue-3d1596d37cbd170f512eb939b97f5f22a3834c79.yaml'
    from ditz.objects import DitzObject
    editor = DitzEditor(path)
    print(editor.edit())
    print('Modified:', editor.modified)
    print('Error:', editor.error)