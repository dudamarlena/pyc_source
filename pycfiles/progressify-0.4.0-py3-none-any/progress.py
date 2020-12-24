# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ProgressedHttp/progress.py
# Compiled at: 2017-10-08 03:38:16
__doc__ = '\n    Progress Bar decorator for classes\n'
from __future__ import absolute_import, division, print_function
import sys, math, functools
from subprocess import check_output
from itertools import cycle
from time import time
from ProgressedHttp.utils import str_len, unit_change
__all__ = [
 'bar']

def bar(width=0, fill='#'):
    u"""
    进度条处理
    :param width: 手动设置进度条宽度
    :param fill: 进度填充字符
    """

    def function_wrapper(func):

        @functools.wraps(func)
        def arguments(self, *args, **kwargs):
            if not hasattr(self, 'progressed') or not hasattr(self, 'total'):
                print('progressed, total attribute is needed!')
                return
            else:
                progress_cursor = 1
                last_update = time()
                while self.progressed <= self.total:
                    func(self, *args, **kwargs)
                    if not hasattr(self, 'disable_progress') or not self.disable_progress:
                        if self.total <= 0:
                            print('Total Length Invalid !')
                            self.progressed = self.total = 1
                            break
                        if not width:
                            try:
                                w = int(check_output('stty size', stderr=None, shell=True).split(' ')[1])
                            except:
                                w = 50

                        else:
                            w = width
                        if time() - last_update > 0.1:
                            if not hasattr(self, 'chunked') or not self.chunked:
                                percent = self.progressed / float(self.total)
                                percent_show = ('{}%').format(int(percent * 100))
                                title = getattr(self, 'title', '')
                                mark_width = w - len(percent_show) - str_len(title) - 7
                                mark_count = int(math.floor(mark_width * percent))
                                sys.stdout.write(' ' + title + ' ' + '[' + fill * mark_count + ' ' * (mark_width - mark_count) + ']  ' + percent_show + '\r')
                            else:
                                progress_cursor += 1
                                title = getattr(self, 'title', '')
                                chunk_recved = unit_change(self.chunk_recved)
                                mark_width = w - str_len(title) - len(chunk_recved) - 6
                                sys.stdout.write(' ' + title + ' ' + '[' + ('').join([ i for _, i in zip(range(mark_width), cycle(['>> ', ' >>', '> >'][(progress_cursor % 3)])) ]) + ('] {}\r').format(chunk_recved))
                            sys.stdout.flush()
                            last_update = time()
                        if self.progressed == self.total:
                            sys.stdout.write(' ' * w + '\r')
                            break
                    elif self.progressed == self.total:
                        break

                return

        return arguments

    return function_wrapper