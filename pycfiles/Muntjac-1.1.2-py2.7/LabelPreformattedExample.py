# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/LabelPreformattedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label

class LabelPreformattedExample(VerticalLayout):

    def __init__(self):
        super(LabelPreformattedExample, self).__init__()
        self.setSpacing(True)
        preformattedText = Label('This is an example of a Label component.\n\nThe content mode of this label is set\nto CONTENT_PREFORMATTED. This means\nthat it will display the content text\nusing a fixed-width font. You also have\nto insert the line breaks yourself.\n\n\tHTML and XML special characters\n\t(<,>,&) are escaped properly to\n\tallow displaying them.')
        preformattedText.setContentMode(Label.CONTENT_PREFORMATTED)
        self.addComponent(preformattedText)