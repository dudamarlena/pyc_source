# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/core/manning.py
# Compiled at: 2020-05-11 12:58:14
# Size of source mod 2**32: 26389 bytes
"""
Manning's counter-ion condensation theory for thermodynamics of ions
in charged membranes.
"""
import warnings, math
from membrane_toolkit.core.unitized import ureg

def manning_eql(solution, xi, fixed_charge):
    """
    Return a solution object in equilibrium with fixed_charge, according
    to Manning's Counter-ion Condensation theory

    Args:
        xi : float
            Number representing the Manning parameter, dimensionless.
        fixed_charge : str quantity
            String representing the concentration of fixed charges, including sign.
            Must be specified in mol/L of water absorbed by the membrane
        solution : Solution object
            The external solution to be brought into equilibrium with the fixed
            charges

    Returns:
        Solution : A solution that has established Donnan-Manning equilibrium with the
            external (input) Solution

    Notes:
        See XXXX

    References:
        J. Kamcev, M. Galizia, F.M. Benedetti, E.-S. Jang, D.R. Paul,
        B. Freeman, et al., Partitioning of Mobile Ions Between Ion Exchange
        Polymers and Aqueous Salt Solutions: Importance of Counter-ion
        Condensation, Phys. Chem. Chem. Phys. (2016). doi:10.1039/C5CP06747B.

        G.S. Manning, Limiting Laws and Counterion Condensation in
        Polyelectrolyte Solutions I. Colligative Properties, J. Chem.
        Phys. 51 (1969) 924–933. doi:10.1063/1.1672157.
    """
    salt = solution.get_salt()
    fixed_charge = ureg(fixed_charge)
    manning_soln = solution.copy()
    if fixed_charge.magnitude >= 0:
        formula_counter = salt.anion
        formula_co = salt.cation
        conc_counter = solution.get_amount(salt.anion, str(fixed_charge.units))
        conc_co = solution.get_amount(salt.cation, str(fixed_charge.units))
        z_counter = salt.z_anion
        z_co = salt.z_cation
        nu_counter = salt.nu_anion
        nu_co = salt.nu_cation
    else:
        if fixed_charge.magnitude <= 0:
            formula_counter = salt.cation
            formula_co = salt.anion
            conc_counter = solution.get_amount(salt.cation, str(fixed_charge.units))
            conc_co = solution.get_amount(salt.anion, str(fixed_charge.units))
            z_counter = salt.z_cation
            z_co = salt.z_anion
            nu_counter = salt.nu_cation
            nu_co = salt.nu_anion
        else:
            warnings.warn('Fixed charge concentration is zero, Donnan equilibrium cannot be              established. Returning a copy of the bulk solution.')
            return manning_soln
    if conc_counter.magnitude == 0 or conc_co.magnitude == 0:
        return manning_soln
    Cfix = abs(fixed_charge.magnitude)
    zfix = fixed_charge.magnitude / Cfix
    RHS = solution.get_activity(formula_counter) ** nu_counter * solution.get_activity(formula_co) ** nu_co

    def manning_solve(Cc):
        gamma_mean = get_activity_coefficient_manning(xi, Cfix * zfix, Cc, 'mean', nu_counter, nu_co, z_counter, z_co)
        LHS = Cc ** nu_co * ((-z_co * Cc - zfix * Cfix) / z_counter) ** nu_counter * gamma_mean ** (nu_counter + nu_co)
        return LHS - RHS

    from scipy.optimize import brentq
    result_co = brentq(manning_solve, 1e-10, (2 * conc_co.magnitude), xtol=1e-06)
    result_counter = -(result_co * z_co + zfix * Cfix) / z_counter
    units = str(fixed_charge.units)
    manning_soln.set_amount(formula_counter, str(result_counter) + units)
    manning_soln.set_amount(formula_co, str(result_co) + units)
    return manning_soln


