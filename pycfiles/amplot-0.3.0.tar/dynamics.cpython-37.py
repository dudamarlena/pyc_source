# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/dynamics.py
# Compiled at: 2020-04-24 08:45:30
# Size of source mod 2**32: 11387 bytes
import tensorflow as tf
import amplitf.interface as atfi
import amplitf.kinematics as atfk

@atfi.function
def helicity_amplitude(x, spin):
    """
    Helicity amplitude for a resonance in scalar-scalar state
      x    : cos(helicity angle)
      spin : spin of the resonance
    """
    if spin == 0:
        return atfi.complex(atfi.const(1.0), atfi.const(0.0))
    if spin == 1:
        return atfi.complex(x, atfi.const(0.0))
    if spin == 2:
        return atfi.complex((3.0 * x ** 2 - 1.0) / 2.0, atfi.const(0.0))
    if spin == 3:
        return atfi.complex((5.0 * x ** 3 - 3.0 * x) / 2.0, atfi.const(0.0))
    if spin == 4:
        return atfi.complex((35.0 * x ** 4 - 30.0 * x ** 2 + 3.0) / 8.0, atfi.const(0.0))


@atfi.function
def relativistic_breit_wigner(m2, mres, wres):
    """
    Relativistic Breit-Wigner 
    """
    if wres.dtype is atfi.ctype():
        return tf.math.reciprocal(atfi.cast_complex(mres * mres - m2) - atfi.complex(atfi.const(0.0), mres) * wres)
    if wres.dtype is atfi.fptype():
        return tf.math.divide(atfi.complex(mres * wres, atfi.const(0.0)), atfi.complex(mres * mres - m2, -mres * wres))


@atfi.function
def blatt_weisskopf_ff(q, q0, d, l):
    """
    Blatt-Weisskopf formfactor for intermediate resonance
    """
    z = q * d
    z0 = q0 * d

    def hankel1(x):
        if l == 0:
            return Const(1.0)
        if l == 1:
            return 1 + x * x
        if l == 2:
            x2 = x * x
            return 9 + x2 * (3.0 + x2)
        if l == 3:
            x2 = x * x
            return 225 + x2 * (45 + x2 * (6 + x2))
        if l == 4:
            x2 = x * x
            return 11025.0 + x2 * (1575.0 + x2 * (135.0 + x2 * (10.0 + x2)))

    return atfi.sqrt(hankel1(z0) / hankel1(z))


@atfi.function
def mass_dependent_width(m, m0, gamma0, p, p0, ff, l):
    """
    mass-dependent width for BW amplitude
    """
    if l == 0:
        return gamma0 * (p / p0) * (m0 / m) * (ff * ff)
    if l == 1:
        return gamma0 * (p / p0) ** 3 * (m0 / m) * (ff * ff)
    if l == 2:
        return gamma0 * (p / p0) ** 5 * (m0 / m) * (ff * ff)
    if l >= 3:
        return gamma0 * (p / p0) ** (2 * l + 1) * (m0 / m) * ff ** 2


@atfi.function
def orbital_barrier_factor(p, p0, l):
    """
    Orbital barrier factor
    """
    if l == 0:
        return atfi.ones(p)
    if l == 1:
        return p / p0
    if l >= 2:
        return (p / p0) ** l


@atfi.function
def breit_wigner_lineshape(m2, m0, gamma0, ma, mb, mc, md, dr, dd, lr, ld, barrier_factor=True, ma0=None, md0=None):
    """
    Breit-Wigner amplitude with Blatt-Weisskopf formfactors, mass-dependent width and orbital barriers
    """
    m = atfi.sqrt(m2)
    q = atfk.two_body_momentum(md, m, mc)
    q0 = atfk.two_body_momentum(md if md0 is None else md0, m0, mc)
    p = atfk.two_body_momentum(m, ma, mb)
    p0 = atfk.two_body_momentum(m0, ma if ma0 is None else ma0, mb)
    ffr = blatt_weisskopf_ff(p, p0, dr, lr)
    ffd = blatt_weisskopf_ff(q, q0, dd, ld)
    width = mass_dependent_width(m, m0, gamma0, p, p0, ffr, lr)
    bw = relativistic_breit_wigner(m2, m0, width)
    ff = ffr * ffd
    if barrier_factor:
        b1 = orbital_barrier_factor(p, p0, lr)
        b2 = orbital_barrier_factor(q, q0, ld)
        ff *= b1 * b2
    return bw * atfi.complex(ff, atfi.const(0.0))


