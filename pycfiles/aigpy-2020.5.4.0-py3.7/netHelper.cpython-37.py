# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\netHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 3572 bytes
"""
@File    :   netHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import re, os, sys, json, socket, requests
from aigpy.progressHelper import ProgressTool
from aigpy.convertHelper import convertStorageUnit
from aigpy.pathHelper import getFileName

def downloadString(url, timeouts=(3.05, 27)):
    try:
        re = requests.get(url, timeouts)
        return re.content
    except:
        return


def downloadJson(url, timeouts=(3.05, 27)):
    try:
        re = requests.get(url, timeouts)
        info = json.loads(re.content)
        return info
    except:
        return


def getFileSize(url):
    if sys.version_info > (3, 0):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen
    try:
        response = urlopen(url)
        info = response.info()
        dic = dict(info)
        length = dic['Content-Length']
        return int(length)
    except:
        return -1


def downloadFileByUrls(urlArray, fileName, stimeout=None, showprogress=False):
    if os.access(fileName, 0):
        os.remove(fileName)
    progress = None
    if showprogress:
        desc = getFileName(fileName)
        progress = ProgressTool((len(urlArray)), 10, unit='', desc=desc)
    curcount = 1
    for item in urlArray:
        ret = downloadFile(item, fileName, stimeout, False, append=True)
        if ret != True:
            return False
            if progress:
                progress.setCurCount(curcount)
                curcount += 1

    return True


def downloadFile(url, fileName, stimeout=None, showprogress=False, append=False):
    if sys.version_info > (3, 0):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen
    try:
        if stimeout is None:
            response = urlopen(url)
        else:
            response = urlopen(url, timeout=stimeout)
        unit = 'mb'
        if convertStorageUnit(response.length, 'byte', unit) < 1:
            unit = 'kb'
        progress = None
        if showprogress:
            desc = getFileName(fileName)
            progress = ProgressTool((convertStorageUnit(response.length, 'byte', unit)), 10, unit=unit, desc=desc)
        mode = 'wb'
        if append:
            mode = 'ab'
        curcount = 0
        chunksize = 16384
        with open(fileName, mode) as (f):
            while True:
                chunk = response.read(chunksize)
                curcount += len(chunk)
                if progress:
                    progress.setCurCount(convertStorageUnit(curcount, 'byte', unit))
                if not chunk:
                    break
                f.write(chunk)

            return True
    except:
        return False


def getIpStatus(host, port, timeouts=1):
    socket.setdefaulttimeout(timeouts)
    flag = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
    except:
        flag = False

    return flag


def getIP():
    text = requests.get('http://txt.go.sohu.com/ip/soip').text
    ip = re.findall('\\d+.\\d+.\\d+.\\d+', text)[0]
    return ip


def getResult(code=0, msg='', data=''):
    ret = {}
    ret['code'] = code
    ret['errmsg'] = msg
    ret['data'] = data
    return json.dumps(ret)