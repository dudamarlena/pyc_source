# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/VerticalLayoutBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import TextField, VerticalLayout

class VerticalLayoutBasicExample(VerticalLayout):

    def __init__(self):
        super(VerticalLayoutBasicExample, self).__init__()
        for i in range(5):
            tf = TextField('Row %d' % (i + 1))
            tf.setWidth('300px')
            self.addComponent(tf)