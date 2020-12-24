# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/LabelPlainExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label

class LabelPlainExample(VerticalLayout):

    def __init__(self):
        super(LabelPlainExample, self).__init__()
        self.setSpacing(True)
        plainText = Label('This is an example of a Label component. The content mode of this label is set to CONTENT_TEXT. This means that it will display the content text as is. HTML and XML special characters (<,>,&) are escaped properly to allow displaying them.')
        plainText.setContentMode(Label.CONTENT_TEXT)
        self.addComponent(plainText)