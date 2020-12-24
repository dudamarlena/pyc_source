# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\utils.py
# Compiled at: 2015-05-18 08:15:13
# Size of source mod 2**32: 783 bytes
import shutil, os, hashlib, logging
log = logging.getLogger(__name__)

def copy_only_new(src, dest):
    h1 = hashlib.sha1()
    h1.update(open(src))
    h2 = hashlib.sha1()
    h2.update(open(dest))
    if h1.hexdigest() != h2.hexdigest():
        try:
            log.info('Removing ' + dest)
            os.remove(dest)
            shutil.copy(src, dest)
        except Exception as e:
            log.warning(e)

    else:
        log.info("Didn't copy because same content")


def is_same_contents(file1, file2):
    h1 = hashlib.sha1()
    h2 = hashlib.sha1()
    with open(file1, 'rb') as (f):
        h1.update(f.read())
    with open(file2, 'rb') as (f):
        h2.update(f.read())
    return h1.hexdigest() == h2.hexdigest()