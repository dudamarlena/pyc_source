# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/validator.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 1689 bytes
"""
Validating DFBA files against the guidelines & rules.

It is necessary to define all the rules for the FBA model.
"""
from sbmlutils.dfba.model import DFBAModel
version = '0.2-draft'

def validate_dfba(sbml_path):
    """ Validate given DFBA model against specification
    
    :param sbml_path: path to top model.
    :return: 
    """
    validator = DFBAValidator.from_sbmlpath(sbml_path=sbml_path)
    return validator.validate()


class DFBAValidator(object):
    __doc__ = ' Simulator class to dynamic flux balance models (DFBA). '

    def __init__(self, dfba_model):
        """ Create validator with the top level SBML file.

        :param top_level_path: absolute path of top level SBML file
        :param output_directory: directory where output files are written
        """
        self.dfba_model = dfba_model

    @staticmethod
    def from_sbmlpath(sbml_path):
        """ Create validator with the top level SBML file.
        
        :param sbml_path: path to top model file. 
        :return: 
        """
        dfba_model = DFBAModel(sbml_path)
        return DFBAValidator(dfba_model)

    def validate(self):
        print('--------------------------------------------------------------------------------')
        print('VALIDATION:')
        print('--------------------------------------------------------------------------------')
        print(self.dfba_model)


RuleTypes = {}

class Rule(object):
    __doc__ = ' Rule which is checkted\n    \n    '

    def __init__(self, rid, description, f=None):
        self.rid = rid
        self.description = description
        self.f = f

    def __str__(self):
        return '[{}] {}'.format(self.rid, self.description)


if __name__ == '__main__':
    r1 = Rule('DFBA-R0001', 'The DFBA model **MUST** be a single SBML `comp` model.')
    print(r1)