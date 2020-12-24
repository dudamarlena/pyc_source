# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/embedded/ImageEmbedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout
from muntjac.ui.embedded import Embedded
from muntjac.terminal.theme_resource import ThemeResource

class ImageEmbedExample(VerticalLayout):

    def __init__(self):
        super(ImageEmbedExample, self).__init__()
        e = Embedded('Image from a theme resource', ThemeResource('../runo/icons/64/document.png'))
        self.addComponent(e)