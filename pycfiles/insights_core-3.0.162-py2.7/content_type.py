# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/util/content_type.py
# Compiled at: 2019-05-16 13:41:33
import shlex, subprocess
from subprocess import PIPE
import six
from threading import Lock
try:
    from insights.contrib import magic
except Exception:
    magic_loaded = False
else:
    mime_flag = magic.MAGIC_MIME_TYPE if hasattr(magic, 'MAGIC_MIME_TYPE') else 16
    _magic = magic.open(mime_flag | magic.CONTINUE)
    _magic.load()
    magic_loaded = True

magic_lock = Lock()

def from_file(name):
    if magic_loaded:
        with magic_lock:
            return six.b(_magic.file(name)).decode('unicode-escape').splitlines()[0].strip()
    else:
        cmd = 'file --mime-type -b %s'
        p = subprocess.Popen(shlex.split(cmd % name), stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        return stdout.strip().decode('utf-8')


def from_buffer(b):
    if magic_loaded:
        with magic_lock:
            return _magic.buffer(b)
    else:
        cmd = 'file --mime-type -b -'
        p = subprocess.Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate(b)
        return stdout.strip().decode('utf-8')