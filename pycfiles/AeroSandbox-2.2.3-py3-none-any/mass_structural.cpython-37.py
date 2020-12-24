# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\mass_structural.py
# Compiled at: 2020-04-13 14:27:09
# Size of source mod 2**32: 12157 bytes


def mass_hpa_wing(span, chord, vehicle_mass, n_ribs, n_wing_sections=1, ultimate_load_factor=1.75, type='cantilevered', t_over_c=0.128, include_spar=True):
    """
    Finds the mass of the wing structure of a human powered aircraft (HPA), following Juan Cruz's correlations in
    http://journals.sfu.ca/ts/index.php/ts/article/viewFile/760/718
    :param span: wing span [m]
    :param chord: wing mean chord [m]
    :param vehicle_mass: aircraft gross weight [kg]
    :param n_ribs: number of ribs in the wing
    :param n_wing_sections: number of wing sections or panels (for disassembly?)
    :param ultimate_load_factor: ultimate load factor [unitless]
    :param type: Type of bracing: "cantilevered", "one-wire", "multi-wire"
    :param t_over_c: wing airfoil thickness-to-chord ratio
    :param include_spar: Should we include the mass of the spar? Useful if you want to do your own primary structure calculations. [boolean]
    :return: Wing structure mass [kg]
    """
    if include_spar:
        if type == 'cantilevered':
            mass_primary_spar = (span * 0.117 + span ** 2 * 0.011) * (1 + (ultimate_load_factor * vehicle_mass / 100 - 2) / 4)
        elif type == 'one-wire':
            mass_primary_spar = (span * 0.031 + span ** 2 * 0.00756) * (1 + (ultimate_load_factor * vehicle_mass / 100 - 2) / 4)
        elif type == 'multi-wire':
            mass_primary_spar = (span * 0.135 + span ** 2 * 0.00168) * (1 + (ultimate_load_factor * vehicle_mass / 100 - 2) / 4)
        else:
            raise ValueError("Bad input for 'type'!")
        mass_primary = mass_primary_spar * 1.2342282752488558
    else:
        mass_primary = 0
    ratio_of_rib_spacing_to_chord = span / n_ribs / chord
    n_end_ribs = 2 * n_wing_sections - 2
    area = span * chord
    W_wr = n_ribs * (chord ** 2 * t_over_c * 0.055 + chord * 0.00191)
    W_wer = n_end_ribs * (chord ** 2 * t_over_c * 0.662 + chord * 0.00657)
    W_wLE = 0.456 * (span ** 2 * ratio_of_rib_spacing_to_chord ** 1.3333333333333333 / span)
    W_wTE = span * 0.0277
    W_wc = area * 0.0308
    mass_secondary = W_wr + W_wer + W_wLE + W_wTE + W_wc
    return mass_primary + mass_secondary


def mass_wing_spar(span, mass_supported, ultimate_load_factor=1.75, n_booms=1):
    r"""
    Finds the mass of the spar for a wing on a single- or multi-boom lightweight aircraft. Model originally designed for solar aircraft.
    Data was fit to the range 30 < wing_span < 90 [m] and 50 < supported_mass < 800 [kg], but validity should extend somewhat beyond that.
    Extremely accurate fits within this range; R^2 > 0.99 for all fits.
    Source: AeroSandbox\studies\MultiBoomSparMass
    Assumptions:
        * Rectangular lift distribution (close enough, slightly conservative w.r.t. elliptical)
        * Constraint that local wing dihedral/anhedral angle must not exceed 10 degrees anywhere.
        * If multi-boom, assumes static-aerostructurally-optimal placement of the outer booms.
    :param span: Wing span [m]
    :param mass_supported: Total mass of all fuselages + tails
    :param ultimate_load_factor: Design load factor. Default taken from Daedalus design.
    :param n_booms: Number of booms on the design. Can be 1, 2, or 3. Assumes optimal placement of the outer booms.
    :return:
    """
    if n_booms == 1:
        c = 0.0082116578817492
        m = 0.3380385531034899
        n = 1.650021011836785
    elif n_booms == 2:
        c = 0.0038966832809997
        m = 0.3472862388655697
        n = 1.622223150903495
    elif n_booms == 3:
        c = 0.0059175282654185
        m = 0.3807869156408368
        n = 1.3862788430962647
    else:
        raise ValueError('Bad value of n_booms!')
    return c * (mass_supported * ultimate_load_factor) ** m * span ** n


def mass_hpa_stabilizer(span, chord, dynamic_pressure_at_manuever_speed, n_ribs, t_over_c=0.128, include_spar=True):
    """
    Finds the mass of a stabilizer structure of a human powered aircraft (HPA), following Juan Cruz's correlations in
    http://journals.sfu.ca/ts/index.php/ts/article/viewFile/760/718
    Note: apply this once to BOTH the rudder and elevator!!!
    :param span: stabilizer span [m]
    :param chord: stabilizer mean chord [m]
    :param dynamic_pressure_at_manuever_speed: dynamic pressure at maneuvering speed [Pa]
    :param n_ribs: number of ribs in the wing
    :param t_over_c: wing airfoil thickness-to-chord ratio
    :param include_spar: Should we include the mass of the spar? Useful if you want to do your own primary structure calculations. [boolean]
    :return: Stabilizer structure mass [kg]
    """
    area = span * chord
    q = dynamic_pressure_at_manuever_speed
    if include_spar:
        W_tss = (span * 0.0415 + span ** 2 * 0.00391) * (1 + (q * area / 78.5 - 1) / 2)
        mass_primary = W_tss
    else:
        mass_primary = 0
    ratio_of_rib_spacing_to_chord = span / n_ribs / chord
    W_tsr = n_ribs * (chord ** 2 * t_over_c * 0.116 + chord * 0.00401)
    W_tsLE = 0.174 * (area ** 2 * ratio_of_rib_spacing_to_chord ** 1.3333333333333333 / span)
    W_tsc = area * 0.0193
    mass_secondary = W_tsr + W_tsLE + W_tsc
    correction_factor = 1.1031616372329087
    return (mass_primary + mass_secondary) * correction_factor


