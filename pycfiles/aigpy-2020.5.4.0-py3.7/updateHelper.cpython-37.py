# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\updateHelper.py
# Compiled at: 2019-05-08 11:43:35
# Size of source mod 2**32: 4567 bytes
"""
@File    :   updateHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import os, sys, time, shutil, win32api
import aigpy.netHelper as netHelper
import aigpy.pathHelper as pathHelper
import aigpy.cmdHelper as cmdHelper
import aigpy.systemHelper as systemHelper
import aigpy.versionHelper as versionHelper
import aigpy.configHelper as configHelper
import aigpy.zipHelper as zipHelper
from aigpy.versionHelper import VersionFile

class updateTool(object):

    def __init__(self, in__file__, name, url, curver, mainFile, elseList, zipFile=None):
        self._file_ = in__file__
        self.tmpName = name + '-NewVersion'
        self.verName = name + '-verinfo.ini'
        self.curPath = systemHelper.getOwnPath(in__file__)
        self.tmpPath = self.curPath + '\\' + self.tmpName
        self.verPath = self.curPath + '\\' + self.verName
        self.curVer = VersionFile()
        self.curVer.version = curver
        self.curVer.mainFile = mainFile
        self.curVer.elseFileList = elseList
        self.curVer.zipFile = zipFile
        if zipFile is not None:
            self.curVer.isZip = 1
        self.curVer.saveFile(self.verPath)
        self.netVer = VersionFile()
        self.netUrl = url

    def _getNetVerinfo(self):
        tmpFile = self.curPath + '\\' + 'aigpy-tmp.ini'
        if not netHelper.downloadFile(self.netUrl + '//' + self.verName, tmpFile):
            return False
        return self.netVer.readFile(tmpFile)

    def isNeedUpdate(self):
        if self.curVer.version is None:
            return False
        if self.netVer.version is None:
            if self._getNetVerinfo() is False:
                return False
        return versionHelper.cmpVersion(self.curVer.version, self.netVer.version) < 0

    def _downloadFiles(self):
        check = pathHelper.remove(self.tmpPath)
        check = pathHelper.mkdirs(self.tmpPath)
        if self.netVer.mainFile is None:
            return False
            if self.netVer.isZip == 0:
                plist = []
                plist.append(self.netVer.mainFile)
                for item in self.netVer.elseFileList:
                    plist.append(item)

                for item in plist:
                    urlpath = self.netUrl + '//' + item
                    topath = self.tmpPath + '\\' + item
                    if netHelper.downloadFile(urlpath, topath) is False:
                        return False

        else:
            urlpath = self.netUrl + '//' + self.netVer.zipFile
            topath = self.tmpPath + '\\' + self.netVer.zipFile
            if netHelper.downloadFile(urlpath, topath) is False:
                return False
            return zipHelper.unzip(topath, self.tmpPath)
        return True

    def go(self):
        bFlag = '-1'
        stri = cmdHelper.findInArgv('AIGPYUPDATE=')
        if stri != None:
            bFlag = stri[len('AIGPYUPDATE='):]
        if bFlag == '-1':
            if self.isNeedUpdate() == False:
                return False
            if self._downloadFiles() == False:
                return False
            para = sys.argv
            para.append('AIGPYUPDATE=0')
            para.remove(para[0])
            win32api.ShellExecute(0, 'open', self.tmpPath + '\\' + self.netVer.mainFile, cmdHelper.converArgvToStr(para), self.tmpPath, 0)
            return True
        if bFlag == '0':
            time.sleep(3)
            ver = VersionFile()
            tmpFile = self.curPath + '\\..\\' + 'aigpy-tmp.ini'
            ver.readFile(tmpFile)
            plist = []
            plist.append(ver.mainFile)
            for item in ver.elseFileList:
                plist.append(item)

            for item in plist:
                shutil.copyfile(self.curPath + '\\' + item, self.curPath + '\\..\\' + item)

            para = sys.argv
            para.remove(para[0])
            para.remove(stri)
            para.append('AIGPYUPDATE=2')
            win32api.ShellExecute(0, 'open', self.curPath + '\\..\\' + ver.mainFile, cmdHelper.converArgvToStr(para), self.curPath + '\\..\\', 1)
            return True
        return False