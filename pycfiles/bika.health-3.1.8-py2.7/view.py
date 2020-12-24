# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/sample/view.py
# Compiled at: 2014-12-12 07:13:54
from bika.health.browser.sample.edit import SampleEditView

class SampleView(SampleEditView):
    """ Overrides bika.lims.browser.sample.SampleView (through SampleEdit)
        Shows additional information inside the table_header about the Patient
        if exists in the attached Analysis Request
    """

    def __call__(self):
        self.allow_edit = False
        return super(SampleView, self).__call__()