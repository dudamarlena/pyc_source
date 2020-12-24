# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/solution.py
# Compiled at: 2020-04-22 01:17:05
# Size of source mod 2**32: 94225 bytes
"""
pyEQL Solution Class

:copyright: 2013-2020 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""
import math
from pint import UndefinedUnitError
import pyEQL.activity_correction as ac
import pyEQL.water_properties as h2o
import pyEQL.solute as sol
import pyEQL.salt_ion_match as salt
from pyEQL import unit
from pyEQL import paramsDB as db
from pyEQL.logging_system import Unique
import logging
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Solution:
    __doc__ = "\n    Class representing the properties of a solution. Instances of this class\n    contain information about the solutes, solvent, and bulk properties.\n\n    Parameters\n    ----------\n    solutes : list of lists, optional\n                See add_solute() documentation for formatting of this list.\n                Defaults to empty (pure solvent) if omitted\n    volume : str, optional\n                Volume of the solvent, including the unit. Defaults to '1 L' if omitted.\n                Note that the total solution volume will be computed using partial molar\n                volumes of the respective solutes as they are added to the solution.\n    temperature : str, optional\n                The solution temperature, including the unit. Defaults to '25 degC' if omitted.\n    pressure : Quantity, optional\n                The ambient pressure of the solution, including the unit.\n                Defaults to '1 atm' if omitted.\n    pH : number, optional\n                Negative log of H+ activity. If omitted, the solution will be\n                initialized to pH 7 (neutral) with appropriate quantities of\n                H+ and OH- ions\n\n    Returns\n    -------\n    Solution\n        A Solution object.\n\n    Examples\n    --------\n    >>> s1 = pyEQL.Solution([['Na+','1 mol/L'],['Cl-','1 mol/L']],temperature='20 degC',volume='500 mL')\n    >>> print(s1)\n    Components:\n    ['H2O', 'Cl-', 'H+', 'OH-', 'Na+']\n    Volume: 0.5 l\n    Density: 1.0383030844030992 kg/l\n\n    See Also\n    --------\n    add_solute\n\n    "

    def __init__(self, solutes=[], **kwargs):
        if 'volume' in kwargs:
            volume_set = True
            self.volume = unit(kwargs['volume'])
        else:
            volume_set = False
            self.volume = unit('1 L')
        if 'temperature' in kwargs:
            self.temperature = unit(kwargs['temperature'])
        else:
            self.temperature = unit('25 degC')
        if 'pressure' in kwargs:
            self.pressure = unit(kwargs['pressure'])
        else:
            self.pressure = unit('1 atm')
        self.components = {}
        self.volume_update_required = False
        if 'solvent' in kwargs:
            self.solvent_name = kwargs['solvent'][0]
            if kwargs['solvent'][0] == 'H2O':
                if kwargs['solvent'][0] == 'water':
                    logger.error('Non-aqueous solvent detected. These are not yet supported!')
                if volume_set is True:
                    logger.error('Solvent volume and mass cannot both be specified. Calculating volume based on solvent mass.')
                self.add_solvent(self.solvent_name, kwargs['solvent'][1])
            else:
                self.solvent_name = 'H2O'
            self.add_solvent(self.solvent_name, str(self.volume * h2o.water_density(self.temperature)))
        elif 'pH' in kwargs:
            pH = kwargs['pH']
        else:
            pH = 7
        self.add_solute('H+', str(10 ** (-1 * pH)) + 'mol/L')
        self.add_solute('OH-', str(10 ** (-1 * (14 - pH))) + 'mol/L')
        for item in solutes:
            (self.add_solute)(*item)

    def add_solute(self, formula, amount, parameters={}):
        """
        Primary method for adding substances to a pyEQL solution

        Parameters
        ----------
        formula : str
                    Chemical formula for the solute.
                    Charged species must contain a + or - and (for polyvalent solutes) a number representing the net
                    charge (e.g. 'SO4-2').
        amount : str
                    The amount of substance in the specified unit system. The string should contain both a quantity and
                    a pint-compatible representation of a unit. e.g. '5 mol/kg' or '0.1 g/L'
        parameters : dictionary, optional
                    Dictionary of custom parameters, such as diffusion coefficients, transport numbers, etc. Specify
                    parameters as key:value pairs separated by commas within curly braces, e.g. {diffusion_coeff:5e-10,
                    transport_number:0.8}. The 'key' is the name that will be used to access the parameter, the value
                    is its value.

        """
        if unit(amount).dimensionality in ('[substance]/[length]**3', '[mass]/[length]**3'):
            orig_volume = self.get_volume()
            new_solute = sol.Solute(formula, amount, self.get_volume(), self.get_solvent_mass(), parameters)
            self.components.update({new_solute.get_name(): new_solute})
            solute_vol = self._get_solute_volume()
            target_vol = orig_volume - solute_vol
            target_mass = target_vol * h2o.water_density(self.get_temperature())
            mw = self.get_solvent().get_molecular_weight()
            target_mol = target_mass / mw
            self.get_solvent().moles = target_mol
        else:
            new_solute = sol.Solute(formula, amount, self.get_volume(), self.get_solvent_mass(), parameters)
            self.components.update({new_solute.get_name(): new_solute})
            if self.get_solvent_mass() <= unit('0 kg'):
                logger.error('All solvent has been depleted from the solution')
                return None
            self.volume_update_required = True

    def add_solvent(self, formula, amount):
        """
        Same as add_solute but omits the need to pass solvent mass to pint
        """
        new_solvent = sol.Solute(formula, amount, self.get_volume(), amount)
        self.components.update({new_solvent.get_name(): new_solvent})

    def get_solute(self, i):
        """
        Return the specified solute object.

        """
        return self.components[i]

    def get_solvent(self):
        """
        Return the solvent object.

        """
        return self.components[self.solvent_name]

    def get_temperature(self):
        """
        Return the temperature of the solution.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity: The temperature of the solution, in Kelvin.
        """
        return self.temperature.to('K')

    def set_temperature(self, temperature):
        """
        Set the solution temperature.

        Parameters
        ----------
        temperature : str
            String representing the temperature, e.g. '25 degC'
        """
        self.temperature = unit(temperature)
        self._update_volume()

    def get_pressure(self):
        """
        Return the hydrostatic pressure of the solution.

        Returns
        -------
        Quantity: The hydrostatic pressure of the solution, in atm.
        """
        return self.pressure.to('atm')

    def set_pressure(self, pressure):
        """
        Set the hydrostatic pressure of the solution.

        Parameters
        ----------
        pressure : str
            String representing the temperature, e.g. '25 degC'
        """
        self.pressure = unit(pressure)
        self._update_volume()

    def get_solvent_mass(self):
        """
        Return the mass of the solvent.

        This method is used whenever mol/kg (or similar) concentrations
        are requested by get_amount()

        Parameters
        ----------
        None

        Returns
        -------
        Quantity: the mass of the solvent, in kg

        See Also
        --------
        get_amount
        """
        solvent = self.get_solvent()
        mw = solvent.get_molecular_weight()
        return solvent.get_moles().to('kg', 'chem', mw=mw)

    def get_volume(self):
        """
        Return the volume of the solution.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity: the volume of the solution, in L
        """
        if self.volume_update_required is True:
            self._update_volume()
            self.volume_update_required = False
        return self.volume.to('L')

    def set_volume(self, volume):
        """Change the total solution volume to volume, while preserving
        all component concentrations

        Parameters
        ----------
        volume : str quantity
                Total volume of the solution, including the unit, e.g. '1 L'

        Examples
        ---------
        >>> mysol = Solution([['Na+','2 mol/L'],['Cl-','0.01 mol/L']],volume='500 mL')
        >>> print(mysol.get_volume())
        0.5000883925072983 l
        >>> mysol.list_concentrations()
        {'H2O': '55.508435061791985 mol/kg', 'Cl-': '0.00992937605907076 mol/kg', 'Na+': '2.0059345573880325 mol/kg'}
        >>> mysol.set_volume('200 mL')
        >>> print(mysol.get_volume())
        0.2 l
        >>> mysol.list_concentrations()
        {'H2O': '55.50843506179199 mol/kg', 'Cl-': '0.00992937605907076 mol/kg', 'Na+': '2.0059345573880325 mol/kg'}

        """
        scale_factor = unit(volume) / self.get_volume()
        for item in self.components:
            self.get_solute(item).moles = self.get_solute(item).moles * scale_factor
        else:
            self.volume = unit(volume)

    def get_mass(self):
        """
        Return the total mass of the solution.

        The mass is calculated each time this method is called.
        Parameters
        ----------
        None

        Returns
        -------
        Quantity: the mass of the solution, in kg

        """
        total_mass = 0
        for item in self.components:
            total_mass += self.get_amount(item, 'kg')
        else:
            return total_mass.to('kg')

    def get_density(self):
        """
        Return the density of the solution.

        Density is calculated from the mass and volume each time this method is called.

        Returns
        -------
        Quantity: The density of the solution.
        """
        return self.get_mass() / self.get_volume()

    def get_dielectric_constant--- This code section failed: ---

 L. 437         0  LOAD_GLOBAL              h2o
                2  LOAD_METHOD              water_dielectric_constant
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              get_temperature
                8  CALL_METHOD_0         0  ''
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'di_water'

 L. 439        14  LOAD_CONST               1
               16  STORE_FAST               'denominator'

 L. 440        18  LOAD_FAST                'self'
               20  LOAD_ATTR                components
               22  GET_ITER         
             24_0  COME_FROM            34  '34'
               24  FOR_ITER            122  'to 122'
               26  STORE_FAST               'item'

 L. 442        28  LOAD_FAST                'item'
               30  LOAD_STR                 'H2O'
               32  COMPARE_OP               !=
               34  POP_JUMP_IF_FALSE    24  'to 24'

 L. 444        36  SETUP_FINALLY        82  'to 82'

 L. 445        38  LOAD_FAST                'self'
               40  LOAD_METHOD              get_amount
               42  LOAD_FAST                'item'
               44  LOAD_STR                 'fraction'
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'fraction'

 L. 446        50  LOAD_FAST                'self'
               52  LOAD_METHOD              get_solute
               54  LOAD_FAST                'item'
               56  CALL_METHOD_1         1  ''
               58  LOAD_METHOD              get_parameter

 L. 447        60  LOAD_STR                 'dielectric_parameter_water'

 L. 446        62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'coefficient'

 L. 449        66  LOAD_FAST                'denominator'
               68  LOAD_FAST                'coefficient'
               70  LOAD_FAST                'fraction'
               72  BINARY_MULTIPLY  
               74  INPLACE_ADD      
               76  STORE_FAST               'denominator'
               78  POP_BLOCK        
               80  JUMP_BACK            24  'to 24'
             82_0  COME_FROM_FINALLY    36  '36'

 L. 450        82  DUP_TOP          
               84  LOAD_GLOBAL              TypeError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   118  'to 118'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 451        96  LOAD_GLOBAL              logger
               98  LOAD_METHOD              warning

 L. 452       100  LOAD_STR                 'No dielectric parameters found for species %s.'
              102  LOAD_FAST                'item'
              104  BINARY_MODULO    

 L. 451       106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 454       110  POP_EXCEPT       
              112  JUMP_BACK            24  'to 24'
              114  POP_EXCEPT       
              116  JUMP_BACK            24  'to 24'
            118_0  COME_FROM            88  '88'
              118  END_FINALLY      
              120  JUMP_BACK            24  'to 24'

 L. 456       122  LOAD_FAST                'di_water'
              124  LOAD_FAST                'denominator'
              126  BINARY_TRUE_DIVIDE
              128  STORE_FAST               'dielectric_constant'

 L. 458       130  LOAD_FAST                'dielectric_constant'
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 114

    def get_viscosity_relative(self):
        r"""
        Return the viscosity of the solution relative to that of water

        This is calculated using a simplified form of the Jones-Dole equation:

        .. math:: \eta_{rel} = 1 + \sum_i B_i m_i

        Where :math:`m` is the molal concentration and :math:`B` is an empirical parameter.

        See
        <http://downloads.olisystems.com/ResourceCD/TransportProperties/Viscosity-Aqueous.pdf>
        <http://www.nrcresearchpress.com/doi/pdf/10.1139/v77-148>
        <http://apple.csgi.unifi.it/~fratini/chen/pdf/14.pdf>
        """
        viscosity_rel = self.get_viscosity_dynamic() / h2o.water_viscosity_dynamic(self.get_temperature(), self.get_pressure())
        return viscosity_rel

    def get_viscosity_dynamic(self):
        """
        Return the dynamic (absolute) viscosity of the solution.

        Calculated from the kinematic viscosity

        See Also
        --------
        get_viscosity_kinematic
        get_viscosity_relative
        """
        return self.get_viscosity_kinematic() * self.get_density()

    def get_viscosity_kinematic(self):
        r"""
        Return the kinematic viscosity of the solution.

        Notes
        -----
        The calculation is based on a model derived from the Eyring equation
        and presented in [#]_

        .. math::

            \ln \nu = \ln {\nu_w MW_w \over \sum_i x_i MW_i } +
            15 x_+^2 + x_+^3  \delta G^*_{123} + 3 x_+ \delta G^*_{23} (1-0.05x_+)

        Where:

        .. math:: \delta G^*_{123} = a_o + a_1 (T)^{0.75}
        .. math:: \delta G^*_{23} = b_o + b_1 (T)^{0.5}

        In which :math: `\nu` is the kinematic viscosity, MW is the molecular weight,
        `x_+` is the mole fraction of cations, and T is the temperature in degrees C.

        The a and b fitting parameters for a variety of common salts are included in the
        database.

        References
        ----------
        .. [#] Vásquez-Castillo, G.; Iglesias-Silva, G. a.; Hall, K. R. An extension                of the McAllister model to correlate kinematic viscosity of electrolyte solutions.                Fluid Phase Equilib. 2013, 358, 44–49.

        See Also
        --------
        get_viscosity_dynamic
        get_viscosity_relative
        """
        salt = self.get_salt()
        cation = salt.cation
        db.search_parameters(salt.formula)
        a0 = a1 = b0 = b1 = 0
        if db.has_parameter(salt.formula, 'erying_viscosity_coefficients'):
            params = db.get_parameter(salt.formula, 'erying_viscosity_coefficients')
            a0 = params.get_value()[0]
            a1 = params.get_value()[1]
            b0 = params.get_value()[2]
            b1 = params.get_value()[3]
        else:
            logger.warning('Viscosity coefficients for %s not found. Viscosity will be approximate.' % salt.formula)
        temperature = self.get_temperature().to('degC')
        G_123 = a0 + a1 * temperature.magnitude ** 0.75
        G_23 = b0 + b1 * temperature.magnitude ** 0.5
        nu_w = h2o.water_viscosity_kinematic(temperature, self.get_pressure()).to('m**2 / s').magnitude
        MW = self.get_mass() / (self.get_moles_solvent() + self.get_total_moles_solute())
        MW_w = self.get_solvent().get_molecular_weight()
        x_cat = self.get_amount(cation, 'fraction')
        nu = math.log(nu_w * MW_w / MW) + 15 * x_cat ** 2 + x_cat ** 3 * G_123 + 3 * x_cat * G_23 * (1 - 0.05 * x_cat)
        return math.exp(nu) * unit('m**2 / s')

    def get_conductivity(self):
        r"""
        Compute the electrical conductivity of the solution.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
            The electrical conductivity of the solution in Siemens / meter.

        Notes
        -----
        Conductivity is calculated by summing the molar conductivities of the respective
        solutes, but they are activity-corrected and adjusted using an empricial exponent.
        This approach is used in PHREEQC and Aqion models [#]_ [#]_

        .. math::

            EC = {F^2 \over R T} \sum_i D_i z_i ^ 2 \gamma_i ^ {\alpha} m_i

        Where:

        .. math::

            \alpha = \begin{cases} {0.6 \over \sqrt{|z_i|}} & {I < 0.36|z_i|} \\ {\sqrt{I} \over |z_i|} &
            otherwise \end{cases}

        Note: PHREEQC uses the molal rather than molar concentration according to
        http://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/phreeqc3-html/phreeqc3-43.htm

        References
        ----------
        .. [#] http://www.aqion.de/site/77
        .. [#] http://www.hydrochemistry.eu/exmpls/sc.html

        See Also
        --------
        get_ionic_strength
        get_molar_conductivity
        get_activity_coefficient

        """
        EC = 0 * unit('S/m')
        temperature = self.get_temperature()
        for item in self.components:
            z = abs(self.get_solute(item).get_formal_charge())
            if not z == 0:
                if self.get_ionic_strength().magnitude < 0.36 * z:
                    alpha = 0.6 / z ** 0.5
                else:
                    alpha = self.get_ionic_strength().magnitude ** 0.5 / z
                diffusion_coefficient = self.get_property(item, 'diffusion_coefficient')
                molar_cond = diffusion_coefficient * (unit.e * unit.N_A) ** 2 * self.get_solute(item).get_formal_charge() ** 2 / (unit.R * temperature)
                EC += molar_cond * self.get_activity_coefficient(item) ** alpha * self.get_amount(item, 'mol/L')
            return EC.to('S/m')

    def get_osmotic_pressure(self):
        r"""
        Return the osmotic pressure of the solution relative to pure water.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
                The osmotic pressure of the solution relative to pure water in Pa

        See Also
        --------
        get_water_activity
        get_osmotic_coefficient
        get_salt

        Notes
        -----
        Osmotic pressure is calculated based on the water activity [#]_ [#]_ :

        .. math:: \Pi = {RT \over V_w} \ln a_w

        Where :math:`\Pi` is the osmotic pressure, :math:`V_w` is the partial
        molar volume of water (18.2 cm**3/mol), and :math:`a_w` is the water
        activity.

        References
        ----------
        .. [#] Sata, Toshikatsu. Ion Exchange Membranes: Preparation, Characterization, and Modification.                Royal Society of Chemistry, 2004, p. 10.

        .. [#] http://en.wikipedia.org/wiki/Osmotic_pressure#Derivation_of_osmotic_pressure

        Examples
        --------
        >>> s1=pyEQL.Solution()
        >>> s1.get_osmotic_pressure()
        0.0

        >>> s1 = pyEQL.Solution([['Na+','0.2 mol/kg'],['Cl-','0.2 mol/kg']])
        >>> soln.get_osmotic_pressure()
        <Quantity(906516.7318131207, 'pascal')>
        """
        partial_molar_volume_water = 1.82e-05 * unit('m ** 3/mol')
        osmotic_pressure = -1 * unit.R * self.get_temperature() / partial_molar_volume_water * math.log(self.get_water_activity())
        logger.info('Computed osmotic pressure of solution as %s Pa at T= %s degrees C' % (
         osmotic_pressure, self.get_temperature()))
        return osmotic_pressure.to('Pa')

    def p(self, solute, activity=True):
        """
        Return the negative log of the activity of solute.

        Generally used for expressing concentration of hydrogen ions (pH)

        Parameters
        ----------
        solute : str
            String representing the formula of the solute
        activity: bool, optional
            If False, the function will use the molar concentration rather
            than the activity to calculate p. Defaults to True.

        Returns
        -------
        Quantity
            The negative log10 of the activity (or molar concentration if
            activity = False) of the solute.

        Examples
        --------
        TODO

        """
        try:
            if activity is True:
                return -1 * math.log10(self.get_activity(solute))
            if activity is False:
                return -1 * math.log10(self.get_amount(solute, 'mol/L').magnitude)
        except ValueError:
            return 0

    def get_amount--- This code section failed: ---

 L. 815         0  SETUP_FINALLY        34  'to 34'

 L. 816         2  LOAD_FAST                'self'
                4  LOAD_METHOD              get_solute
                6  LOAD_FAST                'solute'
                8  CALL_METHOD_1         1  ''
               10  LOAD_METHOD              get_moles
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'moles'

 L. 817        16  LOAD_FAST                'self'
               18  LOAD_METHOD              get_solute
               20  LOAD_FAST                'solute'
               22  CALL_METHOD_1         1  ''
               24  LOAD_METHOD              get_molecular_weight
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'mw'
               30  POP_BLOCK        
               32  JUMP_FORWARD        108  'to 108'
             34_0  COME_FROM_FINALLY     0  '0'

 L. 820        34  DUP_TOP          
               36  LOAD_GLOBAL              KeyError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE   106  'to 106'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 821        48  SETUP_FINALLY        68  'to 68'

 L. 822        50  LOAD_CONST               0
               52  LOAD_GLOBAL              unit
               54  LOAD_FAST                'units'
               56  CALL_FUNCTION_1       1  ''
               58  BINARY_MULTIPLY  
               60  POP_BLOCK        
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    48  '48'

 L. 823        68  DUP_TOP          
               70  LOAD_GLOBAL              UndefinedUnitError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   100  'to 100'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 824        82  LOAD_GLOBAL              logger
               84  LOAD_METHOD              error
               86  LOAD_STR                 'Unsupported unit specified for get_amount'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 825        92  POP_EXCEPT       
               94  POP_EXCEPT       
               96  LOAD_CONST               0
               98  RETURN_VALUE     
            100_0  COME_FROM            74  '74'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            40  '40'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            32  '32'

 L. 831       108  LOAD_FAST                'units'
              110  LOAD_STR                 'fraction'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   136  'to 136'

 L. 832       116  LOAD_FAST                'moles'
              118  LOAD_FAST                'self'
              120  LOAD_METHOD              get_moles_solvent
              122  CALL_METHOD_0         0  ''
              124  LOAD_FAST                'self'
              126  LOAD_METHOD              get_total_moles_solute
              128  CALL_METHOD_0         0  ''
              130  BINARY_ADD       
              132  BINARY_TRUE_DIVIDE
              134  RETURN_VALUE     
            136_0  COME_FROM           114  '114'

 L. 833       136  LOAD_FAST                'units'
              138  LOAD_STR                 '%'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   178  'to 178'

 L. 834       144  LOAD_FAST                'moles'
              146  LOAD_ATTR                to
              148  LOAD_STR                 'kg'
              150  LOAD_STR                 'chem'
              152  LOAD_FAST                'mw'
              154  LOAD_CONST               ('mw',)
              156  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              158  LOAD_FAST                'self'
              160  LOAD_METHOD              get_mass
              162  CALL_METHOD_0         0  ''
              164  LOAD_METHOD              to
              166  LOAD_STR                 'kg'
              168  CALL_METHOD_1         1  ''
              170  BINARY_TRUE_DIVIDE
              172  LOAD_CONST               100
              174  BINARY_MULTIPLY  
              176  RETURN_VALUE     
            178_0  COME_FROM           142  '142'

 L. 835       178  LOAD_GLOBAL              unit
              180  LOAD_FAST                'units'
              182  CALL_FUNCTION_1       1  ''
              184  LOAD_ATTR                dimensionality
              186  LOAD_CONST               ('[substance]/[length]**3', '[mass]/[length]**3')
              188  COMPARE_OP               in
              190  POP_JUMP_IF_FALSE   214  'to 214'

 L. 839       192  LOAD_FAST                'moles'
              194  LOAD_ATTR                to
              196  LOAD_FAST                'units'
              198  LOAD_STR                 'chem'
              200  LOAD_FAST                'mw'
              202  LOAD_FAST                'self'
              204  LOAD_METHOD              get_volume
              206  CALL_METHOD_0         0  ''
              208  LOAD_CONST               ('mw', 'volume')
              210  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              212  RETURN_VALUE     
            214_0  COME_FROM           190  '190'

 L. 840       214  LOAD_GLOBAL              unit
              216  LOAD_FAST                'units'
              218  CALL_FUNCTION_1       1  ''
              220  LOAD_ATTR                dimensionality
              222  LOAD_CONST               ('[substance]/[mass]', '[mass]/[mass]')
              224  COMPARE_OP               in
          226_228  POP_JUMP_IF_FALSE   252  'to 252'

 L. 841       230  LOAD_FAST                'moles'
              232  LOAD_ATTR                to
              234  LOAD_FAST                'units'
              236  LOAD_STR                 'chem'
              238  LOAD_FAST                'mw'
              240  LOAD_FAST                'self'
              242  LOAD_METHOD              get_solvent_mass
              244  CALL_METHOD_0         0  ''
              246  LOAD_CONST               ('mw', 'solvent_mass')
              248  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              250  RETURN_VALUE     
            252_0  COME_FROM           226  '226'

 L. 842       252  LOAD_GLOBAL              unit
              254  LOAD_FAST                'units'
              256  CALL_FUNCTION_1       1  ''
              258  LOAD_ATTR                dimensionality
              260  LOAD_STR                 '[mass]'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   284  'to 284'

 L. 843       268  LOAD_FAST                'moles'
              270  LOAD_ATTR                to
              272  LOAD_FAST                'units'
              274  LOAD_STR                 'chem'
              276  LOAD_FAST                'mw'
              278  LOAD_CONST               ('mw',)
              280  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              282  RETURN_VALUE     
            284_0  COME_FROM           264  '264'

 L. 844       284  LOAD_GLOBAL              unit
              286  LOAD_FAST                'units'
              288  CALL_FUNCTION_1       1  ''
              290  LOAD_ATTR                dimensionality
              292  LOAD_STR                 '[substance]'
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   310  'to 310'

 L. 845       300  LOAD_FAST                'moles'
              302  LOAD_METHOD              to
              304  LOAD_FAST                'units'
              306  CALL_METHOD_1         1  ''
              308  RETURN_VALUE     
            310_0  COME_FROM           296  '296'

 L. 847       310  LOAD_GLOBAL              logger
              312  LOAD_METHOD              error
              314  LOAD_STR                 'Unsupported unit specified for get_amount'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 848       320  LOAD_CONST               None
              322  RETURN_VALUE     

Parse error at or near `ROT_FOUR' instruction at offset 62

    def get_total_amount(self, element, units):
        """
        Return the total amount of 'element' (across all solutes) in the solution.

        Parameters
        ----------
        element : str
                    String representing the name of the element of interest
        units : str
                    Units desired for the output. Examples of valid units are
                    'mol/L','mol/kg','mol', 'kg', and 'g/L'

        Returns
        -------
        The total amount of the element in the solution, in the specified units

        Notes
        -----
        There is currently no way to distinguish between different oxidation
        states of the same element (e.g. TOTFe(II) vs. TOTFe(III)). This
        is planned for a future release. (TODO)

        See Also
        --------
        get_amount
        """
        import pyEQL.chemical_formula as ch
        TOT = 0 * unit(units)
        for item in self.components:
            if ch.contains(item, element):
                amt = self.get_amount(item, units)
                if unit(units).dimensionality in ('[substance]', '[substance]/[length]**3',
                                                  '[substance]/[mass]'):
                    TOT += amt * ch.get_element_mole_ratio(item, element)
            else:
                if unit(units).dimensionality in ('[mass]', '[mass]/[length]**3', '[mass]/[mass]'):
                    TOT += amt * ch.get_element_weight_fraction(item, element)
                return TOT

    def add_amount(self, solute, amount):
        """
        Add the amount of 'solute' to the parent solution.

        Parameters
        ----------
        solute : str
                    String representing the name of the solute of interest
        amount : str quantity
                    String representing the concentration desired, e.g. '1 mol/kg'
                    If the units are given on a per-volume basis, the solution
                    volume is not recalculated
                    If the units are given on a mass, substance, per-mass, or
                    per-substance basis, then the solution volume is recalculated
                    based on the new composition

        Returns
        -------
        Nothing. The concentration of solute is modified.

        See Also
        --------
        Solute.add_moles
        """
        if unit(amount).dimensionality in ('[substance]/[length]**3', '[mass]/[length]**3'):
            orig_volume = self.get_volume()
            self.get_solute(solute).add_moles(amount, self.get_volume(), self.get_solvent_mass())
            if self.get_amount(solute, 'mol').magnitude < 0:
                logger.warning('Attempted to set a negative concentration for solute %s. Concentration set to 0' % solute)
                self.set_amount(solute, '0 mol')
            solute_vol = self._get_solute_volume()
            target_vol = orig_volume - solute_vol
            target_mass = target_vol * h2o.water_density(self.get_temperature())
            mw = self.get_solvent().get_molecular_weight()
            target_mol = target_mass / mw
            self.get_solvent().moles = target_mol
        else:
            self.get_solute(solute).add_moles(amount, self.get_volume(), self.get_solvent_mass())
            if self.get_amount(solute, 'mol').magnitude < 0:
                logger.warning('Attempted to set a negative concentration for solute %s. Concentration set to 0' % solute)
                self.set_amount(solute, '0 mol')
            if self.get_solvent_mass() <= unit('0 kg'):
                logger.error('All solvent has been depleted from the solution')
                return None
            self.volume_update_required = True

    def set_amount(self, solute, amount):
        """
        Set the amount of 'solute' in the parent solution.

        Parameters
        ----------
        solute : str
                    String representing the name of the solute of interest
        amount : str Quantity
                    String representing the concentration desired, e.g. '1 mol/kg'
                    If the units are given on a per-volume basis, the solution
                    volume is not recalculated and the molar concentrations of
                    other components in the solution are not altered, while the
                    molal concentrations are modified.

                    If the units are given on a mass, substance, per-mass, or
                    per-substance basis, then the solution volume is recalculated
                    based on the new composition and the molal concentrations of
                    other components are not altered, while the molar concentrations
                    are modified.

        Returns
        -------
        Nothing. The concentration of solute is modified.

        See Also
        --------
        Solute.set_moles
        """
        if unit(amount).magnitude < 0:
            logger.error('Negative amount specified for solute %s. Concentration not changed.' % solute)
        else:
            if unit(amount).dimensionality in ('[substance]/[length]**3', '[mass]/[length]**3'):
                orig_volume = self.get_volume()
                self.get_solute(solute).set_moles(amount, self.get_volume(), self.get_solvent_mass())
                solute_vol = self._get_solute_volume()
                target_vol = orig_volume - solute_vol
                target_mass = target_vol * h2o.water_density(self.get_temperature())
                mw = self.get_solvent().get_molecular_weight()
                target_mol = target_mass / mw
                self.get_solvent().moles = target_mol
            else:
                self.get_solute(solute).set_moles(amount, self.get_volume(), self.get_solvent_mass())
                if self.get_solvent_mass() <= unit('0 kg'):
                    logger.error('All solvent has been depleted from the solution')
                    return None
                self._update_volume()

    def get_osmolarity(self, activity_correction=False):
        """Return the osmolarity of the solution in Osm/L

        Parameters
        ----------
        activity_correction : bool
                If TRUE, the osmotic coefficient is used to calculate the
                osmolarity. This correction is appropriate when trying to predict
                the osmolarity that would be measured from e.g. freezing point
                depression. Defaults to FALSE if omitted.
        """
        if activity_correction is True:
            factor = self.get_osmotic_coefficient()
        else:
            factor = 1
        return factor * self.get_total_moles_solute() / self.get_volume().to('L')

    def get_osmolality(self, activity_correction=False):
        """Return the osmolality of the solution in Osm/kg

        Parameters
        ----------
        activity_correction : bool
                If TRUE, the osmotic coefficient is used to calculate the
                osmolarity. This correction is appropriate when trying to predict
                the osmolarity that would be measured from e.g. freezing point
                depression. Defaults to FALSE if omitted.
        """
        if activity_correction is True:
            factor = self.get_osmotic_coefficient()
        else:
            factor = 1
        return factor * self.get_total_moles_solute() / self.get_solvent_mass().to('kg')

    def get_total_moles_solute(self):
        """Return the total moles of all solute in the solution"""
        tot_mol = 0
        for item in self.components:
            if item != self.solvent_name:
                tot_mol += self.components[item].get_moles()
            return tot_mol

    def get_mole_fraction(self, solute):
        """
        Return the mole fraction of 'solute' in the solution

        Notes
        -----
        This function is DEPRECATED and will raise a warning when called.
        Use get_amount() instead and specify 'fraction' as the unit type.
        """
        logger.warning('get_mole_fraction is DEPRECATED! Use get_amount() instead.')
        return self.get_amount(solute, 'fraction')

    def get_moles_solvent(self):
        """
        Return the moles of solvent present in the solution

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
            The moles of solvent in the solution.

        """
        return self.get_amount(self.solvent_name, 'mol')

    def get_salt(self):
        """
        Determine the predominant salt in a solution of ions.

        Many empirical equations for solution properties such as activity coefficient,
        partial molar volume, or viscosity are based on the concentration of
        single salts (e.g., NaCl). When multiple ions are present (e.g., a solution
        containing Na+, Cl-, and Mg+2), it is generally not possible to direclty model
        these quantities. pyEQL works around this problem by treating such solutions
        as single salt solutions.

        The get_salt() method examines the ionic composition of a solution and returns
        an object that identifies the single most predominant salt in the solution, defined
        by the cation and anion with the highest mole fraction. The Salt object contains
        information about the stoichiometry of the salt to enable its effective concentration
        to be calculated (e.g., 1 M MgCl2 yields 1 M Mg+2 and 2 M Cl-).

        Parameters
        ----------
        None

        Returns
        -------
        Salt
            Salt object containing information about the parent salt.

        See Also
        --------
        get_activity
        get_activity_coefficient
        get_water_activity
        get_osmotic_coefficient
        get_osmotic_pressure
        get_viscosity_kinematic

        Examples
        --------
        >>> s1 = Solution([['Na+','0.5 mol/kg'],['Cl-','0.5 mol/kg']])
        >>> s1.get_salt()
        <pyEQL.salt_ion_match.Salt object at 0x7fe6d3542048>
        >>> s1.get_salt().formula
        'NaCl'
        >>> s1.get_salt().nu_cation
        1
        >>> s1.get_salt().z_anion
        -1

        >>> s2 = pyEQL.Solution([['Na+','0.1 mol/kg'],['Mg+2','0.2 mol/kg'],['Cl-','0.5 mol/kg']])
        >>> s2.get_salt().formula
        'MgCl2'
        >>> s2.get_salt().nu_anion
        2
        >>> s2.get_salt().z_cation
        2
        """
        import pyEQL.salt_ion_match as salt
        return salt.identify_salt(self)

    def get_salt_list(self):
        """
        Determine the predominant salt in a solution of ions.

        Many empirical equations for solution properties such as activity coefficient,
        partial molar volume, or viscosity are based on the concentration of
        single salts (e.g., NaCl). When multiple ions are present (e.g., a solution
        containing Na+, Cl-, and Mg+2), it is generally not possible to direclty model
        these quantities.

        The get_salt_list() method examines the ionic composition of a solution and
        simplifies it into a list of salts. The method retuns a dictionary of
        Salt objects where the keys are the salt formulas (e.g., 'NaCl'). The
        Salt object contains information about the stoichiometry of the salt to
        enable its effective concentration to be calculated
        (e.g., 1 M MgCl2 yields 1 M Mg+2 and 2 M Cl-).

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary of Salt objects, keyed to the salt formula

        See Also
        --------
        get_activity
        get_activity_coefficient
        get_water_activity
        get_osmotic_coefficient
        get_osmotic_pressure
        get_viscosity_kinematic

        """
        import pyEQL.salt_ion_match as salt
        return salt.generate_salt_list(self, unit='mol/kg')

    def get_activity_coefficient(self, solute, scale='molal', verbose=False):
        r"""Return the activity coefficient of a solute in solution.

        Whenever the appropriate parameters are available, the Pitzer model [#]_ is used.
        If no Pitzer parameters are available, then the appropriate equations are selected
        according to the following logic: [#]_

        I <= 0.0005: Debye-Huckel equation
        0.005 < I <= 0.1:  Guntelberg approximation
        0.1 < I <= 0.5: Davies equation
        I > 0.5: Raises a warning and returns activity coefficient = 1

        The ionic strength, activity coefficients, and activities are all
        calculated based on the molal (mol/kg) concentration scale. If a different
        scale is given as input, then the molal-scale activity coefficient :math:`\gamma_\pm` is
        converted according to [#]_

        .. math:: f_\pm = \gamma_\pm * (1 + M_w \sum_i \nu_i \m_i)

        .. math:: y_\pm = m \rho_w / C \gamma_\pm

        where :math:`f_\pm` is the rational activity coefficient, :math:`M_w` is
        the molecular weight of water, the summation represents the total molality of
        all solute  species, :math:`y_\pm` is the molar activity coefficient,
        :math:`\rho_w` is the density of pure water, :math:`m` and :math:`C` are
        the molal and molar concentrations of the chosen salt (not individual solute),
        respectively.

        Parameters
        ----------
        solute : str
                    String representing the name of the solute of interest
        scale : str, optional
                    The concentration scale for the returned activity coefficient.
                    Valid options are "molal", "molar", and "rational" (i.e., mole fraction).
                    By default, the molal scale activity coefficient is returned.
        verbose : bool, optional
                    If True, pyEQL will print a message indicating the parent salt
                    that is being used for activity calculations. This option is
                    useful when modeling multicomponent solutions. False by default.

        Returns
        -------
        The mean ion activity coefficient of the solute in question on  the selected scale.

        See Also
        --------
        get_ionic_strength
        get_salt
        activity_correction.get_activity_coefficient_debyehuckel
        activity_correction.get_activity_coefficient_guntelberg
        activity_correction.get_activity_coefficient_davies
        activity_correction.get_activity_coefficient_pitzer

        Notes
        -----
        For multicomponent mixtures, pyEQL implements the "effective Pitzer model"
        presented by Mistry et al. [#]_. In this model, the activity coefficient
        of a salt in a multicomponent mixture is calculated using an "effective
        molality," which is the molality that would result in a single-salt
        mixture with the same total ionic strength as the multicomponent solution.

        .. math:: m_effective = 2 I \over (\nu_+ z_+^2 + \nu_- z_- ^2)

        References
        ----------
        .. [#] May, P. M., Rowland, D., Hefter, G., & Königsberger, E. (2011).
               A Generic and Updatable Pitzer Characterization of Aqueous Binary Electrolyte Solutions at 1 bar and
               25 °C. *Journal of Chemical & Engineering Data*, 56(12), 5066–5077. doi:10.1021/je2009329

        .. [#] Stumm, Werner and Morgan, James J. *Aquatic Chemistry*, 3rd ed,
               pp 165. Wiley Interscience, 1996.

        .. [#] Robinson, R. A.; Stokes, R. H. Electrolyte Solutions: Second Revised
               Edition; Butterworths: London, 1968, p.32.

        """
        ion = self.components[solute]
        temperature = str(self.get_temperature())
        if self.get_amount(solute, 'mol').magnitude == 0:
            return unit('1 dimensionless')
        Salt = None
        salt_list = salt.generate_salt_list(self, unit='mol/kg')
        for item in salt_list:
            if not solute == item.cation:
                if solute == item.anion:
                    Salt = item
                if Salt is None:
                    logger.warning('No salts found that contain solute %s. Returning unit activity coefficient.' % solute)
                    return unit('1 dimensionless')
                db.search_parameters(Salt.formula)
                if db.has_parameter(Salt.formula, 'pitzer_parameters_activity'):
                    if verbose is True:
                        print('Calculating activity coefficient based on parent salt %s' % Salt.formula)
                    param = db.get_parameter(Salt.formula, 'pitzer_parameters_activity')
                    if Salt.nu_cation >= 2:
                        if not Salt.nu_anion <= -2 or Salt.nu_cation >= 3 or Salt.nu_anion <= -3:
                            alpha1 = 2
                            alpha2 = 50
                        else:
                            alpha1 = 1.4
                            alpha2 = 12
                    else:
                        alpha1 = 2
                        alpha2 = 0
                    molality = Salt.get_effective_molality(self.get_ionic_strength())
                    activity_coefficient = ac.get_activity_coefficient_pitzer(self.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
                    logger.info('Calculated activity coefficient of species %s as %s based on salt %s using Pitzer model' % (
                     solute, activity_coefficient, Salt))
                    molal = activity_coefficient
                else:
                    if self.get_ionic_strength().magnitude <= 0.005:
                        logger.info('Ionic strength = %s. Using Debye-Huckel to calculate activity coefficient.' % self.get_ionic_strength())
                        molal = ac.get_activity_coefficient_debyehuckel(self.get_ionic_strength(), ion.get_formal_charge(), temperature)
                    else:
                        if self.get_ionic_strength().magnitude <= 0.1:
                            logger.info('Ionic strength = %s. Using Guntelberg to calculate activity coefficient.' % self.get_ionic_strength())
                            molal = ac.get_activity_coefficient_guntelberg(self.get_ionic_strength(), ion.get_formal_charge(), temperature)
                        else:
                            if self.get_ionic_strength().magnitude <= 0.5:
                                logger.info('Ionic strength = %s. Using Davies equation to calculate activity coefficient.' % self.get_ionic_strength())
                                molal = ac.get_activity_coefficient_davies(self.get_ionic_strength(), ion.get_formal_charge(), temperature)
                            else:
                                logger.warning('Ionic strength too high to estimate activity for species %s. Specify parameters for Pitzer model.Returning unit activity coefficient' % solute)
                                molal = unit('1 dimensionless')
                if scale == 'molal':
                    return molal
                if scale == 'molar':
                    total_molality = self.get_total_moles_solute() / self.get_solvent_mass()
                    total_molarity = self.get_total_moles_solute() / self.get_volume()
                    return (molal * h2o.water_density(self.get_temperature()) * total_molality / total_molarity).to('dimensionless')
                if scale == 'rational':
                    return molal * (1 + unit('0.018 kg/mol') * self.get_total_moles_solute() / self.get_solvent_mass())
            logger.warning('Invalid scale argument. Returning molal-scale activity coefficient')
            return molal

    def get_activity(self, solute, scale='molal', verbose=False):
        """
        Return the thermodynamic activity of the solute in solution on the molal scale.

        Parameters
        ----------
        solute : str
                    String representing the name of the solute of interest
        scale : str, optional
                    The concentration scale for the returned activity.
                    Valid options are "molal", "molar", and "rational" (i.e., mole fraction).
                    By default, the molal scale activity is returned.
        verbose : bool, optional
                    If True, pyEQL will print a message indicating the parent salt
                    that is being used for activity calculations. This option is
                    useful when modeling multicomponent solutions. False by default.

        Returns
        -------
        The thermodynamic activity of the solute in question (dimensionless)

        See Also
        --------
        get_activity_coefficient
        get_ionic_strength
        get_salt

        Notes
        -----
        The thermodynamic activity depends on the concentration scale used [#].
        By default, the ionic strength, activity coefficients, and activities are all
        calculated based on the molal (mol/kg) concentration scale.

        References
        ----------
        .. [#] Robinson, R. A.; Stokes, R. H. Electrolyte Solutions: Second Revised
               Edition; Butterworths: London, 1968, p.32.

        """
        if solute == 'H2O' or solute == 'water':
            activity = self.get_water_activity()
        else:
            if scale == 'molal':
                unit = 'mol/kg'
            else:
                if scale == 'molar':
                    unit = 'mol/L'
                else:
                    if scale == 'rational':
                        unit = 'fraction'
                    else:
                        logger.error('Invalid scale argument. Returning molal-scale activity.')
                        unit = 'mol/kg'
                        scale = 'molal'
            activity = self.get_activity_coefficient(solute, scale=scale, verbose=verbose) * self.get_amount(solute, unit).magnitude
            logger.info('Calculated %s scale activity of solute %s as %s' % (
             scale, solute, activity))
        return activity

    def get_osmotic_coefficient(self, scale='molal'):
        r"""
        Return the osmotic coefficient of an aqueous solution.

        Osmotic coefficient is calculated using the Pitzer model.[#]_ If appropriate parameters for
        the model are not available, then pyEQL raises a WARNING and returns an osmotic
        coefficient of 1.

        If the 'rational' scale is given as input, then the molal-scale osmotic
        coefficient :math:`\phi` is converted according to [#]_

        .. math:: g = - \phi * M_w \sum_i \nu_i \m_i) / \ln x_w

        where :math:`g` is the rational osmotic coefficient, :math:`M_w` is
        the molecular weight of water, the summation represents the total molality of
        all solute  species, and :math:`x_w` is the mole fraction of water.

        Parameters
        ----------
        scale : str, optional
                    The concentration scale for the returned osmotic coefficient.
                    Valid options are "molal", "rational" (i.e., mole fraction),
                    and "fugacity".  By default, the molal scale osmotic coefficient is returned.
        Returns
        -------
        Quantity :
            The osmotic coefficient

        See Also
        --------
        get_water_activity
        get_ionic_strength
        get_salt

        Notes
        -----
        For multicomponent mixtures, pyEQL adopts the "effective Pitzer model"
        presented by Mistry et al. [#]_. In this approach, the osmotic coefficient of
        each individual salt is calculated using the normal Pitzer model based
        on its respective concentration. Then, an effective osmotic coefficient
        is calculated as the concentration-weighted average of the individual
        osmotic coefficients.

        For example, in a mixture of 0.5 M NaCl and 0.5 M KBr, one would calculate
        the osmotic coefficient for each salt using a concentration of 0.5 M and
        an ionic strength of 1 M. Then, one would average the two resulting
        osmotic coefficients to obtain an effective osmotic coefficient for the
        mixture.

        (Note: in the paper referenced below, the effective
        osmotic coefficient is determined by weighting using the "effective molality"
        rather than the true molality. Subsequent checking and correspondence with
        the author confirmed that the weight factor should be the true molality, and
        that is what is implemented in pyEQL.)

        References
        ----------
        .. [#] May, P. M., Rowland, D., Hefter, G., & Königsberger, E. (2011).
               A Generic and Updatable Pitzer Characterization of Aqueous Binary Electrolyte Solutions at 1 bar
               and 25 °C. *Journal of Chemical & Engineering Data*, 56(12), 5066–5077. doi:10.1021/je2009329

        .. [#] Robinson, R. A.; Stokes, R. H. Electrolyte Solutions: Second Revised
               Edition; Butterworths: London, 1968, p.32.

        .. [#] Mistry, K. H.; Hunter, H. a.; Lienhard V, J. H. Effect of composition and nonideal solution behavior on
               desalination calculations for mixed
               electrolyte solutions with comparison to seawater. Desalination 2013, 318, 34–47.

        Examples
        --------
        >>> s1 = pyEQL.Solution([['Na+','0.2 mol/kg'],['Cl-','0.2 mol/kg']])
        >>> s1.get_osmotic_coefficient()
        <Quantity(0.9235996615888572, 'dimensionless')>

        >>> s1 = pyEQL.Solution([['Mg+2','0.3 mol/kg'],['Cl-','0.6 mol/kg']],temperature='30 degC')
        >>> s1.get_osmotic_coefficient()
        <Quantity(0.891154788474231, 'dimensionless')>

        """
        temperature = str(self.get_temperature())
        ionic_strength = self.get_ionic_strength()
        effective_osmotic_sum = 0
        molality_sum = 0
        salt_list = self.get_salt_list()
        for item in salt_list:
            if item.formula == 'HOH':
                pass
            elif item.z_cation >= 2:
                if item.z_anion <= -2:
                    if item.z_cation >= 3 or item.z_anion <= -3:
                        alpha1 = 2
                        alpha2 = 50
                    else:
                        alpha1 = 1.4
                        alpha2 = 12
                else:
                    alpha1 = 2
                    alpha2 = 0
                concentration = salt_list[item]
                molality_sum += concentration
                db.search_parameters(item.formula)
                if db.has_parameter(item.formula, 'pitzer_parameters_activity'):
                    param = db.get_parameter(item.formula, 'pitzer_parameters_activity')
                    osmotic_coefficient = ac.get_osmotic_coefficient_pitzer(ionic_strength, concentration, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], item.z_cation, item.z_anion, item.nu_cation, item.nu_anion, temperature)
                    logger.info('Calculated osmotic coefficient of water as %s based on salt %s using Pitzer model' % (
                     osmotic_coefficient, item.formula))
                    effective_osmotic_sum += concentration * osmotic_coefficient
            else:
                logger.warning('Cannot calculate osmotic coefficient because Pitzer parameters for salt %s are not specified. Returning unit osmotic coefficient' % item.formula)
                effective_osmotic_sum += concentration * unit('1 dimensionless')
        else:
            molal_phi = effective_osmotic_sum / molality_sum
            if scale == 'molal':
                return molal_phi
            if scale == 'rational':
                solvent = self.get_solvent().formula
                return -molal_phi * unit('0.018 kg/mol') * self.get_total_moles_solute() / self.get_solvent_mass() / math.log(self.get_amount(solvent, 'fraction'))
            if scale == 'fugacity':
                solvent = self.get_solvent().formula
                return math.exp(-molal_phi * unit('0.018 kg/mol') * self.get_total_moles_solute() / self.get_solvent_mass() - math.log(self.get_amount(solvent, 'fraction')))
            logger.warning('Invalid scale argument. Returning molal-scale osmotic coefficient')
            return molal_phi

    def get_water_activity(self):
        r"""
        Return the water activity.

        Returns
        -------
        Quantity :
            The thermodynamic activity of water in the solution.

        See Also
        --------
        get_osmotic_coefficient
        get_ionic_strength
        get_salt

        Notes
        -----
        Water activity is related to the osmotic coefficient in a solution containing i solutes by: [#]_

        .. math:: \ln a_w = - \Phi M_w \sum_i m_i

        Where :math:`M_w` is the molar mass of water (0.018015 kg/mol) and :math:`m_i` is the molal concentration
        of each species.

        If appropriate Pitzer model parameters are not available, the
        water activity is assumed equal to the mole fraction of water.

        References
        ----------
        .. [#] Blandamer, Mike J., Engberts, Jan B. F. N., Gleeson, Peter T., Reis, Joao Carlos R., 2005. "Activity of         water in aqueous systems: A frequently neglected property." *Chemical Society Review* 34, 440-458.

        Examples
        --------
        >>> s1 = pyEQL.Solution([['Na+','0.3 mol/kg'],['Cl-','0.3 mol/kg']])
        >>> s1.get_water_activity()
        <Quantity(0.9900944932888518, 'dimensionless')>
        """
        osmotic_coefficient = self.get_osmotic_coefficient()
        if osmotic_coefficient == 1:
            logger.warning('Pitzer parameters not found. Water activity set equal to mole fraction')
            return self.get_amount('H2O', 'fraction').to('dimensionless')
        concentration_sum = unit('0 mol/kg')
        for item in self.components:
            if item == 'H2O':
                pass
            else:
                concentration_sum += self.get_amount(item, 'mol/kg')
        else:
            logger.info('Calculated water activity using osmotic coefficient')
            return math.exp(-osmotic_coefficient * 0.018015 * unit('kg/mol') * concentration_sum) * unit('1 dimensionless')

    def get_ionic_strength(self):
        r"""
        Return the ionic strength of the solution.

        Return the ionic strength of the solution, calculated as 1/2 * sum ( molality * charge ^2) over all the ions.
        Molal (mol/kg) scale concentrations are used for compatibility with the activity correction formulas.

        Returns
        -------
        Quantity :
            The ionic strength of the parent solution, mol/kg.

        See Also
        --------
        get_activity
        get_water_activity

        Notes
        -----
        The ionic strength is calculated according to:

        .. math:: I = \sum_i m_i z_i^2

        Where :math:`m_i` is the molal concentration and :math:`z_i` is the charge on species i.

        Examples
        --------
        >>> s1 = pyEQL.Solution([['Na+','0.2 mol/kg'],['Cl-','0.2 mol/kg']])
        >>> s1.get_ionic_strength()
        <Quantity(0.20000010029672785, 'mole / kilogram')>

        >>> s1 = pyEQL.Solution([['Mg+2','0.3 mol/kg'],['Na+','0.1 mol/kg'],['Cl-','0.7 mol/kg']],temperature='30 degC')
        >>> s1.get_ionic_strength()
        <Quantity(1.0000001004383303, 'mole / kilogram')>
        """
        self.ionic_strength = 0
        for solute in self.components.keys():
            self.ionic_strength += 0.5 * self.get_amount(solute, 'mol/kg') * self.components[solute].get_formal_charge() ** 2
        else:
            return self.ionic_strength

    def get_charge_balance(self):
        r"""
        Return the charge balance of the solution.

        Return the charge balance of the solution. The charge balance represents the net electric charge
        on the solution and SHOULD equal zero at all times, but due to numerical errors will usually
        have a small nonzero value.

        Returns
        -------
        float :
            The charge balance of the solution, in equivalents.

        Notes
        -----
        The charge balance is calculated according to:

        .. math:: CB = F \sum_i n_i z_i

        Where :math:`n_i` is the number of moles, :math:`z_i` is the charge on species i, and :math:`F` is the Faraday
        constant.

        """
        self.charge_balance = 0
        for solute in self.components.keys():
            self.charge_balance += self.get_amount(solute, 'mol') * self.components[solute].get_formal_charge() * unit.e * unit.N_A
        else:
            return self.charge_balance.magnitude

    def get_alkalinity(self):
        r"""
        Return the alkalinity or acid neutralizing capacity of a solution

        Returns
        -------
        Quantity :
            The alkalinity of the solution in mg/L as CaCO3

        Notes
        -----
        The alkalinity is calculated according to: [#]_

        .. math:: Alk = F \sum_i z_i C_B - \sum_i z_i C_A

        Where :math:`C_B` and :math:`C_A` are conservative cations and anions, respectively
        (i.e. ions that do not participate in acid-base reactions), and :math:`z_i` is their charge.
        In this method, the set of conservative cations is all Group I and Group II cations, and the conservative anions
        are all the anions of strong acids.

        References
        ----------
        .. [#] Stumm, Werner and Morgan, James J. Aquatic Chemistry, 3rd ed,
               pp 165. Wiley Interscience, 1996.
        """
        alkalinity = 0 * unit('mol/L')
        equiv_wt_CaCO3 = 50.045 * unit('g/mol')
        base_cations = [
         'Li+',
         'Na+',
         'K+',
         'Rb+',
         'Cs+',
         'Fr+',
         'Be+2',
         'Mg+2',
         'Ca+2',
         'Sr+2',
         'Ba+2',
         'Ra+2']
        acid_anions = [
         'Cl-', 'Br-', 'I-', 'SO4-2', 'NO3-', 'ClO4-', 'ClO3-']
        for item in self.components:
            if item in base_cations:
                z = self.get_solute(item).get_formal_charge()
                alkalinity += self.get_amount(item, 'mol/L') * z
            if item in acid_anions:
                z = self.get_solute(item).get_formal_charge()
                alkalinity -= self.get_amount(item, 'mol/L') * z
            return (alkalinity * equiv_wt_CaCO3).to('mg/L')

    def get_hardness(self):
        """
        Return the hardness of a solution.

        Hardness is defined as the sum of the equivalent concentrations
        of multivalent cations as calcium carbonate.

        NOTE: at present pyEQL cannot distinguish between mg/L as CaCO3
        and mg/L units. Use with caution.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
            The hardness of the solution in mg/L as CaCO3

        """
        hardness = 0 * unit('mol/L')
        equiv_wt_CaCO3 = 50.045 * unit('g/mol')
        for item in self.components:
            z = self.get_solute(item).get_formal_charge()
            if z > 1:
                hardness += z * self.get_amount(item, 'mol/L')
            return (hardness * equiv_wt_CaCO3).to('mg/L')

    def get_debye_length(self):
        r"""
        Return the Debye length of a solution

        Debye length is calculated as [#]_

        .. math::

            \kappa^{-1} = \sqrt({\epsilon_r \epsilon_o k_B T \over (2 N_A e^2 I)})

        where :math:`I` is the ionic strength, :math:`epsilon_r` and :math:`epsilon_r`
        are the relative permittivity and vacuum permittivity, :math:`k_B` is the
        Boltzmann constant, and :math:`T` is the temperature, :math:`e` is the
        elementary charge, and :math:`N_A` is Avogadro's number.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
            The Debye length, in nanometers.

        References
        ----------
        .. [#] https://en.wikipedia.org/wiki/Debye_length#Debye_length_in_an_electrolyte

        See Also
        --------
        get_ionic_strength
        get_dielectric_constant

        """
        temperature = self.get_temperature()
        ionic_strength = self.get_ionic_strength().magnitude * unit('mol/L')
        dielectric_constant = self.get_dielectric_constant()
        debye_length = (dielectric_constant * unit.epsilon_0 * unit.k * temperature / (2 * unit.N_A * unit.e ** 2 * ionic_strength)) ** 0.5
        return debye_length.to('nm')

    def get_bjerrum_length(self):
        r"""
        Return the Bjerrum length of a solution

        Bjerrum length representes the distance at which electrostatic
        interactions between particles become comparable in magnitude
        to the thermal energy.:math:`\lambda_B` is calculated as [#]_

        .. math::

            \lambda_B = {e^2 \over (4 \pi \epsilon_r \epsilon_o k_B T)}

        where :math:`e` is the fundamental charge, :math:`epsilon_r` and :math:`epsilon_r`
        are the relative permittivity and vacuum permittivity, :math:`k_B` is the
        Boltzmann constant, and :math:`T` is the temperature.

        Parameters
        ----------
        None

        Returns
        -------
        Quantity
            The Bjerrum length, in nanometers.

        References
        ----------
        .. [#] https://en.wikipedia.org/wiki/Bjerrum_length

        Examples
        --------
        >>> s1 = pyEQL.Solution()
        >>> s1.get_bjerrum_length()
        <Quantity(0.7152793009386953, 'nanometer')>

        See Also
        --------
        get_dielectric_constant

        """
        temperature = self.get_temperature()
        dielectric_constant = self.get_dielectric_constant()
        bjerrum_length = unit.e ** 2 / (4 * math.pi * dielectric_constant * unit.epsilon_0 * unit.k * temperature)
        return bjerrum_length.to('nm')

    def get_transport_number(self, solute, activity_correction=False):
        r"""
        Calculate the transport number of the solute in the solution

        Parameters
        ----------
        solute : str
            String identifying the solute for which the transport number is
            to be calculated.

        activity_correction: bool
            If True, the transport number will be corrected for activity following
            the same method used for solution conductivity. Defaults to False
            if omitted.

        Returns
        -------
        float
            The transport number of `solute`

        Notes
        -----
        Transport number is calculated according to [#]_ :

        .. math::

            t_i = {D_i z_i^2 C_i \over \sum D_i z_i^2 C_i}

        Where :math:`C_i` is the concentration in mol/L, :math:`D_i` is the diffusion
        coefficient, and :math:`z_i` is the charge, and the summation extends
        over all species in the solution.

        If `activity_correction` is True, the contribution of each ion to the
        transport number is corrected with an activity factor. See the documentation
        for get_conductivity() for an explanation of this correction.

        References
        ----------
        .. [#] Geise, G. M.; Cassady, H. J.; Paul, D. R.; Logan, E.; Hickner, M. A. "Specific
               ion effects on membrane potential and the permselectivity of ion exchange membranes.""
               *Phys. Chem. Chem. Phys.* 2014, 16, 21673–21681.

        """
        denominator = 0
        numerator = 0
        for item in self.components:
            z = self.get_solute(item).get_formal_charge()
            term = self.get_property(item, 'diffusion_coefficient') * z ** 2 * self.get_amount(item, 'mol/L')
            if activity_correction is True:
                gamma = self.get_activity_coefficient(item)
                if self.get_ionic_strength().magnitude < 0.36 * z:
                    alpha = 0.6 / z ** 0.5
                else:
                    alpha = self.get_ionic_strength().magnitude ** 0.5 / z
                if item == solute:
                    numerator = term * gamma ** alpha
                denominator += term * gamma ** alpha
            else:
                if item == solute:
                    numerator = term
                denominator += term
        else:
            return (numerator / denominator).to('dimensionless')

    def get_molar_conductivity(self, solute):
        r"""
        Calculate the molar (equivalent) conductivity for a solute

        Parameters
        ----------
        solute : str
            String identifying the solute for which the molar conductivity is
            to be calculated.

        Returns
        -------
        float
                The molar or equivalent conductivity of the species in the solution.
                Zero if the solute is not charged.

        Notes
        -----
        Molar conductivity is calculated from the Nernst-Einstein relation [#]_

        .. math::

            \kappa_i = {z_i^2 D_i F^2 \over RT}

        Note that the diffusion coefficient is strongly variable with temperature.

        References
        ----------

        .. [#] Smedley, Stuart. The Interpretation of Ionic Conductivity in Liquids, pp 1-9. Plenum Press, 1980.

        Examples
        --------
        TODO

        """
        temperature = self.get_temperature()
        D = self.get_property(solute, 'diffusion_coefficient')
        molar_cond = D * (unit.e * unit.N_A) ** 2 * self.get_solute(solute).get_formal_charge() ** 2 / (unit.R * temperature)
        logger.info('Computed molar conductivity as %s from D = %s at T=%s' % (
         molar_cond, str(D), temperature))
        return molar_cond.to('mS / cm / (mol/L)')

    def get_mobility(self, solute):
        r"""
        Calculate the ionic mobility of the solute

        Parameters
        ----------
        solute : str
            String identifying the solute for which the mobility is
            to be calculated.

        Returns
        -------
        float : The ionic mobility. Zero if the solute is not charged.

        Notes
        -----
        This function uses the Einstein relation to convert a diffusion coefficient
        into an ionic mobility [#]_

        .. math::

            \mu_i = {F |z_i| D_i \over RT}

        References
        ----------
        .. [#] Smedley, Stuart I. The Interpretation of Ionic Conductivity in Liquids. Plenum Press, 1980.

        """
        temperature = self.get_temperature()
        D = self.get_property(solute, 'diffusion_coefficient')
        mobility = unit.N_A * unit.e * abs(self.get_solute(solute).get_formal_charge()) * D / (unit.R * temperature)
        logger.info('Computed ionic mobility as %s from D = %s at T=%s' % (
         mobility, str(D), temperature))
        return mobility.to('m**2/V/s')

    def get_property(self, solute, name):
        """Retrieve a thermodynamic property (such as diffusion coefficient)
        for solute, and adjust it from the reference conditions to the conditions
        of the solution

        Parameters
        ----------
        solute: str
            String representing the chemical formula of the solute species
        name: str
            The name of the property needed, e.g.
            'diffusion coefficient'

        Returns
        -------
        Quantity: The desired parameter

        """
        if db.has_parameter(solute, name):
            base_value = self.get_solute(solute).get_parameter(name)
        else:
            base_value = None
        base_temperature = unit('25 degC')
        base_pressure = unit('1 atm')
        if name == 'diffusion_coefficient':
            if base_value is not None:
                return base_value * self.get_temperature() / base_temperature * h2o.water_viscosity_dynamic(base_temperature, base_pressure) / self.get_viscosity_dynamic()
                logger.warning('Diffusion coefficient not found for species %s. Assuming zero.' % solute)
                return unit('0 m**2/s')
                if name == 'partial_molar_volume':
                    if solute == 'H2O':
                        vol = self.get_solute('H2O').get_molecular_weight() / h2o.water_density(self.get_temperature())
                        return vol.to('cm **3 / mol')
                    if base_value is not None:
                        return base_value
            else:
                logger.warning('Partial molar volume not found for species %s. Assuming zero.' % solute)
                return unit('0 cm **3 / mol')
        else:
            logger.warning('%s has not been corrected for solution conditions' % name)
            return base_value

    def get_chemical_potential_energy--- This code section failed: ---

 L.2359         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_temperature
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'temperature'

 L.2361         8  LOAD_GLOBAL              unit
               10  LOAD_STR                 '0 J'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'E'

 L.2364        16  LOAD_FAST                'self'
               18  LOAD_ATTR                components
               20  GET_ITER         
               22  FOR_ITER            166  'to 166'
               24  STORE_FAST               'item'

 L.2365        26  SETUP_FINALLY       140  'to 140'

 L.2366        28  LOAD_FAST                'activity_correction'
               30  LOAD_CONST               True
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    86  'to 86'

 L.2367        36  LOAD_FAST                'E'

 L.2368        38  LOAD_GLOBAL              unit
               40  LOAD_ATTR                R

 L.2369        42  LOAD_FAST                'temperature'
               44  LOAD_METHOD              to
               46  LOAD_STR                 'K'
               48  CALL_METHOD_1         1  ''

 L.2368        50  BINARY_MULTIPLY  

 L.2370        52  LOAD_FAST                'self'
               54  LOAD_METHOD              get_amount
               56  LOAD_FAST                'item'
               58  LOAD_STR                 'mol'
               60  CALL_METHOD_2         2  ''

 L.2368        62  BINARY_MULTIPLY  

 L.2371        64  LOAD_GLOBAL              math
               66  LOAD_METHOD              log
               68  LOAD_FAST                'self'
               70  LOAD_METHOD              get_activity
               72  LOAD_FAST                'item'
               74  CALL_METHOD_1         1  ''
               76  CALL_METHOD_1         1  ''

 L.2368        78  BINARY_MULTIPLY  

 L.2367        80  INPLACE_ADD      
               82  STORE_FAST               'E'
               84  JUMP_FORWARD        136  'to 136'
             86_0  COME_FROM            34  '34'

 L.2374        86  LOAD_FAST                'E'

 L.2375        88  LOAD_GLOBAL              unit
               90  LOAD_ATTR                R

 L.2376        92  LOAD_FAST                'temperature'
               94  LOAD_METHOD              to
               96  LOAD_STR                 'K'
               98  CALL_METHOD_1         1  ''

 L.2375       100  BINARY_MULTIPLY  

 L.2377       102  LOAD_FAST                'self'
              104  LOAD_METHOD              get_amount
              106  LOAD_FAST                'item'
              108  LOAD_STR                 'mol'
              110  CALL_METHOD_2         2  ''

 L.2375       112  BINARY_MULTIPLY  

 L.2378       114  LOAD_GLOBAL              math
              116  LOAD_METHOD              log
              118  LOAD_FAST                'self'
              120  LOAD_METHOD              get_amount
              122  LOAD_FAST                'item'
              124  LOAD_STR                 'fraction'
              126  CALL_METHOD_2         2  ''
              128  CALL_METHOD_1         1  ''

 L.2375       130  BINARY_MULTIPLY  

 L.2374       132  INPLACE_ADD      
              134  STORE_FAST               'E'
            136_0  COME_FROM            84  '84'
              136  POP_BLOCK        
              138  JUMP_BACK            22  'to 22'
            140_0  COME_FROM_FINALLY    26  '26'

 L.2381       140  DUP_TOP          
              142  LOAD_GLOBAL              ValueError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   162  'to 162'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L.2382       154  POP_EXCEPT       
              156  JUMP_BACK            22  'to 22'
              158  POP_EXCEPT       
              160  JUMP_BACK            22  'to 22'
            162_0  COME_FROM           146  '146'
              162  END_FINALLY      
              164  JUMP_BACK            22  'to 22'

 L.2384       166  LOAD_FAST                'E'
              168  LOAD_METHOD              to
              170  LOAD_STR                 'J'
              172  CALL_METHOD_1         1  ''
              174  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 158

    def get_lattice_distance(self, solute):
        r"""
        Calculate the average distance between molecules

        Calculate the average distance between molecules of the given solute,
        assuming that the molecules are uniformly distributed throughout the
        solution.

        Parameters
        ----------
        solute : str
                    String representing the name of the solute of interest

        Returns
        -------
        Quantity : The average distance between solute molecules

        Examples
        --------
        >>> soln = Solution([['Na+','0.5 mol/kg'],['Cl-','0.5 mol/kg']])
        >>> soln.get_lattice_distance('Na+')
        1.492964.... nanometer

        Notes
        -----
        The lattice distance is related to the molar concentration as follows:

        .. math:: d = ( C_i N_A ) ^ {-{1\over3}}

        """
        distance = (self.get_amount(solute, 'mol/L') * unit.N_A) ** (-0.3333333333333333)
        return distance.to('nm')

    def _update_volume(self):
        """
        Recalculate the solution volume based on composition

        """
        self.volume = self._get_solvent_volume() + self._get_solute_volume()

    def _get_solvent_volume(self):
        """
        Return the volume of the pure solvent

        """
        solvent_vol = self.get_solvent_mass() / h2o.water_density(self.get_temperature(), self.get_pressure())
        return solvent_vol.to('L')

    def _get_solute_volume(self):
        """
        Return the volume of only the solutes

        """
        temperature = str(self.get_temperature())
        Salt = self.get_salt()
        db.search_parameters(Salt.formula)
        solute_vol = 0 * unit('L')
        pitzer_calc = False
        if db.has_parameter(Salt.formula, 'pitzer_parameters_volume'):
            param = db.get_parameter(Salt.formula, 'pitzer_parameters_volume')
            molality = (self.get_amount(Salt.cation, 'mol/kg') + self.get_amount(Salt.anion, 'mol/kg')) / 2
            if Salt.nu_cation >= 2:
                if Salt.nu_anion >= 2:
                    if Salt.nu_cation >= 3 or Salt.nu_anion >= 3:
                        alpha1 = 2
                        alpha2 = 50
                else:
                    alpha1 = 1.4
                    alpha2 = 12
            else:
                alpha1 = 2
                alpha2 = 0
            apparent_vol = ac.get_apparent_volume_pitzer(self.get_ionic_strength(), molality, alpha1, alpha2, param.get_value()[0], param.get_value()[1], param.get_value()[2], param.get_value()[3], param.get_value()[4], Salt.z_cation, Salt.z_anion, Salt.nu_cation, Salt.nu_anion, temperature)
            solute_vol += apparent_vol * (self.get_amount(Salt.cation, 'mol') / Salt.nu_cation + self.get_amount(Salt.anion, 'mol') / Salt.nu_anion) / 2
            pitzer_calc = True
            logger.info('Updated solution volume using Pitzer model for solute %s' % Salt.formula)
        for item in self.components:
            solute = self.get_solute(item)
            if item in ('H2O', 'HOH'):
                pass
            elif pitzer_calc is True and item in (Salt.anion, Salt.cation):
                pass
            elif db.has_parameter(item, 'partial_molar_volume'):
                solute_vol += solute.get_parameter('partial_molar_volume') * solute.get_moles()
                logger.info('Updated solution volume using direct partial molar volume for solute %s' % item)
            else:
                logger.warning('Partial molar volume data not available for solute %s. Solution volume will not be corrected.' % item)
        else:
            return solute_vol.to('L')

    def copy(self):
        """Return a copy of the solution

        TODO - clarify whether this is a deep or shallow copy
        """
        new_temperature = str(self.get_temperature())
        new_pressure = str(self.pressure)
        new_solvent = self.solvent_name
        new_solvent_mass = str(self.get_solvent_mass())
        new_solutes = []
        for item in self.components:
            if item == self.solvent_name:
                pass
            else:
                new_solutes.append([item, str(self.get_amount(item, 'mol'))])
        else:
            return Solution(new_solutes,
              solvent=[
             new_solvent, new_solvent_mass],
              temperature=new_temperature,
              pressure=new_pressure)

    def list_solutes(self):
        """
        List all the solutes in the solution.

        """
        return list(self.components.keys())

    def list_concentrations(self, unit='mol/kg', decimals=4, type='all'):
        """
        List the concentration of each species in a solution.

        Parameters
        ----------
        unit: str
            String representing the desired concentration unit.
        decimals: int
            The number of decimal places to display. Defaults to 4.
        type     : str
            The type of component to be sorted. Defaults to 'all' for all
            solutes. Other valid arguments are 'cations' and 'anions' which
            return lists of cations and anions, respectively.

        Returns
        -------
        dict
            Dictionary containing a list of the species in solution paired with their amount in the specified units

        """
        result_list = []
        if type == 'all':
            print('Component Concentrations:\n')
            print('========================\n')
            for item in self.components:
                amount = self.get_amount(item, unit)
                result_list.append([item, amount])
                print(item + ':' + '\t {0:0.{decimals}f~}'.format(amount, decimals=decimals))

        else:
            if type == 'cations':
                print('Cation Concentrations:\n')
                print('========================\n')
                for item in self.components:
                    if self.components[item].get_formal_charge() > 0:
                        amount = self.get_amount(item, unit)
                        result_list.append([item, amount])
                        print(item + ':' + '\t {0:0.{decimals}f~}'.format(amount, decimals=decimals))

            else:
                if type == 'anions':
                    print('Anion Concentrations:\n')
                    print('========================\n')
                    for item in self.components:
                        if self.components[item].get_formal_charge() < 0:
                            amount = self.get_amount(item, unit)
                            result_list.append([item, amount])
                            print(item + ':' + '\t {0:0.{decimals}f~}'.format(amount, decimals=decimals))

                return result_list

    def list_salts(self, unit='mol/kg', decimals=4):
        list = salt.generate_salt_list(self, unit)
        for item in list:
            print(item.formula + '\t {:0.{decimals}f}'.format((list[item]), decimals=decimals))

    def list_activities(self, decimals=4):
        """
        List the activity of each species in a solution.

        Parameters
        ----------
        decimals: int
            The number of decimal places to display. Defaults to 4.

        Returns
        -------
        dict
            Dictionary containing a list of the species in solution paired with their activity

        """
        print('Component Activities:\n')
        print('=====================\n')
        for i in self.components.keys():
            print(i + ':' + '\t {0.magnitude:0.{decimals}f}'.format((self.get_activity(i)),
              decimals=decimals))

    def __str__(self):
        str1 = 'Volume: {0:.3f~}\n'.format(self.get_volume())
        str2 = 'Pressure: {0:.3f~}\n'.format(self.get_pressure())
        str3 = 'Temperature: {0:.3f~}\n'.format(self.get_temperature())
        str4 = 'Components: {0:}\n'.format(self.list_solutes())
        return str1 + str2 + str3 + str4