def mass_hpa_tail_boom(length_tail_boom, dynamic_pressure_at_manuever_speed, mean_tail_surface_area):
    """
    Finds the mass of a tail boom structure of a human powered aircraft (HPA), following Juan Cruz's correlations in
    http://journals.sfu.ca/ts/index.php/ts/article/viewFile/760/718
    Assumes a tubular tail boom of high modules (E > 228 GPa) graphite/epoxy
    :param length_tail_boom: length of the tail boom [m]. Calculated as distance from the wing 1/4 chord to the furthest tail surface.
    :param dynamic_pressure_at_manuever_speed: dynamic pressure at maneuvering speed [Pa]
    :param mean_tail_surface_area: mean of the areas of the tail surfaces (elevator, rudder)
    :return: mass of the tail boom [m]
    """
    l = length_tail_boom
    q = dynamic_pressure_at_manuever_speed
    area = mean_tail_surface_area
    w_tb = (l * 0.114 + l ** 2 * 0.0196) * (1 + (q * area / 78.5 - 1) / 2)
    return w_tb


def mass_surface_balsa_monokote_cf(chord, span, mean_t_over_c=0.08):
    """
    Estimates the mass of a lifting surface constructed with balsa-monokote-carbon-fiber construction techniques.
    Warning: Not well validated; spar sizing is a guessed scaling and not based on structural analysis.
    :param chord: wing mean chord [m]
    :param span: wing span [m]
    :param mean_t_over_c: wing thickness-to-chord ratio [unitless]
    :return: estimated surface mass [kg]
    """
    mean_t = chord * mean_t_over_c
    monokote_mass = 0.061 * chord * span * 2
    rib_density = 200
    rib_spacing = 0.1
    rib_width = 0.003
    ribs_mass = mean_t * chord * rib_width * rib_density * (span / rib_spacing)
    spar_mass_1_inch = 0.2113 * span * 1.5
    spar_mass = spar_mass_1_inch * (mean_t / 0.0254) ** 2
    return (monokote_mass + ribs_mass + spar_mass) * 1.2


def mass_surface_solid(chord, span, density=2700, mean_t_over_c=0.08):
    """
    Estimates the mass of a lifting surface constructed out of a solid piece of material.
    Warning: Not well validated; spar sizing is a guessed scaling and not based on structural analysis.
    :param chord: wing mean chord [m]
    :param span: wing span [m]
    :param mean_t_over_c: wing thickness-to-chord ratio [unitless]
    :return: estimated surface mass [kg]
    """
    mean_t = chord * mean_t_over_c
    volume = chord * span * mean_t
    return density * volume


if __name__ == '__main__':
    import casadi as cas, numpy as np
    import matplotlib.pyplot as plt
    print('Daedalus wing, estimated mass: %f' % mass_hpa_wing(span=34,
      chord=0.902,
      vehicle_mass=104.1,
      n_ribs=100,
      n_wing_sections=5,
      type='one-wire'))
    print('Daedalus wing, actual mass: %f' % 18.9854)
    nr = np.linspace(1, 400, 401)
    m = mass_hpa_wing(span=34,
      chord=0.902,
      vehicle_mass=104.1,
      n_ribs=nr,
      n_wing_sections=5,
      type='one-wire')
    plt.plot(nr, m)
    plt.ylim([15, 20])
    plt.grid(True)
    plt.xlabel('Number of ribs')
    plt.ylabel('Wing mass [kg]')
    plt.title('Daedalus Wing Rib Count Optimization Test')
    plt.show()
    opti = cas.Opti()
    nr_opt = opti.variable()
    opti.set_initial(nr_opt, 100)
    opti.minimize(mass_hpa_wing(span=34,
      chord=0.902,
      vehicle_mass=104.1,
      n_ribs=nr_opt,
      n_wing_sections=5,
      type='one-wire'))
    opti.solver('ipopt')
    sol = opti.solve()
    print('Optimal number of ribs: %f' % sol.value(nr_opt))
    print('Daedalus elevator, estimated mass: %f' % mass_hpa_stabilizer(span=4.26,
      chord=0.6,
      dynamic_pressure_at_manuever_speed=30.012500000000003,
      n_ribs=20))
    span = 34
    mass_total = 104.1
    mass_wing_primary_cruz = mass_hpa_wing(span=span,
      chord=0.902,
      vehicle_mass=mass_total,
      n_ribs=(sol.value(nr_opt)),
      n_wing_sections=1,
      type='cantilevered') - mass_hpa_wing(span=span,
      chord=0.902,
      vehicle_mass=mass_total,
      n_ribs=(sol.value(nr_opt)),
      n_wing_sections=1,
      type='cantilevered',
      include_spar=False)
    mass_wing_primary_physics = mass_wing_spar(span=span,
      mass_supported=mass_total)