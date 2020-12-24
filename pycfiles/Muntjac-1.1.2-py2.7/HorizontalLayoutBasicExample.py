# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/HorizontalLayoutBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import HorizontalLayout, TextField, Label, Alignment

class HorizontalLayoutBasicExample(HorizontalLayout):

    def __init__(self):
        super(HorizontalLayoutBasicExample, self).__init__()
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)