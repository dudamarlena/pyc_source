# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\pipHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 1137 bytes
__doc__ = '\n@File    :   pipHelper.py\n@Time    :   2019/03/11\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   pip server tool\n'
import aigpy.netHelper as netHelper

def getInfo(projectName):
    """Get project information from pypi
    - Return: json or None                              
    """
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url, None)
    return ret


def getLastVersion(projectName):
    """Get project version from pypi
    - Return: str or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return
        return ret['info']['version']
    except:
        return


def getVersionList(projectName):
    """Get project all versions from pypi
    - Return: json or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return
        return ret['releases']
    except:
        return