# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/mime_types.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.application import Application
from muntjac.ui.embedded import Embedded
from muntjac.terminal.class_resource import ClassResource

class TestMimeTypes(TestCase):

    def testEmbeddedPDF(self):

        class app(Application):

            def init(self):
                pass

        e = Embedded('A pdf', ClassResource('file.pddf', app()))
        self.assertEquals('application/octet-stream', e.getMimeType(), 'Invalid mimetype')
        e = Embedded('A pdf', ClassResource('file.pdf', app()))
        self.assertEquals('application/pdf', e.getMimeType(), 'Invalid mimetype')