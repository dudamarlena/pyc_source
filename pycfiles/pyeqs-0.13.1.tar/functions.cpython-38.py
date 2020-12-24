# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/functions.py
# Compiled at: 2020-04-22 01:14:26
# Size of source mod 2**32: 18893 bytes
__doc__ = '\npyEQL functions that take Solution objects as inputs or return Solution objects\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
import math, pyEQL
from pyEQL import paramsDB as db
from pyEQL import unit
from pyEQL.logging_system import Unique
import logging
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def gibbs_mix(Solution1, Solution2):
    r"""
    Return the Gibbs energy change associated with mixing two solutions.

    Parameters
    ----------
    Solution1, Solution2 : Solution objects
        The two solutions to be mixed.

    Returns
    -------
    Quantity
        The change in Gibbs energy associated with complete mixing of the
        Solutions, in Joules.

    Notes
    -----

    The Gibbs energy of mixing is calculated as follows: [#]_

    .. math:: 
    
        \Delta_{mix} G = \sum_i (n_c + n_d) R T \ln a_b - \sum_i n_c R T \ln a_c - \sum_i n_d R T \ln a_d

    Where :math:`n` is the number of moles of substance, :math:`T` is the temperature in kelvin,
    and  subscripts :math:`b`, :math:`c`, and :math:`d` refer to the concentrated, dilute, and blended
    Solutions, respectively.

    Note that dissociated ions must be counted as separate components,
    so a simple salt dissolved in water is a three component solution (cation,
    anion, and water).

    References
    ----------

    .. [#] Koga, Yoshikata, 2007. *Solution Thermodynamics and its Application to Aqueous Solutions:            A differential approach.* Elsevier, 2007, pp. 23-37.

    Examples
    --------

    """
    concentrate = Solution1
    dilute = Solution2
    blend = mix(Solution1, Solution2)
    term_list = {concentrate: 0, dilute: 0, blend: 0}
    temperature = blend.get_temperature()
    for solution in term_list:
        for solute in solution.components:
            if not solution.get_amount(solute, 'fraction') == 0:
                term_list[solution] += solution.get_amount(solute, 'mol') * math.log(solution.get_activity(solute))

        return (unit.R * temperature.to('K') * (term_list[blend] - term_list[concentrate] - term_list[dilute])).to('J')


def entropy_mix(Solution1, Solution2):
    r"""
    Return the ideal mixing entropy associated with mixing two solutions

    Parameters
    ----------
    Solution1, Solution2 : Solution objects
        The two solutions to be mixed.

    Returns
    -------
    Quantity
        The ideal mixing entropy associated with complete mixing of the
        Solutions, in Joules.

    Notes
    -----

    The ideal entropy of mixing is calculated as follows:[#]_

    .. math::

        \Delta_{mix} S = \sum_i (n_c + n_d) R T \ln x_b - \sum_i n_c R T \ln x_c - \sum_i n_d R T \ln x_d

    Where :math:`n` is the number of moles of substance, :math:`T` is the temperature in kelvin,
    and  subscripts :math:`b`, :math:`c`, and :math:`d` refer to the concentrated, dilute, and blended
    Solutions, respectively.

    Note that dissociated ions must be counted as separate components,
    so a simple salt dissolved in water is a three component solution (cation,
    anion, and water).

    References
    ----------

    .. [#] Koga, Yoshikata, 2007. *Solution Thermodynamics and its Application to Aqueous Solutions:            A differential approach.* Elsevier, 2007, pp. 23-37.

    Examples
    --------

    """
    concentrate = Solution1
    dilute = Solution2
    blend = mix(Solution1, Solution2)
    term_list = {concentrate: 0, dilute: 0, blend: 0}
    temperature = blend.get_temperature()
    for solution in term_list:
        for solute in solution.components:
            if not solution.get_amount(solute, 'fraction') == 0:
                term_list[solution] += solution.get_amount(solute, 'mol') * math.log(solution.get_amount(solute, 'fraction'))

        return (unit.R * temperature.to('K') * (term_list[blend] - term_list[concentrate] - term_list[dilute])).to('J')


