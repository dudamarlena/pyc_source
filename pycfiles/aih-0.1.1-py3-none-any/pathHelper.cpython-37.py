# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\pathHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 3509 bytes
__doc__ = '\n@File    :   pathHelper.py\n@Time    :   2018/12/17\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, shutil

def getDiffTmpPathName(basePath):
    """Get tmp file name like 'Tmp1'"""
    count = 0
    basePath = basePath.replace('\\', '/')
    basePath = basePath.strip()
    basePath = basePath.rstrip('/')
    path = basePath + '/Tmp' + str(count)
    while os.path.exists(path):
        count = count + 1
        path = basePath + '/Tmp' + str(count)

    return path


def mkdirs(path):
    path = path.replace('\\', '/')
    path = path.strip()
    path = path.rstrip('/')
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


def remove(path):
    """Remove file or dir"""
    try:
        if os.path.exists(path) is False:
            return True
        if os.path.isfile(path) is True:
            os.remove(path)
        if os.path.isdir(path) is True:
            shutil.rmtree(path)
        return True
    except:
        return False


def copyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        return False
    fpath, fname = os.path.split(dstfile)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    shutil.copyfile(srcfile, dstfile)
    return True


def replaceLimitChar(path, newChar):
    if path is None:
        return ''
    if newChar is None:
        newChar = ''
    path = path.replace(':', newChar)
    path = path.replace('/', newChar)
    path = path.replace('?', newChar)
    path = path.replace('<', newChar)
    path = path.replace('>', newChar)
    path = path.replace('|', newChar)
    path = path.replace('\\', newChar)
    path = path.replace('*', newChar)
    path = path.replace('"', newChar)
    return path


def getDirName(filepath):
    """e:/test/file.txt --> e:/test/"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return './'
    return filepath[0:index + 1]


def getFileName(filepath):
    """e:/test/file.txt --> file.txt"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return filepath
    return filepath[index + 1:len(filepath)]


def getFileNameWithoutExtension(filepath):
    """e:/test/file.txt --> file"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return filepath
    return filepath[0:index]


def getFileExtension(filepath):
    """e:/test/file.txt --> .txt"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return
    return filepath[index:len(filepath)]


def getDirSize(path):
    try:
        if os.path.isdir(path) is False:
            return 0
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])

        return size
    except:
        return 0


def getDirFiles(path):
    try:
        if os.path.isdir(path) is False:
            return []
        ret = []
        for root, dirs, files in os.walk(path):
            root = root.replace('\\', '/')
            for item in files:
                ret.append(root + '/' + item)

        return ret
    except:
        return []