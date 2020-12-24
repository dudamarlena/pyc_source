# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/mixins.py
# Compiled at: 2015-09-15 01:59:29
from collections import defaultdict
from .utils import get_experiment_variant

class VariantTestMixin(object):
    experiments = []

    def __init__(self, *args, **kwargs):
        super(VariantTestMixin, self).__init__(*args, **kwargs)
        self.variants = defaultdict(lambda : None)

    def dispatch(self, request, *args, **kwargs):
        self.set_variants()
        return super(VariantTestMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['variants'] = self.variants
        return super(VariantTestMixin, self).get_context_data(**kwargs)

    def set_variants(self):
        for exp in self.experiments:
            variant = get_experiment_variant(self.request, exp)
            if variant:
                self.variants[exp] = variant