# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/extension/gps/browser.py
# Compiled at: 2012-06-04 05:00:32
from ztfy.thesaurus.extension.gps.interfaces import IThesaurusTermGPSExtensionInfo
from z3c.form import field
from ztfy.skin.form import DialogEditForm
from ztfy.thesaurus import _

class ThesaurusTermGPSEditDialog(DialogEditForm):
    """Thesaurus term GPS extension info edit form"""

    @property
    def title(self):
        return self.getContent().label

    legend = _('Update GPS coordinates')
    fields = field.Fields(IThesaurusTermGPSExtensionInfo)