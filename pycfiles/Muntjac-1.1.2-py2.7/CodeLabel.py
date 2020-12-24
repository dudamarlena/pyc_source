# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/CodeLabel.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.api import Label

class CodeLabel(Label):
    CLIENT_WIDGET = None

    def __init__(self, content=None):
        if content is None:
            self.setContentMode(self.CONTENT_PREFORMATTED)
            super(CodeLabel, self).__init__()
        else:
            super(CodeLabel, self).__init__(content, self.CONTENT_PREFORMATTED)
        return

    def setContentMode(self, contentMode):
        if contentMode != self.CONTENT_PREFORMATTED:
            raise NotImplementedError, 'Only preformatted content supported'
        super(CodeLabel, self).setContentMode(self.CONTENT_PREFORMATTED)