def get_activity_coefficient_manning(xi: float, C_fix: float, Cs: float, type: str='mean', nu_counter: int=1, nu_co: int=1, z_counter: int=1, z_co: int=-1):
    r"""
    Return an ion activity coefficient inside a charged polymer,
    according to Manning theory

    Args:
        xi:
            Number representing the Manning parameter for the polymer,
            dimensionless.
        C_fix:
            Number representing the concentration of fixed charges, including sign.
            Must be specified in mol/L of water absorbed by the polymer. Note that
            monovalent charged groups are assumed.
        Cs:
            Number representing the concentraiton of mobile salt inside the
            polymer. Must be specified in mol/L of water absorbed by the polymer.
        type:
            Specifies whether the counter-ion, co-ion, or the mean ionic activity
            coefficient is returned. Valid arguments are 'counter', 'co', and
            'mean'. Defaults to 'mean' if not specified.
        nu_counter:
            Stoichiometric coefficient of the counter-ion in the parent salt. Defaults to 1 if not specified.
        nu_co : int
            Stoichiometric coefficient of the co-ion in the parent salt. Defaults to -1 if not specified.
        z_counter:
            Net charge, including sign, of the counter-ion. Defaults to +1 if not specified. Note that the sign of
            z_counter must be opposite to the sign of C_fix.
        z_co:
            Net charge, including sign, of the co-ion. Defaults to -1 if not specified. Note that the sign of
            z_co must be the same as the sign of C_fix.

    Returns:
        float: the mean or individual ion activity coefficient inside the polymer.

    Notes:
        When \( \xi \gt \frac{1}{|z_{ct}|} \), ion activity coefficients are given by:

        $$
            \bar \gamma_{ct} = \frac{\frac{X}{\xi |z_{ct}|} + \nu_{ct} |z_{ct}|}{X + \nu_{ct} |z_{ct}|}
            exp [-\frac{\frac{X}{2}}{X+\xi |z_{co} z_{ct}| ( \nu_{co} + \nu_{ct})}]
        $$

        and

        $$
            \bar \gamma_{co} = exp [-\frac{\frac{X z_{co}^2}{2 z_{ct}^2}}{X+\xi |z_{co} z_{ct}|
            ( \nu_{co} + \nu_{ct})}]
        $$

        and if \( \xi \lt \frac{1}{|z_{ct}|} \), by

        $$
            \bar \gamma_{ct} = exp [-\frac{\xi \frac{X}{2}}{(X |z_{ct}| +
            (\nu_{co} z_{co}^2 + \nu_{ct} z_{ct}^2)} z_{ct}^2]
        $$

        and

        $$
        \bar \gamma_{co} = exp [-\frac{\xi \frac{X}{2}}{(X |z_{ct}| + (\nu_{co} z_{co}^2 +
        \bar \nu_{ct} z_{ct}^2)} z_{co}^2]
        $$

        where

        $$
        X = \frac{\bar C_{co}}{\bar C_{fix}}
        $$

        \(\bar \gamma\) are activity coefficients, \( \bar C_{fix} \) is the fixed charge concentration
        (including sign), \( \xi \) is the Manning parameter, \( \bar C_{co} \) is the co-ion concentration
        in the membrane, and subscripts \(co\) and \(ct\) refer to the co-ion and counter-ion, respectively,
        and overbars indicate membrane-phase quantities.

        The mean activity coefficient is given by

        $$
        \bar \gamma_\pm = (\gamma_{ct}^{\nu_{ct}} \gamma_{co}^{\nu_{co}})^{\frac{1}{\nu_{ct} + \nu_{co}}}
        $$

    References:
        J. Kamcev, M. Galizia, F.M. Benedetti, E.-S. Jang, D.R. Paul,
        B. Freeman, et al., Partitioning of Mobile Ions Between Ion Exchange
        Polymers and Aqueous Salt Solutions: Importance of Counter-ion
        Condensation, Phys. Chem. Chem. Phys. (2016). doi:10.1039/C5CP06747B.

        Kamcev, J.; Paul, D. R.; Freeman, B. D. Ion Activity Coefficients in
        Ion Exchange Polymers: Applicability of Manning’s Counterion Condensation
        Theory. Macromolecules 2015, 48 (21), 8011–8024.

        Manning, G. S. Limiting Laws and Counterion Condensation in
        Polyelectrolyte Solutions I. Colligative Properties. J. Chem. Phys.
        1969, 51 (3), 924–933.
    """
    if C_fix < 0:
        raise z_counter > 0 and z_co < 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and co-ion. Aborting.')
    else:
        if C_fix >= 0:
            raise z_counter < 0 and z_co > 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and co-ion. Aborting.')
        else:
            if z_counter * nu_counter != -1 * z_co * nu_co:
                raise Exception('Error in input stoichiometry. z_counter * n_counter != | z_co * nu_co |. Aborting.')
            X = abs(C_fix / Cs)
            xi_critical = 1 / abs(z_counter)
            if xi >= xi_critical:
                gamma_counter = (X / abs(z_counter) / xi + abs(z_counter) * nu_counter) / (X + abs(z_counter) * nu_counter) * math.exp(-(X / 2) / (X + abs(z_co * z_counter) * xi * (nu_co + nu_counter)))
                gamma_co = math.exp(-(X / 2 * (z_co / z_counter) ** 2) / (X + abs(z_co * z_counter) * xi * (nu_co + nu_counter)))
            else:
                if xi < xi_critical:
                    common_factor = -(xi * X / 2) / (X * abs(z_counter) + (nu_counter * z_counter ** 2 + nu_co * z_co ** 2))
                    gamma_counter = math.exp(common_factor * z_counter ** 2)
                    gamma_co = math.exp(common_factor * z_co ** 2)
        if type == 'counter':
            return gamma_counter
        if type == 'co':
            return gamma_co
        if type == 'mean':
            return (gamma_counter ** nu_counter * gamma_co ** nu_co) ** (1 / (nu_counter + nu_co))
        raise Exception("Invalid 'type' argument. Enter 'counter'', 'co', or 'mean'")


