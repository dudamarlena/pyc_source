# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\core\manage_files.py
# Compiled at: 2019-09-09 14:21:50
import compileall, os, shutil, errno

def compile_and_copy(src, dest, *patterns):
    """ Para compilar archivos y copiarlos al repositorio de compilado. """
    base_name = os.path.dirname(dest)
    dest_dir = os.path.abspath(dest)
    compileall.compile_dir(src, force=True)
    if os.path.isdir(base_name):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        try:
            shutil.copytree(src, dest_dir, ignore=shutil.ignore_patterns(*patterns))
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest_dir)
            else:
                print 'Directory not copied. Error: %s' % e