def donnan_eql--- This code section failed: ---

 L. 239         0  LOAD_DEREF               'solution'
                2  LOAD_METHOD              get_salt
                4  CALL_METHOD_0         0  ''
                6  STORE_DEREF              'salt'

 L. 242         8  LOAD_GLOBAL              unit
               10  LOAD_DEREF               'fixed_charge'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_DEREF              'fixed_charge'

 L. 245        16  LOAD_DEREF               'solution'
               18  LOAD_METHOD              get_amount
               20  LOAD_DEREF               'salt'
               22  LOAD_ATTR                cation
               24  LOAD_GLOBAL              str
               26  LOAD_DEREF               'fixed_charge'
               28  LOAD_ATTR                units
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'conc_cation_soln'

 L. 246        36  LOAD_DEREF               'solution'
               38  LOAD_METHOD              get_amount
               40  LOAD_DEREF               'salt'
               42  LOAD_ATTR                anion
               44  LOAD_GLOBAL              str
               46  LOAD_DEREF               'fixed_charge'
               48  LOAD_ATTR                units
               50  CALL_FUNCTION_1       1  ''
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'conc_anion_soln'

 L. 247        56  LOAD_DEREF               'solution'
               58  LOAD_METHOD              get_activity
               60  LOAD_DEREF               'salt'
               62  LOAD_ATTR                cation
               64  CALL_METHOD_1         1  ''
               66  STORE_DEREF              'act_cation_soln'

 L. 248        68  LOAD_DEREF               'solution'
               70  LOAD_METHOD              get_activity
               72  LOAD_DEREF               'salt'
               74  LOAD_ATTR                anion
               76  CALL_METHOD_1         1  ''
               78  STORE_DEREF              'act_anion_soln'

 L. 249        80  LOAD_DEREF               'salt'
               82  LOAD_ATTR                z_cation
               84  STORE_DEREF              'z_cation'

 L. 250        86  LOAD_DEREF               'salt'
               88  LOAD_ATTR                z_anion
               90  STORE_DEREF              'z_anion'

 L. 251        92  LOAD_DEREF               'salt'
               94  LOAD_ATTR                nu_cation
               96  STORE_FAST               'nu_cation'

 L. 255        98  LOAD_GLOBAL              db
              100  LOAD_METHOD              has_parameter
              102  LOAD_DEREF               'salt'
              104  LOAD_ATTR                formula
              106  LOAD_STR                 'partial_molar_volume'
              108  CALL_METHOD_2         2  ''
              110  POP_JUMP_IF_FALSE   136  'to 136'

 L. 256       112  LOAD_GLOBAL              db
              114  LOAD_METHOD              get_parameter
              116  LOAD_DEREF               'salt'
              118  LOAD_ATTR                formula
              120  LOAD_STR                 'partial_molar_volume'
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'item'

 L. 257       126  LOAD_FAST                'item'
              128  LOAD_METHOD              get_value
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'molar_volume'
              134  JUMP_FORWARD        224  'to 224'
            136_0  COME_FROM           110  '110'

 L. 258       136  LOAD_GLOBAL              db
              138  LOAD_METHOD              has_parameter
              140  LOAD_DEREF               'salt'
              142  LOAD_ATTR                cation
              144  LOAD_STR                 'partial_molar_volume'
              146  CALL_METHOD_2         2  ''
              148  POP_JUMP_IF_FALSE   210  'to 210'
              150  LOAD_GLOBAL              db
              152  LOAD_METHOD              has_parameter

 L. 259       154  LOAD_DEREF               'salt'
              156  LOAD_ATTR                anion

 L. 259       158  LOAD_STR                 'partial_molar_volume'

 L. 258       160  CALL_METHOD_2         2  ''
              162  POP_JUMP_IF_FALSE   210  'to 210'

 L. 261       164  LOAD_DEREF               'solution'
              166  LOAD_METHOD              get_solute
              168  LOAD_DEREF               'salt'
              170  LOAD_ATTR                cation
              172  CALL_METHOD_1         1  ''
              174  LOAD_METHOD              get_parameter

 L. 262       176  LOAD_STR                 'partial_molar_volume'

 L. 261       178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'cation_vol'

 L. 264       182  LOAD_DEREF               'solution'
              184  LOAD_METHOD              get_solute
              186  LOAD_DEREF               'salt'
              188  LOAD_ATTR                anion
              190  CALL_METHOD_1         1  ''
              192  LOAD_METHOD              get_parameter

 L. 265       194  LOAD_STR                 'partial_molar_volume'

 L. 264       196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'anion_vol'

 L. 267       200  LOAD_FAST                'cation_vol'
              202  LOAD_FAST                'anion_vol'
              204  BINARY_ADD       
              206  STORE_FAST               'molar_volume'
              208  JUMP_FORWARD        224  'to 224'
            210_0  COME_FROM           162  '162'
            210_1  COME_FROM           148  '148'

 L. 269       210  LOAD_GLOBAL              logger
              212  LOAD_METHOD              error

 L. 270       214  LOAD_STR                 'Required partial molar volume information not available. Aborting.'

 L. 269       216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 272       220  LOAD_CONST               None
              222  RETURN_VALUE     
            224_0  COME_FROM           208  '208'
            224_1  COME_FROM           134  '134'

 L. 276       224  LOAD_DEREF               'solution'
              226  LOAD_METHOD              copy
              228  CALL_METHOD_0         0  ''
              230  STORE_DEREF              'donnan_soln'

 L. 279       232  LOAD_FAST                'conc_cation_soln'
              234  LOAD_ATTR                magnitude
              236  LOAD_CONST               0
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_TRUE    254  'to 254'
              242  LOAD_FAST                'conc_anion_soln'
              244  LOAD_ATTR                magnitude
              246  LOAD_CONST               0
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   258  'to 258'
            254_0  COME_FROM           240  '240'

 L. 280       254  LOAD_DEREF               'donnan_soln'
              256  RETURN_VALUE     
            258_0  COME_FROM           250  '250'

 L. 288       258  LOAD_FAST                'molar_volume'
              260  LOAD_GLOBAL              unit
              262  LOAD_ATTR                R
              264  LOAD_DEREF               'solution'
              266  LOAD_METHOD              get_temperature
              268  CALL_METHOD_0         0  ''
              270  BINARY_MULTIPLY  
              272  LOAD_DEREF               'z_cation'
              274  BINARY_MULTIPLY  
              276  LOAD_FAST                'nu_cation'
              278  BINARY_MULTIPLY  
              280  BINARY_TRUE_DIVIDE
              282  LOAD_METHOD              to

 L. 289       284  LOAD_STR                 '1/Pa'

 L. 288       286  CALL_METHOD_1         1  ''
              288  LOAD_ATTR                magnitude

 L. 287       290  STORE_DEREF              'exp_term'

 L. 293       292  LOAD_CLOSURE             'act_anion_soln'
              294  LOAD_CLOSURE             'act_cation_soln'
              296  LOAD_CLOSURE             'donnan_soln'
              298  LOAD_CLOSURE             'exp_term'
              300  LOAD_CLOSURE             'fixed_charge'
              302  LOAD_CLOSURE             'salt'
              304  LOAD_CLOSURE             'solution'
              306  LOAD_CLOSURE             'z_anion'
              308  LOAD_CLOSURE             'z_cation'
              310  BUILD_TUPLE_9         9 
              312  LOAD_CODE                <code_object donnan_solve>
              314  LOAD_STR                 'donnan_eql.<locals>.donnan_solve'
              316  MAKE_FUNCTION_8          'closure'
              318  STORE_FAST               'donnan_solve'

 L. 336       320  LOAD_CONST               0
              322  LOAD_CONST               ('brentq',)
              324  IMPORT_NAME_ATTR         scipy.optimize
              326  IMPORT_FROM              brentq
              328  STORE_FAST               'brentq'
              330  POP_TOP          

 L. 343       332  LOAD_DEREF               'fixed_charge'
              334  LOAD_ATTR                magnitude
              336  LOAD_CONST               0
              338  COMPARE_OP               >
          340_342  POP_JUMP_IF_FALSE   368  'to 368'

 L. 344       344  LOAD_FAST                'conc_cation_soln'
              346  LOAD_ATTR                magnitude
              348  STORE_FAST               'x'

 L. 345       350  LOAD_FAST                'brentq'
              352  LOAD_FAST                'donnan_solve'
              354  LOAD_CONST               1e-10
              356  LOAD_FAST                'x'
              358  LOAD_CONST               0.001
              360  LOAD_CONST               ('xtol',)
              362  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              364  POP_TOP          
              366  JUMP_FORWARD        404  'to 404'
            368_0  COME_FROM           340  '340'

 L. 346       368  LOAD_DEREF               'fixed_charge'
              370  LOAD_ATTR                magnitude
              372  LOAD_CONST               0
              374  COMPARE_OP               <
          376_378  POP_JUMP_IF_FALSE   404  'to 404'

 L. 347       380  LOAD_FAST                'conc_anion_soln'
              382  LOAD_ATTR                magnitude
              384  STORE_FAST               'x'

 L. 348       386  LOAD_FAST                'brentq'
              388  LOAD_FAST                'donnan_solve'
              390  LOAD_CONST               1e-10
              392  LOAD_FAST                'x'
              394  LOAD_CONST               0.001
              396  LOAD_CONST               ('xtol',)
              398  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              400  POP_TOP          
              402  JUMP_FORWARD        404  'to 404'
            404_0  COME_FROM           402  '402'
            404_1  COME_FROM           376  '376'
            404_2  COME_FROM           366  '366'

 L. 353       404  LOAD_DEREF               'donnan_soln'
              406  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 406