def diffusion_coefficient_manning(xi: float, C_fix: float, Cs: float, vol_frac: float, type: str='counter', nu_counter: int=1, nu_co: int=1, z_counter: int=1, z_co: int=-1):
    r"""
    Return a diffusion coefficient inside a charged polymer,
    according to Manning theory

    Args:
        xi:
            Number representing the Manning parameter for the polymer,
            dimensionless.
        C_fix:
            Number representing the concentration of fixed charges, including sign.
            Must be specified in mol/L of water absorbed by the polymer. Note that
            monovalent charged groups are assumed.
        Cs:
            Number representing the concentraiton of mobile salt inside the polymer.
            Must be specified in mol/L of water absorbed by the polymer.
        vol_frac:
            The volume fraction of water sorbed by the ion exchange membrane.
        xi:
            Number representing the Manning parameter for the polymer,
            dimensionless.
        C_fix:
            Number representing the concentration of fixed charges, including sign.
            Must be specified in mol/L of water absorbed by the polymer. Note that
            monovalent charged groups are assumed.
        Cs:
            Number representing the concentraiton of mobile salt inside the
            polymer. Must be specified in mol/L of water absorbed by the polymer.
        type::
            Specifies whether the counter-ion, co-ion, or the mean diffusion
            coefficient is returned. Valid arguments are 'counter', 'co'. 'mean' is not currently implemented.
            Defaults to 'counter' if not specified.
        nu_counter:
            Stoichiometric coefficient of the counter-ion in the parent salt. Defaults to 1 if not specified.
        nu_co : int
            Stoichiometric coefficient of the co-ion in the parent salt. Defaults to -1 if not specified.
        z_counter:
            Net charge, including sign, of the counter-ion. Defaults to +1 if not specified. Note that the sign of
            z_counter must be opposite to the sign of C_fix.
        z_co:
            Net charge, including sign, of the co-ion. Defaults to -1 if not specified. Note that the sign of
            z_co must be the same as the sign of C_fix.

    Returns:
        float: The mean or individual ion diffusion coefficient inside the polymer, normalized
            by the ion diffusion coefficient in bulk solution (D_mem / D_bulk).

    Notes:
        When \( \xi \gt \frac{1}{|z_{ct}|} \), the counter-ion diffusion coefficient is given by:

        $$
            \frac{\bar D_{ct}}{D_{ct}} = \bigg( \frac{\frac{X}{z_{ct}^2 \nu_{ct} \xi} + 1}
            {\frac{X}{|z_{ct}| \nu_{ct}} + 1} \bigg) \bigg( 1 - \frac{1}{3} z_{ct}^2 A(\frac{1}{|z_{ct}|},
            \frac{X}{|z_{ct}| \xi}\bigg) \bigg( \frac{\phi_w}{2 - \phi_w} \bigg)^2
        $$

        otherwise, when \( \xi \lt \frac{1}{|z_{ct}|} \):

        $$
            \frac{\bar D_{ct}}{D_{ct}} = \bigg( 1 - \frac{1}{3} z_{ct}^2 A(\frac{1}{|z_{ct}|},
            \frac{X}{|z_{ct}| \xi}\bigg) \bigg( \frac{\phi_w}{2 - \phi_w} \bigg)^2
        $$

        In either case, co-ion diffusion coefficient is given by

        $$
            \frac{\bar D_{co}}{D_{co}} = \bigg( 1 - \frac{1}{3} z_{co}^2 A(\frac{1}{|z_{ct}|},
            \frac{X}{|z_{ct}| \xi}\bigg) \bigg( \frac{\phi_w}{2 - \phi_w} \bigg)^2
        $$

        where

        $$
            A = \sum_{m_1} \sum_{m_2} \bigg [ \pi |z_{ct}|(m_1^2+m_2^2)+|z_{ct}|+ \frac{(\nu_{ct}
            + \nu_{co})|z_{ct} z_{co}||z_{ct}| \xi}{X} \bigg]^{-2}
        $$

        $$
        X = \frac{\bar C_{co}}{\bar C_{fix}}
        $$

        \(\bar D\) are diffusion coefficients, \( \bar C_{fix} \) is the fixed charge concentration (including sign),
        \( \xi \) is the Manning parameter, \( \bar C_{co} \) is the co-ion concentration in the membrane,
        and subscripts \(co\) and \(ct\) refer to the co-ion and counter-ion, respectively, and overbars indicate
        membrane-phase quantities.

        The mean salt diffusion coefficient is given by

        $$
        \bar D_s = \frac{\bar D_{ct} \bar D_{co} (z_{ct}^2 \bar C_{ct} + z_{co}^2 \bar C_{co} )}
        {z_{ct}^2 \bar D_{ct} \bar C_{ct} + z_{co}^2 \bar D_{co} \bar C_{co} }
        $$

    References:
        Kamcev, J.; Paul, D. R.; Manning, G. S.; Freeman, B. D. Predicting Salt Permeability Coefficients
        in Highly Swollen, Highly Charged Ion Exchange Membranes. ACS Appl. Mater. Interfaces 2017, 9 (4), 4044–4056.

        Kamcev, Jovan, Paul, Donald R., Manning, Gerald S., Freeman, B. D. Ion Diffusion Coefficients in
        Ion Exchange Membranes: Significance of Counter-Ion Condensation. Macromolecules 2018, 51 (15), 5519–5529.

        Manning, G. S. Limiting Laws and Counterion Condensation in Polyelectrolyte Solutions II.
        Self‐ Diffusion of the Small Ions. J. Chem. Phys. 1969, 51 (3), 934–938.
    """
    if C_fix < 0:
        raise z_counter > 0 and z_co < 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and co-ion. Aborting.')
    else:
        if C_fix >= 0:
            raise z_counter < 0 and z_co > 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and co-ion. Aborting.')
        else:
            X = abs(C_fix / Cs)
            xi_critical = 1 / abs(z_counter)
            if xi >= xi_critical:
                A = _A((1 / abs(z_counter)),
                  (X / xi / abs(z_counter)),
                  nu_counter=nu_counter,
                  nu_co=nu_co,
                  z_counter=z_counter,
                  z_co=z_co)
                D_counter = (X / (z_counter ** 2 * nu_counter * xi) + 1) / (X / (abs(z_counter) * nu_counter) + 1) * (1 - 0.3333333333333333 * z_counter ** 2 * A) * (vol_frac / (2 - vol_frac)) ** 2
            else:
                if xi < xi_critical:
                    A = _A(xi,
                      X, nu_counter=nu_counter, nu_co=nu_co, z_counter=z_counter, z_co=z_co)
                    D_counter = (1 - 0.3333333333333333 * z_counter ** 2 * A) * (vol_frac / (2 - vol_frac)) ** 2
        D_co = (1 - 0.3333333333333333 * z_co ** 2 * A) * (vol_frac / (2 - vol_frac)) ** 2
        if type == 'counter':
            return D_counter
        if type == 'co':
            return D_co
        raise Exception('Invalid "type" argument. Enter "counter" or "co"')


