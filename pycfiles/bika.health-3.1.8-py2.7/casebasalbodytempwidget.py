# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/widgets/casebasalbodytempwidget.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.ATExtensions.widget import RecordsWidget as ATRecordsWidget
from Products.Archetypes.Registry import registerWidget
import json

class CaseBasalBodyTempWidget(ATRecordsWidget):
    security = ClassSecurityInfo()
    _properties = ATRecordsWidget._properties.copy()
    _properties.update({'macro': 'bika_health_widgets/casebasalbodytempwidget', 
       'helper_js': ('bika_health_widgets/casebasalbodytempwidget.js', ), 
       'helper_css': ('bika_health_widgets/casebasalbodytempwidget.css', )})

    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=False):
        outvalues = []
        values = form.get(field.getName(), empty_marker)
        for value in values:
            outvalues.append({'Day1': value.get('Day1', ''), 'Day2': value.get('Day2', ''), 
               'Day3': value.get('Day3', '')})

        return (
         outvalues, {})

    def jsondumps(self, val):
        return json.dumps(val)

    def getBasalBodyTemperature(self):
        conditions = [
         {'Day1': '', 'Day2': '', 
            'Day3': ''}]
        field = self.aq_parent.Schema()['BasalBodyTemperature']
        value = field.get(self.aq_parent)
        return value and value or conditions


registerWidget(CaseBasalBodyTempWidget, title='CaseBasalBodyTempWidget', description='Basal body temperature')