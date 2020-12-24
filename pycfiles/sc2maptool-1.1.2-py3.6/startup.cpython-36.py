# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2maptool\startup.py
# Compiled at: 2018-10-07 19:32:09
# Size of source mod 2**32: 1415 bytes
import distutils.dir_util, os, shutil
from sc2gameLobby.gameConfig import Config
from sc2maptool.__version__ import __version__
from sc2maptool import constants as c

def setup():
    """ensure that the maptool's maps are installed in the SC2 install maps directory simply by importing this module"""
    try:
        _cfg = Config()
        maptoolDir = os.path.join(_cfg.installedApp.mapsDir, c.PATH_MAPTOOLDIR)
    except Exception as e:
        print('WARNING: %s' % e)
        c.PATH_MAP_INSTALL = c.MAPS_FOLDER
        return c.MAPS_FOLDER

    c.PATH_MAP_INSTALL = os.path.join(maptoolDir, __version__)
    if not os.path.isdir(c.PATH_MAP_INSTALL):
        if os.path.isdir(maptoolDir):
            shutil.rmtree(maptoolDir)
        distutils.dir_util.copy_tree(c.MAPS_FOLDER, c.PATH_MAP_INSTALL)
    return c.PATH_MAP_INSTALL


if __name__ == '__main__':
    setup()