def _A(x, y, nu_counter=1, nu_co=1, z_counter=1, z_co=-1):
    r"""
    Calculate the function 'A' required for determining diffusion coefficients
    according to Manning's counter-ion condensation theory

    Args:
        x: float, y: float
        nu_counter, nu_co : int, optional
            Stoichiometric coefficients of the counter-ion and co-ion in the parent
            salt. Defautls to 1 if not specified.
        z_counter, z_co : int, optional
            Net charge, including sign, of the counter-ion and co-ion in the parent
            salt. Defaults to +1 and -1 if not specified. Note that the sign of
            z_counter must be opposite to the sign of fixed_charge, while the sign
            of z_co must match that of fixed_Charge.

    Returns:
        float: The mean or individual ion diffusion coefficient inside the polymer.

    Notes:
        The function A(x,y) is given by [#]_ [#]_ [#]_

        $$
            \sum_{m1} \sum_{m2} [ \frac{\pi}{x} (m_1^2+m_2^2)+|z_g|+ \frac{(\nu_g + \nu_c)|z_g z_c|}{y}]^-2
        $$

        When $\xi$ is greater than the critical value, $x=\frac{1}{|z_g|}$ and $y=\frac{X}{\xi |z_g|}$.
        If $\xi$ is lower than the critical value (counter-ion condensation does not occur), then
        $x=\xi$ and $y=X$.

    References:
        Kamcev, J.; Paul, D. R.; Manning, G. S.; Freeman, B. D. Predicting Salt
        Permeability Coefficients in Highly Swollen, Highly Charged Ion Exchange Membranes.
        ACS Appl. Mater. Interfaces 2017, acsami.6b14902.

        Y. Ji, H. Luo, G.M. Geise, Specific co-ion sorption and diffusion properties
        influence membrane permselectivity, J. Membr. Sci. 563 (2018) 492–504.
        doi:10.1016/j.memsci.2018.06.010.

        Fan, H.; Yip, N. Y. Elucidating Conductivity-Permselectivity Tradeoffs
        in Electrodialysis and Reverse Electrodialysis by Structure-Property Analysis
        of Ion-Exchange Membranes. J. Membr. Sci. 2018.

    """
    n = int(50)
    A = 0
    for i in range(-n, n):
        for j in range(-n, n):
            if i == 0 and j == 0:
                pass
            else:
                A += (math.pi / x * (i ** 2 + j ** 2) + abs(z_counter) + (nu_counter + nu_co) * abs(z_counter * z_co) / y) ** (-2)
        else:
            return A


def beta(xi, fixed_charge, C_counter, Cs, type, nu_counter=1, nu_co=1, z_counter=1, z_co=-1):
    r"""
    Return an ion activity coefficient inside a charged polymer,
    according to Manning theory

    Args:
        xi : float
            Number representing the Manning parameter for the polymer, dimensionless.
        fixed_charge : str quantity
            String representing the concentration of fixed charges, including sign.
            Must be specified in mol/L of water absorbed by the polymer. Note that
            monovalent charged groups are assumed.
        C_counter : str quantity
            String representing the counter-ion concentration inside the polymer.
            Must be specified in mol/L of water absorbed by the polymer.
        Cs : str quantity
            String representing the concentraiton of mobile salt inside the polymer.
            Must be specified in mol/L of water absorbed by the polymer.
        type : str, optional :
            Specifies whether the counter-ion, co-ion, or the mean ionic activity
            coefficient is returned. Valid arguments are 'counter' or 'co'.
        nu_counter: int, nu_co : int, optional
            Stoichiometric coefficients of the counter-ion and co-ion in the parent
            salt. Defautls to 1 if not specified.
        z_counter: int, z_co : int, optional
            Net charge, including sign, of the counter-ion and co-ion in the parent
            salt. Defaults to +1 and -1 if not specified. Note that the sign of
            z_counter must be opposite to the sign of fixed_charge, while the sign
            of z_co must match that of fixed_Charge.

    Returns:
        float: The thermodynamic factor.

    Notes:
        When the Manning parameter is greater than the critical value, the
        thermodynamic factors are given by

        TODO update
        $$
            \gamma_+ \gamma_- = [{{X \over \xi} + 1 \over X +1] exp [{-X \ over X + 2 \xi}]
        $$

        and when the Manning Parameter is less than the critical value, by [#]_

        TODO update
    """
    if ureg(fixed_charge).magnitude < 0:
        raise z_counter > 0 and z_co < 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and                 co-ion. Aborting.')
    else:
        if ureg(fixed_charge).magnitude >= 0:
            raise z_counter < 0 and z_co > 0 or Exception('Mismatch between signs of fixed charge, counter-ion, and                 co-ion. Aborting.')
        else:
            xi_critical = 1 / abs(z_counter)
            if xi >= xi_critical:
                if type == 'counter':
                    beta_counter = 1 + ureg(fixed_charge) * (1 - 1 / abs(z_counter) / xi) / (ureg(fixed_charge) / abs(z_counter) / xi + abs(z_counter) * nu_counter * ureg(Cs)) + (nu_counter + nu_co) * abs(z_counter) * xi * ureg(fixed_charge) * ureg(C_counter) / (2 * (ureg(fixed_charge) + abs(z_counter) * nu_counter * (nu_counter + nu_co) * xi * ureg(Cs)) ** 2)
                    return beta_counter.magnitude
                if type == 'co':
                    beta_co = 1 + 0.5 * (z_co / z_counter) ** 2 * abs(z_counter) * nu_counter * (nu_co + nu_counter) * xi * ureg(fixed_charge) * ureg(Cs) / (ureg(fixed_charge) + abs(z_counter) * nu_counter * (nu_co + nu_counter) * xi * ureg(Cs)) ** 2
                    return beta_co.magnitude
                raise Exception('Invalid "type" argument. Enter "counter", "co",                 or "mean"')
            else:
                if xi < xi_critical:
                    raise Exception('Cannot calculate beta when Manning parameter is below             critical value')
                    return