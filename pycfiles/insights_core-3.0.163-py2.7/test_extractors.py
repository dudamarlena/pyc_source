# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_extractors.py
# Compiled at: 2020-04-30 14:03:01
import os, shlex, subprocess, tempfile, zipfile
from contextlib import closing
from insights.core.hydration import get_all_files
from insights.core.archives import extract

def test_with_zip():
    tmp_dir = tempfile.mkdtemp()
    d = os.path.join(tmp_dir, 'sys', 'kernel')
    os.makedirs(d)
    with open(os.path.join(d, 'kexec_crash_size'), 'w') as (f):
        f.write('ohyeahbaby')
    try:
        os.unlink('/tmp/test.zip')
    except:
        pass

    def _add_to_zip(zf, path, zippath):
        if os.path.isfile(path):
            zf.write(path, zippath, zipfile.ZIP_DEFLATED)
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in os.listdir(path):
                _add_to_zip(zf, os.path.join(path, nm), os.path.join(zippath, nm))

    with closing(zipfile.ZipFile('/tmp/test.zip', 'w')) as (zf):
        _add_to_zip(zf, tmp_dir, os.path.basename(tmp_dir))
    try:
        with extract('/tmp/test.zip') as (ex):
            assert any(f.endswith('/sys/kernel/kexec_crash_size') for f in get_all_files(ex.tmp_dir))
    finally:
        os.unlink('/tmp/test.zip')

    subprocess.call(shlex.split('rm -rf %s' % tmp_dir))