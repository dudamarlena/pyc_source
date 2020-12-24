# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-dummy-country/openfisca_dummy_country/dummy_reform.py
# Compiled at: 2017-04-13 13:15:10
from openfisca_core.model_api import *

class neutralization_rsa(Reform):

    def apply(self):
        self.neutralize_column('rsa')