@atfi.function
def subthreshold_breit_wigner_lineshape(m2, m0, gamma0, ma, mb, mc, md, dr, dd, lr, ld, barrier_factor=True):
    """
    Breit-Wigner amplitude (with the mass under kinematic threshold) 
    with Blatt-Weisskopf formfactors, mass-dependent width and orbital barriers
    """
    m = atfi.sqrt(m2)
    mmin = ma + mb
    mmax = md - mc
    tanhterm = atfi.tanh((m0 - (mmin + mmax) / 2.0) / (mmax - mmin))
    m0eff = mmin + (mmax - mmin) * (1.0 + tanhterm) / 2.0
    q = atfk.two_body_momentum(md, m, mc)
    q0 = atfk.two_body_momentum(md, m0eff, mc)
    p = atfk.two_body_momentum(m, ma, mb)
    p0 = atfk.two_body_momentum(m0eff, ma, mb)
    ffr = blatt_weisskopf_ff(p, p0, dr, lr)
    ffd = blatt_weisskopf_ff(q, q0, dd, ld)
    width = mass_dependent_width(m, m0, gamma0, p, p0, ffr, lr)
    bw = relativistic_breit_wigner(m2, m0, width)
    ff = ffr * ffd
    if barrier_factor:
        b1 = orbital_barrier_factor(p, p0, lr)
        b2 = orbital_barrier_factor(q, q0, ld)
        ff *= b1 * b2
    return bw * atfi.complex(ff, atfi.const(0.0))


@atfi.function
def exponential_nonresonant_lineshape(m2, m0, alpha, ma, mb, mc, md, lr, ld, barrierFactor=True):
    """
    Exponential nonresonant amplitude with orbital barriers
    """
    if barrierFactor:
        m = atfi.sqrt(m2)
        q = atfk.two_body_momentum(md, m, mc)
        q0 = atfk.two_body_momentum(md, m0, mc)
        p = atfk.two_body_momentum(m, ma, mb)
        p0 = atfk.two_body_momentum(m0, ma, mb)
        b1 = orbital_barrier_factor(p, p0, lr)
        b2 = orbital_barrier_factor(q, q0, ld)
        return atfi.complex(b1 * b2 * atfi.exp(-alpha * (m2 - m0 ** 2)), atfi.const(0.0))
    return atfi.complex(atfi.exp(-alpha * (m2 - m0 ** 2)), atfi.const(0.0))


@atfi.function
def polynomial_nonresonant_lineshape(m2, m0, coeffs, ma, mb, mc, md, lr, ld, barrierFactor=True):
    """
    2nd order polynomial nonresonant amplitude with orbital barriers
    coeffs: list of atfi.complex polynomial coefficients [a0, a1, a2]
    """

    def poly(x, cs):
        return cs[0] + cs[1] * atfi.complex(x, atfi.const(0.0)) + cs[2] * atfi.complex(x ** 2, atfi.const(0.0))

    if barrierFactor:
        m = atfi.sqrt(m2)
        q = atfk.two_body_momentum(md, m, mc)
        q0 = atfk.two_body_momentum(md, m0, mc)
        p = atfk.two_body_momentum(m, ma, mb)
        p0 = atfk.two_body_momentum(m0, ma, mb)
        b1 = orbital_barrier_factor(p, p0, lr)
        b2 = orbital_barrier_factor(q, q0, ld)
        return poly(m - m0, coeffs) * atfi.complex(b1 * b2, atfi.const(0.0))
    return poly(m - m0, coeffs)


@atfi.function
def gounaris_sakurai_lineshape(s, m, gamma, m_pi):
    """
      Gounaris-Sakurai shape for rho->pipi
        s     : squared pipi inv. mass
        m     : rho mass
        gamma : rho width
        m_pi  : pion mass
    """
    m2 = m * m
    m_pi2 = m_pi * m_pi
    ss = atfi.sqrt(s)
    ppi2 = (s - 4.0 * m_pi2) / 4.0
    p02 = (m2 - 4.0 * m_pi2) / 4.0
    p0 = atfi.sqrt(p02)
    ppi = atfi.sqrt(ppi2)
    hs = 2.0 * ppi / atfi.pi() / ss * atfi.log((ss + 2.0 * ppi) / 2.0 / m_pi)
    hm = 2.0 * p0 / atfi.pi() / m * atfi.log((m + 2.0 * ppi) / 2.0 / m_pi)
    dhdq = hm * (0.125 / p02 - 0.5 / m2) + 0.5 / atfi.pi() / m2
    f = gamma * m2 / p0 ** 3 * (ppi2 * (hs - hm) - p02 * (s - m2) * dhdq)
    gamma_s = gamma * m2 * ppi ** 3 / s / p0 ** 3
    dr = m2 - s + f
    di = ss * gamma_s
    r = dr / (dr ** 2 + di ** 2)
    i = di / (dr ** 2 + di ** 2)
    return atfi.complex(r, i)


