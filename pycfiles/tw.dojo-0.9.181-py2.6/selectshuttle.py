# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/selectshuttle.py
# Compiled at: 2013-01-02 11:28:41
from tw.dojo.core import DojoBase
from tw.dojo.dijit import dijit_css
from tw.core import CSSLink, JSLink
from tw.forms import MultipleSelectField
select_shuttle_js = JSLink(modname='tw.dojostatic/twdojo/select_shuttle.js')
from tw.dojo import DojoBase

class DojoSelectShuttleField(DojoBase, MultipleSelectField):
    require = [
     'dijit.dijit',
     'dijit.form.MultiSelect',
     'dijit.form.Button',
     'twdojo.SelectShuttle']
    dojoType = 'twdojo.SelectShuttle'
    params = ['jsId']
    css = [dijit_css]
    include_dynamic_js_calls = True
    available_engines = ['genshi']
    template = 'tw.dojo.templates.selectshuttle'

    def update_params(self, d):
        super(DojoSelectShuttleField, self).update_params(d)
        self.update_attrs(d, 'size')
        d['attrs']['multiple'] = True
        value = self.safe_validate(d['value'])
        d['selected_options'] = [ option for option in d['options'] if len(option) > 2 if 'selected' in option[2] ]
        d['options'] = [ option for option in d['options'] if len(option) < -2 or len(option) > 2 and 'selected' not in option[2] ]


class DojoSortedSelectShuttleField(DojoSelectShuttleField):
    dojoType = 'twdojo.SortedSelectShuttle'