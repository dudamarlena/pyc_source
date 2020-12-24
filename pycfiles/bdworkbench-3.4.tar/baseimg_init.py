# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krishna/sources/catalogsdk/bdworkbench/baseimg/baseimg_init.py
# Compiled at: 2018-04-10 18:30:24
from __future__ import print_function
from .. import SubCommand
from ..utils.config import SECTION_WB, KEY_SDKBASE
import os, shutil

class BaseimgInit(SubCommand):
    """

    """

    def __init__(self, config, inmemStore, cmdObj):
        SubCommand.__init__(self, config, inmemStore, cmdObj, 'init')

    def getSubcmdDescripton(self):
        return 'When manually developing appconfig script, this copies a few ' + 'useful scripts that you can use as starter code.'

    def populateParserArgs(self, subparser):
        subparser.add_argument('--os', dest='baseimg', action='store', required=True, choices=[
         'centos6', 'rhel6', 'centos7', 'rhel7', 'ubuntu16'], help='Copy all the files related to building docker image that can be used as a base for apps on BlueData EPIC. The files are copied to the current directory.')

    def run(self, pArgs):
        sdkbase = self.config.get(SECTION_WB, KEY_SDKBASE)
        baseImgDir = os.path.join(sdkbase, 'baseimg')
        depsSrcDir = os.path.join(baseImgDir, 'deps')
        osBaseimgSrc = ''
        if pArgs.baseimg == 'centos6' or pArgs.baseimg == 'rhel6':
            osBaseimgSrc = os.path.join(baseImgDir, 'centos6')
            depsRelativeDir = os.path.join('template', 'deps')
        elif pArgs.baseimg == 'centos7' or pArgs.baseimg == 'rhel7':
            osBaseimgSrc = os.path.join(baseImgDir, 'centos7')
            depsRelativeDir = None
        elif pArgs.baseimg == 'ubuntu16':
            osBaseimgSrc = os.path.join(baseImgDir, 'ubuntu')
            depsRelativeDir = os.path.join('ubuntu16', 'deps')
        else:
            print('ERROR: Unknown baseimg - %s' % pArgs.baseimg)
            return False
        destDir = os.path.join(os.getcwd(), pArgs.baseimg)
        if depsRelativeDir:
            depsDestDir = os.path.join(destDir, depsRelativeDir)
        else:
            depsDestDir = None
        try:
            if os.path.exists(destDir):
                print('ERROR: Destination directory exists.')
                print("ERROR: Please remove '%s' before proceeding." % destDir)
                return False
            shutil.copytree(osBaseimgSrc, destDir)
            if depsDestDir:
                shutil.copytree(depsSrcDir, depsDestDir)
        except Exception, e:
            print('ERROR:', e)
            return False

        return True

    def complete(self, text, argsList):
        return []