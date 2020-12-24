# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/mfenced.py
# Compiled at: 2003-10-15 17:50:00
from element import *
import mrow
from mtoken import MOperator
import re
_whitespace_rx = re.compile('\\s+')

class MFenced(mrow.MRow):

    def __init__(self, plotter, children):
        self.__children = children
        super(MFenced, self).__init__(plotter, [])

    def __addChildren(self, children):
        open = MOperator(self.plotter, self.getAttribute('open', recursive=False, default='(').str)
        close = MOperator(self.plotter, self.getAttribute('close', recursive=False, default=')').str)
        open.setAttribute('fence', True)
        close.setAttribute('fence', True)
        separators = self.getAttribute('separators', recursive=False, default=',').str
        inner_row = []
        for (i, child) in enumerate(children):
            inner_row.append(child)
            if i < len(children) - 1:
                try:
                    sep = separators[i]
                except IndexError:
                    sep = separators[(-1)]
                else:
                    sep = MOperator(self.plotter, sep)
                    sep.setAttribute('separator', True)
                    inner_row.append(sep)

        if len(inner_row) == 0:
            new_children = [
             open, close]
        elif len(inner_row) == 1:
            new_children = [
             open, inner_row[0], close]
        else:
            new_children = [
             open, mrow.MRow(self.plotter, inner_row), close]
        for child in new_children:
            self.addChild(child)

    def update(self):
        try:
            children = self.__children
        except AttributeError:
            children = None

        if children is not None:
            self.__addChildren(children)
            del self.__children
        super(MFenced, self).update()
        return


xml_mapping['mfenced'] = MFenced