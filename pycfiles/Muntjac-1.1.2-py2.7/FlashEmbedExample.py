# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/embedded/FlashEmbedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Embedded
from muntjac.terminal.external_resource import ExternalResource

class FlashEmbedExample(VerticalLayout):

    def __init__(self):
        super(FlashEmbedExample, self).__init__()
        e = Embedded(None, ExternalResource('http://www.youtube.com/v/Qy67XU6xEi8&hl=en_US&fs=1&'))
        e.setMimeType('application/x-shockwave-flash')
        e.setParameter('allowFullScreen', 'true')
        e.setWidth('320px')
        e.setHeight('265px')
        self.addComponent(e)
        return