# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/personal/Notable/scripts/../notable/editor.py
# Compiled at: 2013-03-11 20:10:26
import os, subprocess, threading, time, uuid

def launcher(path):
    subprocess.call(['gvim', '--nofork', path])
    time.sleep(2.5)
    os.remove(path)


def launch(uid, content):
    uid = uid or uuid.uuid4().hex
    path = os.path.join('/tmp', uid)
    with open(path, 'w') as (fh):
        fh.write(content)
    threading.Thread(args=(path,), target=launcher).start()
    return uid