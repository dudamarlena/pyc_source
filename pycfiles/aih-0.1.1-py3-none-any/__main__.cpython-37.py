# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\__main__.py
# Compiled at: 2019-08-30 12:41:18
# Size of source mod 2**32: 1030 bytes
from colorama import init
import socks, requests, sys, os, time
sys.path.append('./')
import aigpy.zipHelper as zipHelper
import aigpy.netHelper as netHelper
from aigpy.updateHelper import updateTool
import aigpy.ffmpegHelper as ffmpegHelper
from aigpy.serverHelper import ServerTool
if __name__ == '__main__':
    os.system('pip install aigpy --upgrade')
    bo = netHelper.downloadFile('http://down.2zzt.com/uploads/cu/cu2.3.zip', 'e:\\1.zip', showprogress=True)
    init(autoreset=True)
    print('\x1b[0;30;40m\tHello World\x1b[0m')
    print('\x1b[0;31;40m\tHello World\x1b[0m')
    print('\x1b[0;32;40m\tHello World\x1b[0m')
    print('\x1b[0;33;40m\tHello World\x1b[0m')
    print('\x1b[0;34;40m\tHello World\x1b[0m')
    print('\x1b[0;35;40m\tHello World\x1b[0m')
    print('\x1b[0;36;40m\tHello World\x1b[0m')
    print('\x1b[0;37;40m\tHello World\x1b[0m')