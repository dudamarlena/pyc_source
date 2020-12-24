# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\versionHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 3477 bytes
import os, platform
import aigpy.configHelper as ConfigHelper

def getVersion(in_filepath):
    try:
        if os.path.isfile(in_filepath) is False:
            return ''
        if os.path.exists(in_filepath) is False:
            return ''
        sysName = platform.system()
        if sysName == 'Windows':
            import win32api
            info = win32api.GetFileVersionInfo(in_filepath, os.sep)
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms),
             win32api.HIWORD(ls), win32api.LOWORD(ls))
            return version
        if sysName == 'Linux':
            return ''
        return ''
    except:
        return ''


def cmpVersion(ver1, ver2):
    vlist1 = ver1.split('.')
    vlist2 = ver2.split('.')
    iIndex = 0
    for obj in vlist1:
        if len(vlist2) <= iIndex:
            break
        if obj > vlist2[iIndex]:
            return 1
        if obj < vlist2[iIndex]:
            return -1
        iIndex = iIndex + 1

    return 0


class VersionFile(object):

    def __init__(self, path=None):
        self.version = None
        self.mainFile = None
        self.elseFileList = []
        self.isZip = 0
        self.zipFile = ''
        if path != None:
            self.readFile(path)

    def saveFile(self, path):
        if path is None or self.version is None or self.mainFile is None:
            return False
        if self.isZip != 0:
            if self.zipFile == '':
                return False
        check = ConfigHelper.SetValue('common', 'version', self.version, path)
        check = ConfigHelper.SetValue('common', 'mainfile', self.mainFile, path)
        if check is False:
            return False
        check = ConfigHelper.SetValue('common', 'iszip', self.isZip, path)
        check = ConfigHelper.SetValue('common', 'zipfile', self.isZip, path)
        if self.elseFileList is None or len(self.elseFileList) == 0:
            return True
        ConfigHelper.SetValue('common', 'elsenum', len(self.elseFileList), path)
        index = 0
        for item in self.elseFileList:
            ConfigHelper.SetValue('common', 'else' + index, item, path)
            index = index + 1

        return True

    def readFile(self, path):
        if path is None:
            return False
        ver = ConfigHelper.GetValue('common', 'version', '', path)
        mainFile = ConfigHelper.GetValue('common', 'mainfile', '', path)
        if ver == '' or mainFile == '':
            return False
        isZip = ConfigHelper.GetValue('common', 'iszip', 0, path)
        isZip = int(isZip)
        zipFile = ConfigHelper.GetValue('common', 'zipfile', '', path)
        if isZip != 0 or zipFile == '':
            return False
        elseNum = ConfigHelper.GetValue('common', 'elsenum', 0, path)
        elseNum = int(elseNum)
        elseList = []
        index = 0
        if elseNum > 0:
            obj = ConfigHelper.GetValue('common', 'else' + index, '', path)
            index = index + 1
            elseList.append(obj)
        self.version = ver
        self.mainFile = mainFile
        self.elseFileList = elseList
        self.isZip = isZip
        self.zipFile = zipFile
        return True