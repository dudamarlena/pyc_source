# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/codelens/htmlFrame.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 803 bytes
from .pg_logger import setHTML
dft_template = '\n<html><body>\n<h3>%(banner)s</h3>\n<div>%(item1)s</div>\n<div>%(item2)s</div>\n<div>%(item3)s</div>\n</html></body>\n'

class HtmlFrame:

    def __init__(self, template=dft_template, banner=''):
        self.outputOn = True
        self.template = template
        self.banner = banner
        self.item1 = self.item2 = self.item3 = ''

    def makeEofPage(self):
        pass

    def makeFrame(self, template=None):
        if not template:
            template = self.template
        content = template % self.__dict__
        setHTML(content)