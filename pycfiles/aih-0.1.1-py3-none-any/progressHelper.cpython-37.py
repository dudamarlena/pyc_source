# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\progressHelper.py
# Compiled at: 2019-08-30 12:41:18
# Size of source mod 2**32: 2445 bytes
__doc__ = '\n@File    :   progressHelper.py\n@Time    :   2018/12/28\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   Show ProgressBar\n'
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