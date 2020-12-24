# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/forms.py
# Compiled at: 2015-04-21 15:30:03
from django import forms
from django.contrib.gis.geos import fromstr
from atlas.models import Country, Region, City
from atlas.fields import LonLatWidget, CoordinateFormField
from atlas.utils import get_city

class SelectLocationForm(forms.Form):
    location = CoordinateFormField(required=True, help_text='Select your location on the map')
    origin = forms.CharField(widget=forms.HiddenInput)
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SelectLocationForm, self).__init__(*args, **kwargs)
        self.fields['origin'].initial = self.request.GET.get('view', '/')
        if 'location' in self.request.session:
            location = self.request.session['location']
            self.fields['location'].initial = location['position'] if 'position' in location else location['city'].coordinates
        return

    def save(self):
        position = fromstr(self.cleaned_data['location'], srid=4326)
        city = get_city(position=position)
        self.request.session['location'] = {'city': city, 'position': position}

    def as_div(self):
        return self._html_output(normal_row='<div class="field"><div %(html_class_attr)s>%(label)s %(errors)s <div class="helptext">%(help_text)s</div> %(field)s</div></div>', error_row='%s', row_ender='</div>', help_text_html='%s', errors_on_separate_row=False)