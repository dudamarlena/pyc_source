# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/functions.py
# Compiled at: 2020-04-22 01:14:26
# Size of source mod 2**32: 18893 bytes
"""
pyEQL functions that take Solution objects as inputs or return Solution objects

:copyright: 2013-2020 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""
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
        else:
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
        else:
            return (unit.R * temperature.to('K') * (term_list[blend] - term_list[concentrate] - term_list[dilute])).to('J')


def donnan_eql(solution, fixed_charge):
    r"""
    Return a solution object in equilibrium with fixed_charge

    Parameters
    ----------
    Solution : Solution object
        The external solution to be brought into equilibrium with the fixed
        charges
    fixed_charge : str quantity
        String representing the concentration of fixed charges, including sign.
        May be specified in mol/L or mol/kg units. e.g. '1 mol/kg'

    Returns
    -------
    Solution
        A solution that has established Donnan equilibrium with the external
        (input) Solution

    Notes
    -----

    The general equation representing the equilibrium between an external
    electrolyte solution and an ion-exchange medium containing fixed charges
    is:[#]_

    .. math:: {a_- \over \bar a_-}^{1 \over z_-} {\bar a_+ \over a_+}^{1 \over z_+}     = exp({\Delta \pi \bar V \over {RT z_+ \nu_+}})

    Where subscripts :math:`+` and :math:`-` indicate the cation and anion, respectively,
    the overbar indicates the membrane phase,
    :math:`a` represents activity, :math:`z` represents charge, :math:`\nu` represents the stoichiometric
    coefficient, :math:`V` represents the partial molar volume of the salt, and
    :math:`\Delta \pi` is the difference in osmotic pressure between the membrane and the
    solution phase.

    In addition, electroneutrality must prevail within the membrane phase:

    .. math:: \bar C_+ z_+ + \bar X + \bar C_- z_- = 0

    Where :math:`C` represents concentration and :math:`X` is the fixed charge concentration
    in the membrane or ion exchange phase.

    This function solves these two equations simultaneously to arrive at the
    concentrations of the cation and anion in the membrane phase. It returns
    a solution equal to the input solution except that the concentrations of
    the predominant cation and anion have been adjusted according to this
    equilibrium.

    NOTE that this treatment is only capable of equilibrating a single salt.
    This salt is identified by the get_salt() method.

    References
    ----------

    .. [#] Strathmann, Heiner, ed. *Membrane Science and Technology* vol. 9, 2004.            Chapter 2, p. 51. http://dx.doi.org/10.1016/S0927-5193(04)80033-0

    Examples
    --------
    TODO

    See Also
    --------
    get_salt

    """
    salt = solution.get_salt()
    fixed_charge = unit(fixed_charge)
    conc_cation_soln = solution.get_amount(salt.cation, str(fixed_charge.units))
    conc_anion_soln = solution.get_amount(salt.anion, str(fixed_charge.units))
    act_cation_soln = solution.get_activity(salt.cation)
    act_anion_soln = solution.get_activity(salt.anion)
    z_cation = salt.z_cation
    z_anion = salt.z_anion
    nu_cation = salt.nu_cation
    if db.has_parameter(salt.formula, 'partial_molar_volume'):
        item = db.get_parameter(salt.formula, 'partial_molar_volume')
        molar_volume = item.get_value()
    else:
        if db.has_parameter(salt.cation, 'partial_molar_volume') and db.has_parameter(salt.anion, 'partial_molar_volume'):
            cation_vol = solution.get_solute(salt.cation).get_parameter('partial_molar_volume')
            anion_vol = solution.get_solute(salt.anion).get_parameter('partial_molar_volume')
            molar_volume = cation_vol + anion_vol
        else:
            logger.error('Required partial molar volume information not available. Aborting.')
            return
    donnan_soln = solution.copy()
    if conc_cation_soln.magnitude == 0 or conc_anion_soln.magnitude == 0:
        return donnan_soln
    exp_term = (molar_volume / (unit.R * solution.get_temperature() * z_cation * nu_cation)).to('1/Pa').magnitude

    def donnan_solve(x):
        if fixed_charge.magnitude >= 0:
            conc_cation_mem = x / abs(z_cation)
            conc_anion_mem = -(conc_cation_mem * z_cation + fixed_charge.magnitude) / z_anion
        else:
            if fixed_charge.magnitude < 0:
                conc_anion_mem = x / abs(z_anion)
                conc_cation_mem = -(conc_anion_mem * z_anion + fixed_charge.magnitude) / z_cation
        units = str(fixed_charge.units)
        donnan_soln.set_amount(salt.cation, str(conc_cation_mem) + units)
        donnan_soln.set_amount(salt.anion, str(conc_anion_mem) + units)
        act_cation_mem = donnan_soln.get_activity(salt.cation)
        act_anion_mem = donnan_soln.get_activity(salt.anion)
        delta_pi = donnan_soln.get_osmotic_pressure().magnitude - solution.get_osmotic_pressure().magnitude
        return (act_cation_mem / act_cation_soln) ** (1 / z_cation) * (act_anion_soln / act_anion_mem) ** (1 / z_anion) - math.exp(delta_pi * exp_term)

    from scipy.optimize import brentq
    if fixed_charge.magnitude > 0:
        x = conc_cation_soln.magnitude
        brentq(donnan_solve, 1e-10, x, xtol=0.001)
    else:
        if fixed_charge.magnitude < 0:
            x = conc_anion_soln.magnitude
            brentq(donnan_solve, 1e-10, x, xtol=0.001)
        else:
            return donnan_soln


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
    else:
        for item in Solution2.components:
            if item in mix_species:
                new_amt = str(unit(mix_species[item]) + Solution2.get_amount(item, 'mol'))
                mix_species.update({item: new_amt})
            else:
                mix_species.update({item: Solution2.get_amount(item, 'mol')})
        else:
            Blend = pyEQL.Solution(temperature=blend_temperature, pressure=blend_pressure)
            for item in mix_species.keys():
                if item in Blend.components:
                    Blend.set_amount(item, mix_species[item])
                else:
                    Blend.add_solute(item, mix_species[item])
            else:
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
    else:
        if solution == 'seawater' or solution == 'SW':
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
        else:
            if solution == 'rainwater':
                temperature = '25 degC'
                pressure = '1 atm'
                pH = 6
                solutes = [['HCO3-', '10^-5.5 mol/L'], ['CO3-2', '10^-9 mol/L']]
            else:
                if solution == 'wastewater' or solution == 'WW':
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
                else:
                    if solution == 'urine':
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
                    else:
                        if solution == 'normal saline' or solution == 'NS':
                            temperature = '25 degC'
                            pressure = '1 atm'
                            pH = 7
                            solutes = [['Na+', '154 mmol/L'], ['Cl-', '154 mmol/L']]
                        else:
                            if solution == 'Ringers lactate' or solution == 'RL':
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