# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/widgets/splitteddatewidget.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.CMFPlone.i18nl10n import ulocalized_time
import json

class SplittedDateWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({'ulocalized_time': ulocalized_time, 
       'macro': 'bika_health_widgets/splitteddatewidget', 
       'helper_js': ('bika_health_widgets/splitteddatewidget.js', ), 
       'helper_css': ('bika_health_widgets/splitteddatewidget.css', ), 
       'changeYear': True, 
       'changeMonth': True, 
       'changeDay': True, 
       'maxDate': '+0d', 
       'yearRange': '-100:+0'})
    security = ClassSecurityInfo()

    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=False):
        outvalues = [
         {'year': form.get('PatientAgeAtCaseOnsetDate_year', empty_marker), 'month': form.get('PatientAgeAtCaseOnsetDate_month', empty_marker), 
            'day': form.get('PatientAgeAtCaseOnsetDate_day', empty_marker)}]
        return (outvalues, {})

    def jsondumps(self, val):
        return json.dumps(val)


registerWidget(SplittedDateWidget, title='SplittedDateWidget', description='Simple control with three input fields (year, month, day)')