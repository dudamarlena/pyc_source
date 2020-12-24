# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\pipHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 1137 bytes
"""
@File    :   pipHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   pip server tool
"""
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