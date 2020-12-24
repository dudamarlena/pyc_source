# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/views/city.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 786 bytes
from dal import autocomplete
from ..models import City

class CityAutocompleteView(autocomplete.Select2QuerySetView):
    __doc__ = '\n    City Autocomplete view.\n    '

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()
        qs = City.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)
        division = self.forwarded.get('division', None)
        if division:
            qs = qs.filter(division=division)
        subdivision = self.forwarded.get('subdivision', None)
        if division:
            qs = qs.filter(subdivision=subdivision)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs