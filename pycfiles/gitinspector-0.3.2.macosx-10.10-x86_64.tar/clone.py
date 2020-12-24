# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/clone.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
import shutil, subprocess, sys, tempfile
__cloned_path__ = None

def create(url):
    global __cloned_path__
    if url.startswith(b'file://') or url.startswith(b'git://') or url.startswith(b'http://') or url.startswith(b'https://') or url.startswith(b'ssh://'):
        location = tempfile.mkdtemp(suffix=b'.gitinspector')
        git_clone = subprocess.Popen((b'git clone {0} {1}').format(url, location), shell=True, bufsize=1, stdout=sys.stderr)
        git_clone.wait()
        if git_clone.returncode != 0:
            sys.exit(git_clone.returncode)
        __cloned_path__ = location
        return location
    return url


def delete():
    if __cloned_path__:
        shutil.rmtree(__cloned_path__, ignore_errors=True)