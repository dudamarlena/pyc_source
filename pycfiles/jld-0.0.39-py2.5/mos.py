# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\tools\mos.py
# Compiled at: 2009-02-10 21:26:52
""" OS tools
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mos.py 851 2009-02-11 02:26:52Z JeanLou.Dupont $'
import os
from stat import *
import jld.api as api

def existsPath(path):
    """ Verifies the existence of 'path'
    """
    try:
        info = os.stat(path)
    except:
        return False

    return info


def existsDir(path):
    """ Verifies the existence of 'path'
        and verifies it corresponds to a 'directory'
    """
    info = existsPath(path)
    if info is False:
        return False
    try:
        mode = info[ST_MODE]
        isdir = S_ISDIR(mode)
    except:
        return False

    return True


def replaceHome(path):
    """ Replaces the '~' string with
        the configured $HOME or $HOMEDRIVE+$HOMEPATH environment variables
    """
    return os.path.expanduser(path)


def createPathIfNotExists(path):
    """ Creates the required path
        IF it does not already exists.
        If the path is a directory => create directory hierarchy
        
        Does not attempt to trap/process exceptions.
    """
    if os.path.exists(path):
        return
    dir = os.path.dirname(path)
    if os.path.exists(dir):
        return
    if not os.path.exists(path):
        os.makedirs(dir)


def createDirIfNotExists(dir):
    """ Creates the specified directory path
        if it does not exist already.
    """
    if os.path.exists(dir):
        return
    if not os.path.exists(dir):
        os.makedirs(dir)


def initPath(path):
    """ Initializes a path.
        The folder hierarchy leading to
        the said path is created IFF it is not
        already in place.
        @param path: the target path
        @raise Exception:  
    """
    ppath = replaceHome(path)
    rep = existsDir(ppath)
    if rep:
        return ppath
    if rep is False:
        createFolderHierarchy(ppath)
    rep = existsDir(ppath)
    if rep is False:
        raise api.ErrorConfig('msg:error_init_folder', {'path': ppath})
    return ppath


def createFolderHierarchy(path):
    """ Creates a folder hierarchy
    """
    try:
        os.makedirs(path)
    except:
        raise api.ErrorConfig('msg:error_create_folder', {'path': path})


def nukedir(directory):
    """ Nukes an entire directory hierarchy (topdown)
    """
    for (root, dirs, files) in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    os.rmdir(directory)


if __name__ == '__main__':
    assert existsPath('C:\\')
    assert existsDir('C:\\')
    home = replaceHome('~')
    assert existsPath(home)