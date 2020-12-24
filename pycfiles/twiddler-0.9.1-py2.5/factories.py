# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/factories.py
# Compiled at: 2008-07-24 14:48:01
from twiddler.zope2.interfaces import *
from twiddler.input.default import Default as DefaultInput
from twiddler.input.plaintext import PlainText
from twiddler.output.default import Default as DefaultOutput
from twiddler.zope2.executor.traverse import Traverse
from zope.interface import directlyProvides

class Factory:

    def __init__(self, obj):
        self.obj = obj

    def __call__(self):
        if IConfigurableComponent.implementedBy(self.obj):
            return self.obj()
        return self.obj


input_default = Factory(DefaultInput)
directlyProvides(input_default, IInputFactory)
input_plaintext = Factory(PlainText)
directlyProvides(input_plaintext, IInputFactory)
output_default = Factory(DefaultOutput)
directlyProvides(output_default, IOutputFactory)
no_executor = Factory(None)
directlyProvides(no_executor, IExecutorFactory)
traverse_executor = Factory(Traverse)
directlyProvides(traverse_executor, IExecutorFactory)