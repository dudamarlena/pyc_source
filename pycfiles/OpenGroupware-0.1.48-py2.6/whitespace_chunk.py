# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/whitespace_chunk.py
# Compiled at: 2012-10-12 07:02:39
import string
from StringIO import StringIO
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class WhitespaceChunkAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'whitespace-chunk'
    __aliases__ = ['whitespaceChunk', 'whitespaceChunkAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'text/plain'

    def do_action(self):
        data = self.rfile.read()
        for record in data.split(' '):
            if record:
                self.wfile.write(('{0}\n').format(record))

    def parse_action_parameters(self):
        pass