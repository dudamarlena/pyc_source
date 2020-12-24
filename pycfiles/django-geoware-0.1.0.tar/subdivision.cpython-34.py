# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/views/subdivision.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 566 bytes
from dal import autocomplete
from ..models import Subdivision

class SubdivisionAutocompleteView(autocomplete.Select2QuerySetView):
    __doc__ = '\n    Subdivision Autocomplete view.\n    '

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Subdivision.objects.none()
        qs = Subdivision.objects.all()
        division = self.forwarded.get('division', None)
        if division:
            qs = qs.filter(division=division)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs