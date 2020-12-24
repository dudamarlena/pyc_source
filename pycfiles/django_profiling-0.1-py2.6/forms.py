# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/dprofiling/forms.py
# Compiled at: 2013-05-14 16:54:48
from django import forms
from django.core.exceptions import ValidationError
_VALID_SORTS = ('calls', 'cumulative', 'cumtime', 'file', 'filename', 'module', 'ncalls',
                'pcalls', 'line', 'name', 'nfl', 'stdname', 'time', 'totime')

def validate_sort(value):
    if not value:
        return
    fields = value.split()
    for field in fields:
        if field not in _VALID_SORTS:
            raise ValidationError('%s is not a valid sort, must be one of: %s' % (
             field, (', ').join(_VALID_SORTS)))


class StatsForm(forms.Form):
    sort = forms.CharField(required=False, label='Stat Sorting', help_text='Enter sort fields space separated in the order they should be applied as per http://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats (i.e. calls cumulative file ncalls)', validators=[
     validate_sort])
    reverse_sort = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    strip_dirs = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    restrictions = forms.CharField(required=False, label='Output Restrictions', help_text='Enter output restrictions, one per line in the order they should be applied as per http://docs.python.org/2/library/profile.html#pstats.Stats.print_stats', widget=forms.Textarea)
    method = forms.ChoiceField(required=True, choices=(
     ('stats', 'Stats'),
     ('callers', 'Callers'),
     ('callees', 'Callees')))

    def clean_sort(self):
        if self.cleaned_data['sort']:
            return self.cleaned_data['sort'].split()
        else:
            return

    def clean_restrictions(self):
        if self.cleaned_data['restrictions']:
            values = [ r.strip() for r in self.cleaned_data['restrictions'].splitlines() if r ]
            output = []
            for value in values:
                try:
                    output.append(int(value))
                    continue
                except:
                    pass

                try:
                    output.append(float(value))
                    continue
                except:
                    pass

                output.append(value)

            return output
        return []