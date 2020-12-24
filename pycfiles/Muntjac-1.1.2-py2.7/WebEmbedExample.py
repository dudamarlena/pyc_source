# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/embedded/WebEmbedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Embedded
from muntjac.terminal.external_resource import ExternalResource

class WebEmbedExample(VerticalLayout):

    def __init__(self):
        super(WebEmbedExample, self).__init__()
        e = Embedded('Google Search', ExternalResource('http://www.google.com'))
        e.setType(Embedded.TYPE_BROWSER)
        e.setWidth('100%')
        e.setHeight('400px')
        self.addComponent(e)