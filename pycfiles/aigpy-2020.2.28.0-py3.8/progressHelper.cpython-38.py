# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\progressHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 2370 bytes
"""
@File    :   progressHelper.py
@Time    :   2018/12/28
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Show ProgressBar
"""
import sys, time, threading

class ProgressTool(object):

    def __init__(self, maxCount, barLength=50, icon='▓', unit='', desc=''):
        self.curCount = 0
        self.maxCount = maxCount
        self.barLength = barLength
        self.icon = icon
        self.mutex = threading.Lock()
        self.end = 0
        self.unit = unit
        self.desc = ''
        if len(desc) > 0:
            self.desc = '(' + desc + ')'

    def reset(self, maxCount):
        if self.mutex.acquire():
            self.curCount = 0
            self.maxCount = maxCount
            self.end = 0
            self.mutex.release()

    def setCurCount(self, curCount):
        if self.mutex.acquire():
            if self.end == 0:
                if curCount >= self.maxCount:
                    curCount = self.maxCount
                    self.end = 1
                self.curCount = curCount
                self._show()
            self.mutex.release()

    def step(self):
        if self.mutex.acquire():
            if self.end == 0 and self.curCount < self.maxCount:
                self.curCount += 1
                self._show()
            else:
                self.end = 1
            self.mutex.release()

    def _show(self):
        numBlock = int(self.curCount * self.barLength / self.maxCount)
        numEmpty = self.barLength - numBlock
        percent = self.curCount * 100.0 / self.maxCount
        process = '%3d' % percent + '%|' + self.icon * numBlock + ' ' * numEmpty + '| ' + str(round(self.curCount, 2)) + '/' + str(round(self.maxCount, 2)) + ' ' + self.unit + self.desc
        if self.curCount < self.maxCount:
            process += '\r'
        else:
            process += '\n'
        sys.stdout.write(process)
        sys.stdout.flush()