# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/override.py
# Compiled at: 2008-10-02 13:12:27
from archetypes.kss.fields import ATFieldDecoratorView
from archetypes.kss.commands.validation import ValidationCommands
from Acquisition import aq_inner
import base64

class KssInlineATFieldDecoratorView(ATFieldDecoratorView):
    __module__ = __name__

    def getKssClasses(self, fieldname, templateId=None, macro=None, target=None):
        result = ATFieldDecoratorView.getKssClasses(self, fieldname, templateId, macro, target)
        if result:
            context = aq_inner(self.context)
            if context.isTemporary():
                attr = ' kssattr-atuid-%s' % base64.b64encode(('/').join(context.getPhysicalPath()))
                result = result + attr
            else:
                result = result + ' ' + self.getKssUIDClass()
        return result