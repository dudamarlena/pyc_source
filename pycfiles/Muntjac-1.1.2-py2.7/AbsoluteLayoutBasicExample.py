# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/AbsoluteLayoutBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import AbsoluteLayout, Button

class AbsoluteLayoutBasicExample(AbsoluteLayout):

    def __init__(self):
        super(AbsoluteLayoutBasicExample, self).__init__()
        self.setMargin(True)
        self.addStyleName('border')
        self.setWidth('99%')
        self.setHeight('300px')
        self.addComponent(Button('Top: 10px, left: 10px'), 'top:10px; left:10px')
        self.addComponent(Button('Top: 10px, right: 40px'), 'top:10px; right:40px')
        self.addComponent(Button('Bottom: 0, left: 50%'), 'bottom:0; left:50%')
        self.addComponent(Button('Top: 50%, right: 50%'), 'top:50%; right:50%')
        self.addComponent(Button('Top: 50%, right: 50%'), 'top:50%; right:50%')