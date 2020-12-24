# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\zipHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 2410 bytes
import os, tarfile, zipfile

def _getParaType(para):
    r"""Return 0-file path \ 1-dir path \ 2-file paths"""
    try:
        if os.path.isfile(para):
            return 0
    except:
        pass

    try:
        if os.path.isdir(para):
            return 1
    except:
        pass

    return 2


def _getZipType(zipName):
    """Return 'tar' or 'zip' """
    try:
        name = os.path.basename(zipName)
        if name.lower().find('.tar') > 0:
            return 'tar'
        return 'zip'
    except:
        pass


def _open(zipName, ptype, mode='w'):
    """Open zip file"""
    try:
        if ptype == 'tar':
            pZip = tarfile.open(zipName, mode)
        else:
            pZip = zipfile.ZipFile(zipName, mode, zipfile.ZIP_DEFLATED)
        return pZip
    except:
        return


def _write(pZip, ptype, pfilename, parcname):
    try:
        if ptype == 'tar':
            pZip.add(pfilename, arcname=parcname)
        else:
            pZip.write(pfilename, arcname=parcname)
        return True
    except:
        return False


def myzip(inPath, outPath):
    """zip files or dir

    - inPath: file path/file paths/dir
    - zipName: output name
    - Return: True/False         
    """
    check = _getParaType(inPath)
    ptype = _getZipType(outPath)
    try:
        pZip = _open(outPath, ptype)
        if check == 2:
            for file in inPath:
                pZip._write(pZip, ptype, file, os.path.basename(file))

        if check == 0:
            pZip._write(pZip, ptype, inPath, os.path.basename(inPath))
        if check == 1:
            name = os.path.dirname(inPath)
            for dirpath, dirnames, filenames in os.walk(inPath):
                fpath = dirpath.replace(name, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    pZip._write(pZip, ptype, os.path.join(dirpath, filename), fpath + filename)

        pZip.close()
        return True
    except:
        return False


def myunzip(zipName, outPath):
    ptype = _getZipType(zipName)
    try:
        pZip = _open(zipName, ptype, 'r')
        pZip.extractall(path=outPath)
        pZip.close()
        return True
    except:
        return False