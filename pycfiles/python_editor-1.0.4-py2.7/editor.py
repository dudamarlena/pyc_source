# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/editor.py
# Compiled at: 2019-02-01 02:10:18
"""Tools for invoking editors programmatically."""
from __future__ import print_function
import sys, locale, os.path, subprocess, tempfile
from distutils.spawn import find_executable
__all__ = [
 'edit',
 'get_editor',
 'EditorError']
__version__ = '1.0.4'

class EditorError(RuntimeError):
    pass


def get_default_editors():
    return [
     'editor',
     'vim',
     'emacs',
     'nano']


def get_editor_args(editor):
    if editor in ('vim', 'gvim', 'vim.basic', 'vim.tiny'):
        return ['-f', '-o']
    else:
        if editor == 'emacs':
            return ['-nw']
        if editor == 'gedit':
            return ['-w', '--new-window']
        if editor == 'nano':
            return ['-R']
        return []


def get_editor():
    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR')
    if editor:
        return editor
    else:
        for ed in get_default_editors():
            path = find_executable(ed)
            if path is not None:
                return path

        raise EditorError('Unable to find a viable editor on this system.Please consider setting your $EDITOR variable')
        return


def get_tty_filename():
    if sys.platform == 'win32':
        return 'CON:'
    return '/dev/tty'


def edit(filename=None, contents=None, use_tty=None, suffix=''):
    editor = get_editor()
    args = [editor] + get_editor_args(os.path.basename(os.path.realpath(editor)))
    if use_tty is None:
        use_tty = sys.stdin.isatty() and not sys.stdout.isatty()
    if filename is None:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix)
        filename = tmp.name
    if contents is not None:
        if hasattr(contents, 'encode'):
            contents = contents.encode()
        with open(filename, mode='wb') as (f):
            f.write(contents)
    args += [filename]
    stdout = None
    if use_tty:
        stdout = open(get_tty_filename(), 'wb')
    proc = subprocess.Popen(args, close_fds=True, stdout=stdout)
    proc.communicate()
    with open(filename, mode='rb') as (f):
        return f.read()
    return


def _get_editor(ns):
    print(get_editor())


def _edit(ns):
    contents = ns.contents
    if contents is not None:
        contents = contents.encode(locale.getpreferredencoding())
    print(edit(filename=ns.path, contents=contents))
    return


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers()
    cmd = sp.add_parser('get-editor')
    cmd.set_defaults(cmd=_get_editor)
    cmd = sp.add_parser('edit')
    cmd.set_defaults(cmd=_edit)
    cmd.add_argument('path', type=str, nargs='?')
    cmd.add_argument('--contents', type=str)
    ns = ap.parse_args()
    ns.cmd(ns)