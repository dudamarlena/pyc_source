# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/datapunt_api/renderers.py
from rest_framework_csv.renderers import CSVRenderer

class PaginatedCSVRenderer(CSVRenderer):
    results_field = 'results'

    def render(self, data, *args, **kwargs):
        print(len(data))
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return (super(PaginatedCSVRenderer, self).render)(data, *args, **kwargs)