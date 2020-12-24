# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sortfiles/bin.py
# Compiled at: 2018-06-15 09:08:17
import glob, sys, os, os.path, shutil

def sort_directory(directory):
    items = glob.glob(('{}/*').format(directory))
    for item in items:
        obj = {}
        extension = os.path.splitext(item)[1]
        obj['extension'] = extension
        obj['fullname'] = item
        ext_dir = ('{}/{}').format(directory, extension.replace('.', ''))
        if not os.path.isdir(item) and not os.path.islink(item):
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir)
            try:
                print ('moving: {} to {}').format(item, ext_dir)
                shutil.move(item.decode('utf-8'), ext_dir)
            except Exception:
                pass


def run():
    if len(sys.argv) < 2:
        print 'No directory provided'
        quit()
    directory = sys.argv[1]
    sort_directory(directory)