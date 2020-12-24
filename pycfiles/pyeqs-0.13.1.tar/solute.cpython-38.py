# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/solute.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 7096 bytes
__doc__ = '\npyEQL Solute class\n\nThis file contains functions and methods for managing properties of \nindividual solutes. The Solute class contains methods for accessing\nONLY those properties that DO NOT depend on solution composition.\nSolute properties such as activity coefficient or concentration\nthat do depend on compsition are accessed via Solution class methods.\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
from pyEQL import unit
import logging
from pyEQL.logging_system import Unique
from pyEQL import paramsDB as db
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Solute:
    """Solute"""

    def __init__(self, formula, amount, volume, solvent_mass, parameters={}):
        """
        Parameters
        ----------
        formula : str
                    Chemical formula for the solute. 
                    Charged species must contain a + or - and (for polyvalent solutes) a number representing the net
                    charge (e.g. 'SO4-2').
        amount : str
                    The amount of substance in the specified unit system. The string should contain both a quantity and
                    a pint-compatible representation of a unit. e.g. '5 mol/kg' or '0.1 g/L'
        volume : pint Quantity
                    The volume of the solution
        solvent_mass : pint Quantity
                    The mass of solvent in the parent solution.
        parameters : dictionary, optional
                    Dictionary of custom parameters, such as diffusion coefficients, transport numbers, etc. Specify 
                    parameters as key:value pairs separated by commas within curly braces, e.g. 
                    {diffusion_coeff:5e-10,transport_number:0.8}. The 'key' is the name that will be used to access 
                    the parameter, the value is its value.
        """
        import pyEQL.chemical_formula as chem
        if not chem.is_valid_formula:
            logger.error('Invalid chemical formula specified.')
            return
        self.formula = formula
        self.mw = chem.get_molecular_weight(formula) * unit('g/mol')
        self.charge = chem.get_formal_charge(formula)
        quantity = unit(amount)
        self.moles = quantity.to('moles',
          'chem', mw=(self.mw), volume=volume, solvent_mass=solvent_mass)
        db.search_parameters(self.formula)

    def get_parameter(self, parameter, temperature=None, pressure=None, ionic_strength=None):
        """
        Return the value of the parameter named 'parameter'
        
        """
        param = db.get_parameter(self.formula, parameter)
        return param.get_value(temperature, pressure, ionic_strength)

    def add_parameter(self, name, magnitude, units='', **kwargs):
        """
        Add a parameter to the parameters database for a solute
        
        See pyEQL.parameters documentation for a description of the arguments
        
        """
        import pyEQL.parameter as pm
        newparam = (pm.Parameter)(name, magnitude, units, **kwargs)
        db.add_parameter(self.get_name(), newparam)

    def get_name(self):
        """
        Return the name (formula) of the solute
        
        Parameters
        ----------
        None
        
        Returns
        -------
        str
            The chemical formula of the solute
            
        """
        return self.formula

    def get_formal_charge(self):
        """
        Return the formal charge of the solute
        
        Parameters
        ----------
        None
        
        Returns
        -------
        int
            The formal charge of the solute
            
        """
        return self.charge

    def get_molecular_weight(self):
        """
        Return the molecular weight of the solute
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Quantity
            The molecular weight of the solute, in g/mol
        """
        return self.mw

    def get_moles(self):
        """
        Return the moles of solute in the solution
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Quantity
            The number of moles of solute
            
        """
        return self.moles

    def add_moles(self, amount, volume, solvent_mass):
        """
        Increase or decrease the amount of a substance present in the solution
        
        Parameters
        ----------
        amount: str quantity
                Amount of substance to add. Must be in mass or substance units.
                Negative values indicate subtraction of material.
        
        """
        quantity = unit(amount)
        self.moles += quantity.to('moles',
          'chem', mw=(self.mw), volume=volume, solvent_mass=solvent_mass)

    def set_moles(self, amount, volume, solvent_mass):
        """
        Set the amount of a substance present in the solution
        
        Parameters
        ----------
        amount: str quantity
                Desired amount of substance. Must be greater than or equal to 
                zero and given in mass or substance units.
        
        """
        quantity = unit(amount)
        self.moles = quantity.to('moles',
          'chem', mw=(self.mw), volume=volume, solvent_mass=solvent_mass)

    def __str__(self):
        return 'Species ' + str(self.get_name()) + ' MW=' + str(self.get_molecular_weight()) + ' Formal Charge=' + str(self.get_formal_charge()) + ' Amount= ' + str(self.get_moles())