@atfi.function
def flatte_lineshape(s, m, g1, g2, ma1, mb1, ma2, mb2):
    """
      Flatte line shape
        s : squared inv. mass
        m : resonance mass
        g1 : coupling to ma1, mb1
        g2 : coupling to ma2, mb2
    """
    mab = atfi.sqrt(s)
    pab1 = atfk.two_body_momentum(mab, ma1, mb1)
    rho1 = 2.0 * pab1 / mab
    pab2 = atfk.complex_two_body_momentum(mab, ma2, mb2)
    rho2 = 2.0 * pab2 / atfi.cast_complex(mab)
    gamma = (atfi.cast_complex(g1 ** 2 * rho1) + atfi.cast_complex(g2 ** 2) * rho2) / atfi.cast_complex(m)
    return relativistic_breit_wigner(s, m, gamma)


@atfi.function
def special_flatte_lineshape(m2, m0, gamma0, ma, mb, mc, md, dr, dd, lr, ld, barrier_factor=True):
    """
    Flatte amplitude with Blatt-Weisskopf formfactors, 2 component mass-dependent width and orbital barriers as done in Pentaquark analysis for L(1405) that peaks below pK threshold.
    ma = [ma1, ma2] and mb = [mb1, mb2]
    NB: The dominant decay for a given resonance should be the 2nd channel i.e. R -> a2 b2. 
    This is because (as done in pentaquark analysis) in calculating p0 (used in Blatt-Weisskopf FF) for both channels, the dominant decay is used.
    Another assumption made in pentaquark is equal couplings ie. gamma0_1 = gamma0_2 = gamma and only differ in phase space factors 
    """
    ma1, ma2 = ma[0], ma[1]
    mb1, mb2 = mb[0], mb[1]
    m = atfi.sqrt(m2)
    q = atfk.two_body_momentum(md, m, mc)
    q0 = atfk.two_body_momentum(md, m0, mc)
    ffd = blatt_weisskopf_ff(q, q0, dd, ld)
    p_1 = atfk.two_body_momentum(m, ma1, mb1)
    p0_1 = atfk.two_body_momentum(m0, ma1, mb1)
    ffr_1 = blatt_weisskopf_ff(p_1, p0_1, dr, lr)
    p_2 = atfk.two_body_momentum(m, ma2, mb2)
    p0_2 = atfk.two_body_momentum(m0, ma2, mb2)
    ffr_2 = blatt_weisskopf_ff(p_2, p0_2, dr, lr)
    width_1 = mass_dependent_width(m, m0, gamma0, p_1, p0_2, blatt_weisskopf_ff(p_1, p0_2, dr, lr), lr)
    width_2 = mass_dependent_width(m, m0, gamma0, p_2, p0_2, ffr_2, lr)
    width = width_1 + width_2
    bw = relativistic_breit_wigner(m2, m0, width)
    ff = ffr_1 * ffd
    if barrier_factor:
        b1 = orbital_barrier_factor(p_1, p0_1, lr)
        b2 = orbital_barrier_factor(q, q0, ld)
        ff *= b1 * b2
    return bw * atfi.complex(ff, atfi.const(0.0))


@atfi.function
def nonresonant_lass_lineshape(m2ab, a, r, ma, mb):
    """
      LASS line shape, nonresonant part
    """
    m = atfi.sqrt(m2ab)
    q = atfk.two_body_momentum(m, ma, mb)
    cot_deltab = 1.0 / a / q + 0.5 * r * q
    ampl = atfi.cast_complex(m) / atfi.complex(q * cot_deltab, -q)
    return ampl


@atfi.function
def resonant_lass_lineshape(m2ab, m0, gamma0, a, r, ma, mb):
    """
      LASS line shape, resonant part
    """
    m = atfi.sqrt(m2ab)
    q0 = atfk.two_body_momentum(m0, ma, mb)
    q = atfk.two_body_momentum(m, ma, mb)
    cot_deltab = 1.0 / a / q + 0.5 * r * q
    phase = atfi.atan(1.0 / cot_deltab)
    width = gamma0 * q / m * m0 / q0
    ampl = relativistic_breit_wigner(m2ab, m0, width) * atfi.complex(atfi.cos(phase), atfi.sin(phase)) * atfi.cast_complex(m2ab * gamma0 / q0)
    return ampl


@atfi.function
def dabba_lineshape(m2ab, b, alpha, beta, ma, mb):
    """
      Dabba line shape
    """
    mSum = ma + mb
    m2a = ma ** 2
    m2b = mb ** 2
    sAdler = max(m2a, m2b) - 0.5 * min(m2a, m2b)
    mSum2 = mSum * mSum
    mDiff = m2ab - mSum2
    rho = atfi.sqrt(1.0 - mSum2 / m2ab)
    realPart = 1.0 - beta * mDiff
    imagPart = b * atfi.exp(-alpha * mDiff) * (m2ab - sAdler) * rho
    denomFactor = realPart * realPart + imagPart * imagPart
    ampl = atfi.complex(realPart, imagPart) / atfi.cast_complex(denomFactor)
    return ampl