# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/views/division.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 546 bytes
from dal import autocomplete
from ..models import Division

class DivisionAutocompleteView(autocomplete.Select2QuerySetView):
    __doc__ = '\n    Division Autocomplete view.\n    '

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Division.objects.none()
        qs = Division.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs