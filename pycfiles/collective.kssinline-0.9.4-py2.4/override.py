# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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