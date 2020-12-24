# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/hdiutil.py
# Compiled at: 2016-05-03 20:54:42
"""Module for OSX-specific utility.

Mounts DMG files.
"""
import os, shutil
from fftool import local
cmd_hdiutil = local('which hdiutil')

def attach(dmg_path, mountpoint):
    args = {'hdiutil': cmd_hdiutil, 
       'dmg_path': dmg_path, 
       'mountpoint': mountpoint}
    cmd = ('{hdiutil} attach {dmg_path} -mountpoint {mountpoint}').format(**args)
    local(cmd)


def detach(mountpoint):
    args = {'hdiutil': cmd_hdiutil, 
       'mountpoint': mountpoint}
    cmd = ('{hdiutil} detach {mountpoint}').format(**args)
    local(cmd)


def move_app(src, dest):
    if os.path.exists(dest):
        print ('Deleting existing {0} file').format(dest)
        shutil.rmtree(dest)
    print ('Moving {0} to {1}').format(src, dest)
    shutil.copytree(src, dest)


def extract_dmg(dmg_path, app_src_filename, app_dest_filename, channel):
    """Mount *.dmg image, copy the *.app dir, then unmount *.dmg image.
    """
    dmg_dirname = os.path.dirname(dmg_path)
    tmp_dirname = os.path.join(dmg_dirname, '_dmg_temp')
    app_src_path = os.path.join(tmp_dirname, app_src_filename)
    app_dest_path = os.path.join(dmg_dirname, app_dest_filename)
    attach(dmg_path, mountpoint=tmp_dirname)
    move_app(app_src_path, app_dest_path)
    detach(mountpoint=tmp_dirname)