def mix(Solution1, Solution2):
    """
    Mix two solutions together

    Returns a new Solution object that results from the mixing of Solution1
    and Solution2

    Parameters
    ----------
    Solution1, Solution2 : Solution objects
        The two solutions to be mixed.

    Returns
    -------
    Solution
        A Solution object representing the mixed solution.

    """
    if not Solution1.solvent_name == Solution2.solvent_name:
        logger.error('mix() function does not support solutions with different solvents. Aborting.')
    else:
        if not Solution1.solvent_name == 'H2O' or Solution1.solvent_name == 'water':
            logger.error('mix() function does not support non-water solvents. Aborting.')
        p1 = Solution1.get_pressure()
        t1 = Solution1.get_temperature()
        v1 = Solution1.get_volume()
        p2 = Solution2.get_pressure()
        t2 = Solution2.get_temperature()
        v2 = Solution2.get_volume()
        if not p1 == p2:
            logger.info('mix() function called between two solutions of different pressure. Pressures will be averaged (weighted by volume)')
        blend_pressure = str((p1 * v1 + p2 * v2) / (v1 + v2))
        t1 == t2 or logger.info('mix() function called between two solutions of different temperature. Temperatures will be averaged (weighted by volume)')
    blend_temperature = str((t1 * v1 + t2 * v2) / (v1 + v2))
    mix_species = {}
    for item in Solution1.components:
        mix_species.update({item: str(Solution1.get_amount(item, 'mol'))})

    for item in Solution2.components:
        if item in mix_species:
            new_amt = str(unit(mix_species[item]) + Solution2.get_amount(item, 'mol'))
            mix_species.update({item: new_amt})
        else:
            mix_species.update({item: Solution2.get_amount(item, 'mol')})

    Blend = pyEQL.Solution(temperature=blend_temperature, pressure=blend_pressure)
    for item in mix_species.keys():
        if item in Blend.components:
            Blend.set_amount(item, mix_species[item])
        else:
            Blend.add_solute(item, mix_species[item])

    return Blend


