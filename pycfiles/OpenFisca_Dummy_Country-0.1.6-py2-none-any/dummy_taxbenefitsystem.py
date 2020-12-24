# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-dummy-country/openfisca_dummy_country/dummy_taxbenefitsystem.py
# Compiled at: 2017-03-31 07:03:44
import pkg_resources, os
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from entities import entities
from scenarios import Scenario
COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_model_dir = os.path.join(COUNTRY_DIR, 'model')
path_to_root_params = os.path.join(COUNTRY_DIR, 'parameters', 'param_root.xml')
path_to_crds_params = os.path.join(COUNTRY_DIR, 'parameters', 'param_more.xml')

class DummyTaxBenefitSystem(TaxBenefitSystem):

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        self.Scenario = Scenario
        self.add_legislation_params(path_to_root_params)
        self.add_legislation_params(path_to_crds_params, 'contribution_sociale')
        self.add_variables_from_directory(path_to_model_dir)