# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/vaccinationcenter.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Archetypes.utils import DisplayList
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.health.config import PROJECTNAME
from bika.lims.content.organisation import Organisation
from bika.health.interfaces import IVaccinationCenter
from zope.interface import implements
schema = Organisation.schema.copy() + ManagedSchema((
 TextField('Remarks', searchable=True, default_content_type='text/x-web-intelligent', allowable_content_types=('text/x-web-intelligent', ), default_output_type='text/html', widget=TextAreaWidget(macro='bika_widgets/remarks', label=_('Remarks'), append_only=True)),))

class VaccinationCenter(Organisation):
    implements(IVaccinationCenter)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


registerType(VaccinationCenter, PROJECTNAME)