def autogenerate(solution=''):
    """
    This method provides a quick way to create Solution objects representing
    commonly-encountered solutions, such as seawater, rainwater, and wastewater.

    Parameters
    ----------
    solution : str
                String representing the desired solution
                Valid entries are 'seawater', 'rainwater',
                'wastewater',and 'urine'

    Returns
    -------
    Solution
        A pyEQL Solution object.

    Notes
    -----
    The following sections explain the different solution options:

    - '' - empty solution, equivalent to pyEQL.Solution()
    - 'rainwater' - pure water in equilibrium with atmospheric CO2 at pH 6
    - 'seawater' or 'SW'- Standard Seawater. See Table 4 of the Reference for Composition [#]_
    - 'wastewater' or 'WW' - medium strength domestic wastewater. See Table 3-18 of [#]_
    - 'urine' - typical human urine. See Table 3-15 of [#]_
    - 'normal saline' or 'NS' - normal saline solution used in medicine [#]_
    - 'Ringers lacatate' or 'RL' - Ringer's lactate solution used in medicine [#]_

    References
    ----------
    .. [#] Millero, Frank J. "The composition of Standard Seawater and the definition of            the Reference-Composition Salinity Scale." *Deep-sea Research. Part I* 55(1), 2008, 50-72.

    .. [#] Metcalf & Eddy, Inc. et al. *Wastewater Engineering: Treatment and Resource Recovery*, 5th Ed.             McGraw-Hill, 2013.

    .. [#] https://en.wikipedia.org/wiki/Saline_(medicine)

    .. [#] https://en.wikipedia.org/wiki/Ringer%27s_lactate_solution

    """
    if solution == '':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 7
        solutes = []
    elif solution == 'seawater' or solution == 'SW':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 8.1
        solutes = [
         [
          'Na+', '10.78145 g/kg'],
         [
          'Mg+2', '1.28372 g/kg'],
         [
          'Ca+2', '0.41208 g/kg'],
         [
          'K+', '0.39910 g/kg'],
         [
          'Sr+2', '0.00795 g/kg'],
         [
          'Cl-', '19.35271 g/kg'],
         [
          'SO4-2', '2.71235 g/kg'],
         [
          'HCO3-', '0.10481 g/kg'],
         [
          'Br-', '0.06728 g/kg'],
         [
          'CO3-2', '0.01434 g/kg'],
         [
          'B(OH)4', '0.00795 g/kg'],
         [
          'F-', '0.00130 g/kg'],
         [
          'OH-', '0.00014 g/kg'],
         [
          'B(OH)3', '0.01944 g/kg'],
         [
          'CO2', '0.00042 g/kg']]
    elif solution == 'rainwater':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 6
        solutes = [['HCO3-', '10^-5.5 mol/L'], ['CO3-2', '10^-9 mol/L']]
    elif solution == 'wastewater' or solution == 'WW':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 7
        solutes = [
         [
          'NH3', '24.3 mg/L'],
         [
          'PO4-3', '7.6 mg/L'],
         [
          'C6H12O6', '410 mg/L'],
         [
          'K+', '16 mg/L'],
         [
          'Cl-', '59 mg/L'],
         [
          'SO4-2', '26 mg/L']]
        logger.warning('Total organic carbon in wastewater is approximated as glucose')
    elif solution == 'urine':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 7
        solutes = [
         [
          'CON2H4', '20,000 mg/L'],
         [
          'C4H7N3O', '1,000 mg/L'],
         [
          'C5H4N4O3', '300 mg/L'],
         [
          'NH4+', '500 mg/L'],
         [
          'HCO3-', '300 mg/L'],
         [
          'NH4+', '500 mg/L'],
         [
          'Mg+2', '100 mg/L'],
         [
          'PO4-3', '1200 mg/L'],
         [
          'Na+', '6000 mg/L'],
         [
          'K+', '1500 mg/L'],
         [
          'Cl-', '1900 mg/L'],
         [
          'SO4-2', '1800 mg/L']]
    elif solution == 'normal saline' or solution == 'NS':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 7
        solutes = [['Na+', '154 mmol/L'], ['Cl-', '154 mmol/L']]
    elif solution == 'Ringers lactate' or solution == 'RL':
        temperature = '25 degC'
        pressure = '1 atm'
        pH = 6.5
        solutes = [
         [
          'Na+', '130 mmol/L'],
         [
          'Cl-', '109 mmol/L'],
         [
          'K+', '4 mmol/L'],
         [
          'Ca+2', '1.5 mmol/L'],
         [
          'C3H5O3-', '28 mmol/L']]
    else:
        logger.error('Invalid solution entered - %s' % solution)
        return
    sol = pyEQL.Solution(solutes, temperature=temperature, pressure=pressure, pH=pH)
    return sol