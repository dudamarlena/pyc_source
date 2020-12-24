# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/views/altname.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 574 bytes
from dal import autocomplete
from ..models import Altname

class AltnameAutocompleteView(autocomplete.Select2QuerySetView):
    __doc__ = '\n    Altname Autocomplete view.\n    '

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Altname.objects.none()
        qs = Altname.objects.all()
        ref_geoname_id = self.forwarded.get('geoname_id', None)
        if ref_geoname_id:
            qs = qs.filter(ref_geoname_id=ref_geoname_id)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs