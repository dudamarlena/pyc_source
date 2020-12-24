# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\console.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import print_function, unicode_literals
import os, subprocess
from distutils.util import strtobool
from six.moves import input
from rbtools.utils.filesystem import make_tempfile

def confirm(question):
    """Interactively prompt for a Yes/No answer.

    Accepted values (case-insensitive) depend on distutils.util.strtobool():
    'Yes' values: y, yes, t, true, on, 1
    'No' values: n, no , f, false, off, 0
    """
    while True:
        full_question = b'%s [Yes/No]: ' % question
        answer = input(full_question.encode(b'utf-8')).lower()
        try:
            return strtobool(answer)
        except ValueError:
            print(b'%s is not a valid answer.' % answer)


def edit_text(content):
    """Allows a user to edit a block of text and returns the saved result.

    The environment's default text editor is used if available, otherwise
    vi is used.
    """
    tempfile = make_tempfile(content.encode(b'utf8'))
    editor = os.environ.get(b'VISUAL') or os.environ.get(b'EDITOR') or b'vi'
    try:
        subprocess.call(editor.split() + [tempfile])
    except OSError:
        print(b'No editor found. Set EDITOR environment variable or install vi.')
        raise

    f = open(tempfile)
    result = f.read()
    f.close()
    return result.decode(b'utf8')