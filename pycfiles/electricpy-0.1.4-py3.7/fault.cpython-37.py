# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\electricpy\fault.py
# Compiled at: 2019-11-05 12:10:53
# Size of source mod 2**32: 57359 bytes
"""
---------------------
`electricpy.fault.py`
---------------------

Included Functions
------------------
- Single Line to Ground:                phs1g
- Double Line to Ground:                phs2g
- Line to Line:                         phs2
- Three-Phase Fault:                    phs3
- Single Pole Open:                     poleopen1
- Double Pole Open:                     poleopen2
- Simple MVA Calculator:                scMVA
- Three-Phase MVA Calculator:           phs3mvasc
- Single-Phase MVA Calculator:          phs1mvasc
- Faulted Bus Voltage:                  busvolt
- CT Saturation Function:               ct_saturation
- CT C-Class Calculator:                ct_cclass
- CT Sat. V at rated Burden:            ct_satratburden
- CT Voltage Peak Formula:              ct_vpeak
- CT Time to Saturation:                ct_timetosat
- Transient Recovery Voltage Calc.:     pktransrecvolt
- TRV Reduction Resistor:               trvresistor
- TOC Trip Time:                        toctriptime
- TOC Reset Time:                       tocreset
- Pickup Setting Assistant:             pickup
- Radial TOC Coordination Tool:         tdradial
- TAP Setting Calculator:               protectiontap
- Transformer Current Correction:       correctedcurrents
- Operate/Restraint Current Calc.:      iopirt
- Symmetrical/RMS Fault Current Calc:   symrmsfaultcur
- TOC Fault Current Ratio:              faultratio
- Residual Compensation Factor Calc:    residcomp
- Distance Elem. Impedance Calc:        distmeasz
- Transformer Mismatch Calculator:      transmismatch
- High-Impedance Voltage Pickup:        highzvpickup
- High-Impedance Minimum Current PU:    highzmini
- Instantaneous Overcurrent PU:         instoc
- Generator Loss of Field Settings:     genlossfield
- Thermal Time Limit Calculator:        thermaltime
"""
import numpy as _np
import scipy.optimize as _fsolve
from .constants import *

def _phaseroll(M012, reference):
    M = A012.dot(M012)
    reference = reference.upper()
    if reference == 'A':
        pass
    elif reference == 'B':
        M = _np.roll(M, 1, 0)
    else:
        if reference == 'C':
            M = _np.roll(M, 2, 0)
        else:
            raise ValueError('Invalid Phase Reference.')
    return M


def phs1g(Vth, Zseq, Rf=0, sequence=True, reference='A'):
    r"""
    Single-Phase-to-Ground Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a single-line-to-ground fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_0+Z_1+Z_2+3*R_f}
    
    .. math:: I_2 = I_1
    
    .. math:: I_0 = I_1
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Ifault:     list of complex,
                The Array of Fault Currents as (If0, If1, If2)
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    Ifault = Vth / (X0 + X1 + X2 + 3 * Rf)
    Ifault = _np.array([Ifault, Ifault, Ifault])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def phs2g(Vth, Zseq, Rf=0, sequence=True, reference='A'):
    r"""
    Double-Line-to-Ground Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a double-line-to-ground fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_1+\frac{Z_2*(Z_0+3*R_f)}{Z_0+Z_2+3*R_f}}
    
    .. math:: I_2 = -\frac{V_{th}-Z_1*I_1}{X_2}
    
    .. math:: I_0 = -\frac{V_{th}-Z_1*I_1}{X_0+3*R_f}
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Ifault:     list of complex,
                The Array of Fault Currents as (If0, If1, If2)
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    If1 = Vth / (X1 + X2 * (X0 + 3 * Rf) / (X0 + X2 + 3 * Rf))
    If2 = -(Vth - X1 * If1) / X2
    If0 = -(Vth - X1 * If1) / (X0 + 3 * Rf)
    Ifault = _np.array([If0, If1, If2])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def phs2(Vth, Zseq, Rf=0, sequence=True, reference='A'):
    r"""
    Line-to-Line Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a phase-to-phase fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_1+Z_2+R_f}
    
    .. math:: I_2 = -I_1
    
    .. math:: I_0 = 0
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Ifault:     list of complex,
                The Array of Fault Currents as (If0, If1, If2)
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    If0 = 0
    If1 = Vth / (X1 + X2 + Rf)
    If2 = -If1
    Ifault = _np.array([If0, If1, If2])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def phs3(Vth, Zseq, Rf=0, sequence=True, reference='A'):
    r"""
    Three-Phase Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a three-phase fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_1+R_1}
    
    .. math:: I_2 = 0
    
    .. math:: I_0 = 0
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Ifault:     list of complex
                The Fault Current, equal for 0, pos., and neg. seq.
    """
    X0, X1, X2 = Zseq
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    Ifault = Vth / (X1 + Rf)
    Ifault = _np.array([0, Ifault, 0])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def poleopen1(Vth, Zseq, sequence=True, reference='A'):
    r"""
    Single Pole Open Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a single pole open fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_1+(\frac{1}{Z_2}+\frac{1}{Z_0})^-1}
    
    .. math:: I_2 = -I_1 * \frac{Z_0}{Z_2+Z_0}
    
    .. math:: I_0 = -I_1 * \frac{Z_2}{Z_2+Z_0}
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference, or the
                faulted phase indicator; default='A'
    
    Returns
    -------
    Ifault:     list of complex,
                The Array of Fault Currents as (If0, If1, If2)
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    If1 = Vth / (X1 + (1 / X2 + 1 / X0) ** (-1))
    If2 = -If1 * X0 / (X2 + X0)
    If0 = -If1 * X2 / (X2 + X0)
    Ifault = _np.array([If0, If1, If2])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def poleopen2(Vth, Zseq, sequence=True, reference='A'):
    r"""
    Single Pole Open Fault Calculator
    
    This function will evaluate the Zero, Positive, and Negative
    sequence currents for a single pole open fault.
    
    .. math:: I_1 = \frac{V_{th}}{Z_1+Z_2+Z_0}
    
    .. math:: I_2 = I_1
    
    .. math:: I_0 = I_1
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference, or the
                faulted phase indicator; default='A'
    
    Returns
    -------
    Ifault:     list of complex,
                The Array of Fault Currents as (If0, If1, If2)
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    If1 = Vth / (X1 + X2 + X0)
    If2 = If1
    If0 = If1
    Ifault = _np.array([If0, If1, If2])
    if not sequence:
        Ifault = _phaseroll(Ifault, reference)
    return Ifault


def scMVA(Zth=None, Isc=None, Vth=1):
    """
    Simple Short-Circuit MVA Calculator
    
    Function defines a method of interpretively
    calculating the short-circuit MVA value
    given two of the three arguments. The formulas
    are all based around the following:
    
    .. math:: MVA_{sc} = V_{th}*I_{sc}
    
    .. math:: V_{th} = I_{sc}*Z_{th}
    
    Parameters
    ----------
    Zth:        float
                The Thevenin-Equivalent-Impedance
    Isc:        float, optional
                Short-Circuit-Current, if left as
                None, will force function to use
                default setting for Vth.
                default=None
    Vth:        float, optional
                The Thevenin-Equivalent-Voltage,
                defaults to a 1-per-unit value.
                default=1
    
    Returns
    -------
    MVA:        float
                Short-Circuit MVA, not described
                as three-phase or otherwise, such
                determination is dependent upon
                inputs.
    """
    if not any((Zth, Isc)):
        raise ValueError('Either Zth or Isc must be specified.')
    elif Zth is not None:
        Zth = abs(Zth)
    else:
        if Isc is not None:
            Isc = abs(Isc)
        if Vth != 1:
            Vth = abs(Vth)
        if all((Zth, Isc)):
            MVA = Isc ** 2 * Zth
        else:
            if all((Zth, Vth)):
                MVA = Vth ** 2 / Zth
            else:
                MVA = Vth * Isc
    return MVA


def phs3mvasc(Vth, Zseq, Rf=0, Sbase=1):
    r"""
    Three-Phase MVA Short-Circuit Calculator
    
    Calculator to evaluate the Short-Circuit MVA of a three-phase fault given the system
    parameters of Vth, Zseq, and an optional Rf. Uses the formula as follows:
    
    .. math:: MVA_{sc} = \frac{\left|V_{th}^2\right|}{|Z_1|} * Sbase
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    Sbase:      real, optional
                The per-unit base for power. default=1
    
    Returns
    -------
    MVA:        real
                Three-Phase Short-Circuit MVA.
    """
    MVA = abs(Vth) ** 2 / abs(Zseq[1]) * Sbase
    if Sbase != 1:
        MVA = MVA * 1e-06
    return MVA


def phs1mvasc(Vth, Zseq, Rf=0, Sbase=1):
    r"""
    Single-Phase MVA Short-Circuit Calculator
    
    Calculator to evaluate the Short-Circuit MVA of a single-phase fault given the system
    parameters of Vth, Zseq, and an optional Rf. Uses the formula as follows:
    
    .. math:: MVA_{sc} = \left|I_1^2\right|*|Z_1| * Sbase
    
    where:
    
    .. math:: I_1 = \frac{V_{th}}{Z_0+Z_1+Z_2+3*R_f}
    
    Parameters
    ----------
    Vth:        complex
                The Thevenin-Equivalent-Voltage
    Zseq:       list of complex
                Tupple of sequence reactances as (Z0, Z1, Z2)
    Rf:         complex, optional
                The fault resistance, default=0
    Sbase:      real, optional
                The per-unit base for power. default=1
    
    Returns
    -------
    MVA:        real
                Single-Phase Short-Circuit MVA.
    """
    X0, X1, X2 = Zseq
    if not isinstance(X0, complex):
        X0 *= complex(0.0, 1.0)
    if not isinstance(X1, complex):
        X1 *= complex(0.0, 1.0)
    if not isinstance(X2, complex):
        X2 *= complex(0.0, 1.0)
    Ifault = Vth / (X0 + X1 + X2 + 3 * Rf)
    MVA = abs(Ifault) ** 2 * abs(X1) * Sbase
    if Sbase != 1:
        MVA = MVA * 1e-06
    return MVA


def busvolt(k, n, Vpf, Z0, Z1, Z2, If, sequence=True, reference='A'):
    """
    Faulted Bus Voltage Calculator
    
    This function is designed to calculate the bus voltage(s)
    given a specific set of fault characteristics.
    
    Parameters
    ----------
    k:          float
                Bus index at which to calculate faulted voltage
    n:          float
                Bus index at which fault occurred
    Vpf:        complex
                Voltage Pre-Fault, Singular Number
    Z0:         ndarray
                Zero-Sequence Impedance Matrix
    Z1:         ndarray
                Positive-Sequence Impedance Matrix
    Z2:         ndarray
                Negative-Sequence Impedance Matrix
    If:         complex
                Sequence Fault Current Evaluated at Bus *n*
    sequence:   bool, optional
                Control argument to force return into symmetrical-
                or phase-domain values.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Vf:         complex
                The Fault Voltage, set of sequence or phase voltages as
                specified by *sequence*
    """
    k = k - 1
    n = n - 1
    Z0 = _np.asarray(Z0)
    Z1 = _np.asarray(Z1)
    Z2 = _np.asarray(Z2)
    If = _np.asarray(If)
    Vfmat = _np.array([0, Vpf, 0]).T
    Zmat = _np.array([[Z0[(k, n)], 0, 0],
     [
      0, Z1[(k, n)], 0],
     [
      0, 0, Z2[(k, n)]]])
    Vf = Vfmat - Zmat.dot(If)
    if not sequence:
        Vf = _phaseroll(Vf, reference)
    return Vf


def ct_saturation(XoR, Imag, Vrated, Irated, CTR, Rb, Xb, remnance=0, freq=60, ALF=20):
    r"""
    Current Transformer Saturation Calculator
    
    A function to determine the saturation value and a boolean indicator
    showing whether or not CT is -in fact- saturated.
    
    To perform this evaluation, we must satisfy the equation:
    
    .. math::
       20\geq(1+\frac{X}{R})*\frac{|I_{mag}|}{I_{rated}*CTR}
       *\frac{\left|R_{burden}+j*\omega*\frac{X_{burden}}
       {\omega}\right|*100}{V_{rated}*(1-remnanc)}
    
    Parameters
    ----------
    XoR:        float
                The X-over-R ratio of the system.
    Imag:       float
                The (maximum) current magnitude to use for calculation,
                typically the fault current.
    Vrated:     float
                The rated voltage (accompanying the C-Class value) of
                the CT.
    Irated:     float
                The rated secondary current for the CT.
    CTR:        float
                The CT Ratio (primary/secondary, N) to be used.
    Rb:         float
                The total burden resistance in ohms.
    Xb:         float
                The total burden reactance in ohms.
    remnance:   float, optional
                The system flux remnance, default=0.
    freq:       float, optional
                The system frequency in Hz, default=60.
    ALF:        float, optional
                The Saturation Constant which must be satisfied,
                default=20.
    
    Returns
    -------
    result:     float
                The calculated Saturation value.
    saturation: bool
                Boolean indicator to mark presence of saturation.
    """
    w = 2 * _np.pi * freq
    Lb = Xb / w
    Vrated = Vrated * (1 - remnance)
    t1 = 1 + XoR
    t2 = Imag / (Irated * CTR)
    t3 = abs(Rb + complex(0.0, 1.0) * w * Lb) * 100 / Vrated
    result = t1 * t2 * t3
    saturation = result >= ALF
    return (
     result, saturation)


def ct_cclass(XoR, Imag, Irated, CTR, Rb, Xb, remnance=0, freq=60, ALF=20):
    r"""
    Current Transformer (CT) C-Class Function
    
    A function to determine the C-Class rated voltage for a CT.
    The formula shown below is used.
    
    .. math::
       C_{class}=\frac{(1+\frac{X}{R})*\frac{|I_{mag}|}
       {I_{rated}*CTR}*\frac{\left|R_{burden}+j*\omega*
       \frac{X_{burden}}{\omega}\right|*100}{V_{rated}}}
       {1-remnance}
    
    Parameters
    ----------
    XoR:        float
                The X-over-R ratio of the system.
    Imag:       float
                The (maximum) current magnitude to use for calculation,
                typically the fault current.
    Irated:     float
                The rated secondary current for the CT.
    CTR:        float
                The CT Ratio (primary/secondary, N) to be used.
    Rb:         float
                The total burden resistance in ohms.
    Xb:         float
                The total burden reactance in ohms.
    remnance:   float, optional
                The system flux remnance, default=0.
    freq:       float, optional
                The system frequency in Hz, default=60.
    ALF:        float, optional
                The Saturation Constant which must be satisfied,
                default=20.
    
    Returns
    -------
    c_class:    float
                The calculated C-Class rated voltage.
    """
    w = 2 * _np.pi * freq
    Lb = Xb / w
    t1 = 1 + XoR
    t2 = Imag / (Irated * CTR)
    t3 = abs(Rb + complex(0.0, 1.0) * w * Lb) * 100 / ALF
    Vr_w_rem = t1 * t2 * t3
    c_class = Vr_w_rem / (1 - remnance)
    return c_class


def ct_satratburden(Inom, VArat=None, ANSIv=None, ALF=20):
    r"""
    Current Transformer (CT) Saturation at Rated Burden Calculator
    
    A function to determine the Saturation at rated burden.
    
    .. math:: V_{saturated}=ALF*\frac{VA_{rated}}{I_{nominal}}
    
    where:
    
    .. math:: VA_{rated}=I_{nominal}*\frac{ANSI_{voltage}}{20}
    
    Parameters
    ----------
    Inom:       float
                Nominal Current
    VArat:      float, optional, exclusive
                The apparent power (VA) rating of the CT.
    ANSIv:      float, optional, exclusive
                The ANSI voltage requirement to meet.
    ALF:        float, optional
                Accuracy Limit Factor, default=20.
    
    Returns
    -------
    Vsat:       float
                The saturated voltage.
    """
    if VArat == None and ANSIv == None:
        raise ValueError('VArat or ANSIv must be specified.')
    else:
        if VArat == None:
            VArat = Inom * ANSIv / 20
    Vsat = ALF * VArat / Inom
    return Vsat


def ct_vpeak(Zb, Ip, CTR):
    r"""
    Current Transformer (CT) Peak Voltage Calculator
    
    Simple formula to calculate the Peak Voltage of a CT.
    
    .. math:: \sqrt{3.5*|Z_burden|*I_{peak}*CTR}
    
    Parameters
    ----------
    Zb:         float
                The burden impedance magnitude (in ohms).
    Ip:         float
                The peak current for the CT.
    CTR:        float
                The CTR turns ratio of the CT.
    
    Returns
    -------
    Vpeak:      float
                The peak voltage.
    """
    return _np.sqrt(3.5 * abs(Zb) * Ip * CTR)


def ct_timetosat(Vknee, XoR, Rb, CTR, Imax, ts=None, npts=100, freq=60, plot=False):
    """
    Current Transformer (CT) Time to Saturation Function
    
    Function to determine the "time to saturate" for an underrated C-Class
    CT using three standard curves described by Juergen Holbach.
    
    Parameters
    ----------
    Vknee:      float
                The knee-voltage for the CT.
    XoR:        float
                The X-over-R ratio of the system.
    Rb:         float
                The total burden resistance in ohms.
    CTR:        float
                The CT Ratio (primary/secondary, N) to be used.
    Imax:       float
                The (maximum) current magnitude to use for calculation,
                typically the fault current.
    ts:         numpy.ndarray or float, optional
                The time-array or particular (floatint point) time at which
                to calculate the values. default=_np.linspace(0,0.1,freq*npts)
    npts:       float, optional
                The number of points (per cycle) to calculate if ts is not
                specified, default=100.
    freq:       float, optional
                The system frequency in Hz, default=60.
    plot:       bool, optional
                Control argument to enable plotting of calculated curves,
                default=False.
    """
    w = 2 * _np.pi * freq
    Tp = XoR / w
    if ts == None:
        ts = _np.linspace(0, 0.1, freq * npts)
    term = -XoR * (_np.exp(-ts / Tp) - 1)
    Vsat1 = Imax * Rb * (term + 1)
    Vsat2 = Imax * Rb * (term - _np.sin(w * ts))
    Vsat3 = Imax * Rb * (1 - _np.cos(w * ts))
    if plot and isinstance(ts, _np.ndarray):
        plt.plot(ts, Vsat1, label='Vsat1')
        plt.plot(ts, Vsat2, label='Vsat2')
        plt.plot(ts, Vsat3, label='Vsat3')
        plt.axhline(Vknee, label='V-knee', linestyle='--')
        plt.title('Saturation Curves')
        plt.xlabel('Time (ts)')
        plt.legend()
        plt.show()
    else:
        if plot:
            print('Unable to plot a single point, *ts* must be a numpy-array.')
        else:
            Vsat1c = Vsat2c = Vsat3c = 0
            if isinstance(ts, _np.ndarray):
                for i in range(len(ts)):
                    if Vsat1[i] > Vknee:
                        if Vsat1c == 0:
                            Vsat1c = ts[(i - 1)]
                        if Vsat2[i] > Vknee:
                            if Vsat2c == 0:
                                Vsat2c = ts[(i - 1)]
                        if Vsat3[i] > Vknee and Vsat3c == 0:
                            Vsat3c = ts[(i - 1)]

                results = (
                 Vsat1c, Vsat2c, Vsat3c)
            else:
                results = (
                 Vsat1, Vsat2, Vsat3)
        return results


def pktransrecvolt(C, L, R=0, VLL=None, VLN=None, freq=60):
    """
    Peak Transient Recovery Function
    
    Peak Transient Recovery Voltage calculation
    function, evaluates the peak transient
    recovery voltage (restriking voltage) and
    the Rate-of-Rise-Recovery Voltage.
    
    Parameters
    ----------
    C:          float
                Capacitance Value in Farads.
    L:          float
                Inductance in Henries.
    R:          float, optional
                The resistance of the system used for
                calculation, default=0.
    VLL:        float, exclusive
                Line-to-Line voltage, exclusive
                optional argument.
    VLN:        float, exclusive
                Line-to-Neutral voltage, exclusive
                optional argument.
    freq:       float, optional
                System frequency in Hz.
    
    Returns
    -------
    Vcpk:       float
                Peak Transient Recovery Voltage in volts.
    RRRV:       float
                The RRRV (Rate-of-Rise-Recovery Voltage)
                calculated given the parameters in volts
                per second.
    """
    alpha = R / (2 * L)
    wn = 1 / _np.sqrt(L * C) - alpha
    fn = wn / (2 * _np.pi)
    if VLL != None:
        Vm = _np.sqrt(0.6666666666666666) * VLL
    else:
        if VLN != None:
            Vm = _np.sqrt(2) * VLN
        else:
            raise ValueError('One voltage must be specified.')
    Vcpk = wn ** 2 / (wn ** 2 - 2 * _np.pi * freq) * Vm * 2
    RRRV = 2 * Vm * fn / 0.5
    return (Vcpk, RRRV)


def trvresistor(C, L, reduction, Rd0=500, wd0=260000.0, tpk0=1e-05):
    """
    Transient Recovery Voltage (TRV) Reduction Resistor Function
    
    Function to find the resistor value that
    will reduce the TRV by a specified
    percentage.
    
    Parameters
    ----------
    C:          float
                Capacitance Value in Farads.
    L:          float
                Inductance in Henries.
    reduction:  float
                The percentage that the TRV
                should be reduced by.
    Rd0:        float, optional
                Damping Resistor Evaluation Starting Point
                default=500
    wd0:        float, optional
                Omega-d evaluation starting point, default=260*k
    tpk0:       float, optional
                Time of peak voltage evaluation starting point,
                default=10*u
    
    Returns
    -------
    Rd:         float
                Damping resistor value, in ohms.
    wd:         float
                Omega-d
    tpk:        float
                Time of peak voltage.
    """
    wn = 1 / _np.sqrt(L * C)
    fctr = (1 - reduction) * 2 - 1

    def equations(data):
        Rd, wd, tpk = data
        X = _np.sqrt(wn ** 2 - (1 / (2 * Rd * C)) ** 2) - wd
        Y = _np.exp(-tpk / (2 * Rd * C)) - fctr
        Z = wd * tpk - _np.pi
        return (X, Y, Z)

    Rd, wd, tpk = _fsolve(equations, (Rd0, wd0, tpk0))
    return (Rd, wd, tpk)


def toctriptime(I, Ipickup, TD, curve='U1', CTR=1):
    """
    Time OverCurrent Trip Time Function
    
    Time-OverCurrent Trip Time Calculator, evaluates the time
    to trip for a specific TOC (51) element given the curve
    type, current characteristics and time-dial setting.
    
    Parameters
    ----------
    I:          float
                Measured Current in Amps
    Ipickup:    float
                Fault Current Pickup Setting (in Amps)
    TD:         float
                Time Dial Setting
    curve:      string, optional
                Name of specified TOC curve, may be entry from set:
                {U1,U2,U3,U4,U5,C1,C2,C3,C4,C5}, default=U1
    CTR:        float, optional
                Current Transformer Ratio, default=1
    
    Returns
    -------
    tt:         float
                Time-to-Trip for characterized element.
    """
    curve = curve.upper()
    const = {'U1':{'A':0.0104, 
      'B':0.2256,  'P':0.02}, 
     'U2':{'A':5.95, 
      'B':0.18,  'P':2.0}, 
     'U3':{'A':3.88, 
      'B':0.0963,  'P':2.0}, 
     'U4':{'A':5.67, 
      'B':0.352,  'P':2.0}, 
     'U5':{'A':0.00342, 
      'B':0.00262,  'P':0.02}, 
     'C1':{'A':0.14, 
      'B':0,  'P':0.02}, 
     'C2':{'A':13.5, 
      'B':0,  'P':2.0}, 
     'C3':{'A':80.0, 
      'B':0,  'P':2.0}, 
     'C4':{'A':120.0, 
      'B':0,  'P':2.0}, 
     'C5':{'A':0.05, 
      'B':0,  'P':0.04}}
    A = const[curve]['A']
    B = const[curve]['B']
    P = const[curve]['P']
    M = I / (CTR * Ipickup)
    tt = TD * (A / (M ** P - 1) + B)
    return tt


def tocreset(I, Ipickup, TD, curve='U1', CTR=1):
    """
    Time OverCurrent Reset Time Function
    
    Function to calculate the time to reset for a TOC
    (Time-OverCurrent, 51) element.
    
    Parameters
    ----------
    I:          float
                Measured Current in Amps
    Ipickup:    float
                Fault Current Pickup Setting (in Amps)
    TD:         float
                Time Dial Setting
    curve:      string, optional
                Name of specified TOC curve, may be entry from set:
                {U1,U2,U3,U4,U5,C1,C2,C3,C4,C5}, default=U1
    CTR:        float, optional
                Current Transformer Ratio, default=1
    
    Returns
    -------
    tr:         float
                Time-to-Reset for characterized element.
    """
    curve = curve.upper()
    C = {'U1':1.08, 
     'U2':5.95,  'U3':3.88,  'U4':5.67, 
     'U5':0.323,  'C1':13.5,  'C2':47.3, 
     'C3':80.0,  'C4':120.0,  'C5':4.85}
    M = I / (CTR * Ipickup)
    tr = TD * (C[curve] / (1 - M ** 2))
    return tr


def pickup(Iloadmax, Ifaultmin, scale=0, printout=False, units='A'):
    """
    Current Pickup Selection Assistant
    
    Used to assist in evaluating an optimal phase-over-current pickup
    setting. Uses maximum load and minimum fault current to provide
    user assistance.
    
    Parameters
    ----------
    Iloadmax:   float
                The maximum load current in amps.
    Ifaultmin:  float
                The minimum fault current in amps.
    scale:      int, optional
                Control scaling to set number of significant figures.
                default=0
    printout:   boolean, optional
                Control argument to enable printing of intermediate
                stages, default=False.
    units:      string, optional
                String to be appended to any printed output denoting
                the units of which are being printed, default="A"
    
    Returns
    -------
    setpoint:   float
                The evaluated setpoint at which the function suggests
                the phase-over-current pickup setting be placed.
    """
    IL2 = 2 * Iloadmax
    IF2 = Ifaultmin / 2
    exponent = len(str(IL2).split('.')[0])
    setpoint = _np.ceil(IL2 * 10 ** (-exponent + 1 + scale)) * 10 ** (exponent - 1 - scale)
    if printout:
        print('Range Min:', IL2, units, '\t\tRange Max:', IF2, units)
    if IF2 < setpoint:
        setpoint = IL2
        if IL2 > IF2:
            raise ValueError('Invalid Parameters.')
    if printout:
        print('Current Pickup:', setpoint, units)
    return setpoint


def tdradial(I, CTI, Ipu_up, Ipu_dn=0, TDdn=0, curve='U1', scale=2, freq=60, CTR_up=1, CTR_dn=1, tfixed=None):
    """
    Radial Time Dial Coordination Function
    
    Function to evaluate the Time-Dial (TD) setting in radial schemes
    where the Coordinating Time Interval (CTI) and the up/downstream
    pickup settings are known along with the TD setting for the
    downstream protection.
    
    Parameters
    ----------
    I:          float
                Measured fault current in Amps, typically set using the
                maximum fault current available.
    CTI:        float
                Coordinating Time Interval in cycles.
    Ipu_up:     float
                Pickup setting for upstream protection,
                specified in amps
    Ipu_dn:     float, optional
                Pickup setting for downstream protection,
                specified in amps, default=0
    TDdn:       float, optional
                Time-Dial setting for downstream protection,
                specified in seconds, default=0
    curve:      string, optional
                Name of specified TOC curve, may be entry from set:
                {U1,U2,U3,U4,U5,C1,C2,C3,C4,C5}, default=U1
    scale:      int, optional
                Scaling value used to evaluate a practical TD
                setting, default=2
    freq:       float, optional
                System operating frequency, default=60
    CTR_up:     float, optional
                Current Transformer Ratio for upstream relay.
                default=1
    CTR_dn:     float, optional
                Current Transformer Ratio for downstream relay.
                default=1
    tfixed:     float, optional
                Used to specify a fixed time delay for coordinated
                protection elements, primarily used for coordinating
                TOC elements (51) with OC elements (50) with a fixed
                tripping time. Overrides downstream TOC arguments
                including *Ipu_dn* and *TDdn*.
    
    Returns
    -------
    TD:         float
                Calculated Time-Dial setting according to radial
                scheme logical analysis.
    """
    curve = curve.upper()
    const = {'U1':{'A':0.0104, 
      'B':0.2256,  'P':0.02}, 
     'U2':{'A':5.95, 
      'B':0.18,  'P':2.0}, 
     'U3':{'A':3.88, 
      'B':0.0963,  'P':2.0}, 
     'U4':{'A':5.67, 
      'B':0.352,  'P':2.0}, 
     'U5':{'A':0.00342, 
      'B':0.00262,  'P':0.02}, 
     'C1':{'A':0.14, 
      'B':0,  'P':0.02}, 
     'C2':{'A':13.5, 
      'B':0,  'P':2.0}, 
     'C3':{'A':80.0, 
      'B':0,  'P':2.0}, 
     'C4':{'A':120.0, 
      'B':0,  'P':2.0}, 
     'C5':{'A':0.05, 
      'B':0,  'P':0.04}}
    A = const[curve]['A']
    B = const[curve]['B']
    P = const[curve]['P']
    if tfixed == None:
        CTI = CTI / freq
        M = I / (CTR_dn * Ipu_dn)
        tpu_desired = TDdn * (A / (M ** P - 1) + B) + CTI
    else:
        tpu_desired = tfixed + CTI
    M = I / (CTR_up * Ipu_up)
    TD = tpu_desired / (A / (M ** 2 - 1) + B)
    TD = _np.floor(TD * 10 ** scale) / 10 ** scale
    return TD


def protectiontap(S, CTR=1, VLN=None, VLL=None):
    """
    Protection TAP Setting Calculator
    
    Evaluates the required TAP setting based on the rated power of
    a transformer (the object being protected) and the voltage
    (either primary or secondary) in conjunction with the CTR
    (current transformer ratio) for the side in question (primary/
    secondary).
    
    Parameters
    ----------
    CTR:        float
                The Current Transformer Ratio.
    S:          float
                Rated apparent power magnitude (VA/VAR/W).
    VLN:        float, exclusive
                Line-to-Neutral voltage in volts.
    VLL:        float, exclusive
                Line-to-Line voltage in volts.
    
    Returns
    -------
    TAP:        float
                The TAP setting required to meet the specifications.
    """
    if VLL != None:
        V = abs(_np.sqrt(3) * VLL)
    else:
        if VLN != None:
            V = abs(3 * VLN)
        else:
            raise ValueError('One or more voltages must be provided.')
    TAP = abs(S) / (V * CTR)
    return TAP


def correctedcurrents(Ipri, TAP, correction='Y', CTR=1):
    """
    Transformer Current Correction Function
    
    Function to evaluate the currents as corrected for microprocessor-
    based relay protection schemes.
    
    Parameters
    ----------
    Ipri:       list of complex
                Three-phase set (IA, IB, IC) of primary currents.
    TAP:        float
                Relay's TAP setting.
    correction: string, optional
                String defining correction factor, may be one of:
                (Y, D+, D-, Z); Y denotes Y (Y0) connection, D+
                denotes Dab (D1) connection, D- denotes Dac (D11)
                connection, and Z (Z12) denotes zero-sequence
                removal. default="Y"
    CTR:        float
                Current Transformer Ratio, default=1
    
    Returns
    -------
    Isec_corr:  list of complex
                The corrected currents to perform operate/restraint
                calculations with.
    """
    MAT = {'Y':XFMY0, 
     'D+':XFMD1, 
     'D-':XFMD11, 
     'Z':XFM12}
    Ipri = _np.asarray(Ipri)
    if isinstance(correction, list):
        mult = MAT[correction[0]]
        for i in correction[1:]:
            mult = mult.dot(MAT[i])

    else:
        if isinstance(correction, str):
            mult = MAT[correction]
        else:
            if isinstance(correction, _np.ndarray):
                mult = correction
            else:
                raise ValueError('Correction must be string or list of strings.')
    Isec_corr = 1 / TAP * mult.dot(Ipri / CTR)
    return Isec_corr


def iopirt(IpriHV, IpriLV, TAPHV, TAPLV, corrHV='Y', corrLV='Y', CTRHV=1, CTRLV=1):
    """
    Operate/Restraint Current Calculator
    
    Calculates the operating current (Iop) and the restraint
    current (Irt) as well as the slope.
    
    Parameters
    ----------
    IpriHV:     list of complex
                Three-phase set (IA, IB, IC) of primary currents
                on the high-voltage side of power transformer.
    IpriLV      list of complex
                Three-phase set (IA, IB, IC) of primary currents
                on the low-voltage side of power transformer.
    TAPHV       float
                Relay's TAP setting for high-voltage side of
                power transformer.
    TAPLV       float
                Relay's TAP setting for low-voltage side of
                power transformer.
    corrHV      string, optional
                String defining correction factor on high-voltage
                side of power transformer, may be one of:
                (Y, D+, D-, Z); Y denotes Y (Y0) connection, D+
                denotes Dab (D1) connection, D- denotes Dac (D11)
                connection, and Z (Z12) denotes zero-sequence
                removal. default="Y"
    corrLV      string, optional
                String defining correction factor on low-voltage
                side of power transformer, may be one of:
                (Y, D+, D-, Z); Y denotes Y (Y0) connection, D+
                denotes Dab (D1) connection, D- denotes Dac (D11)
                connection, and Z (Z12) denotes zero-sequence
                removal. default="Y"
    CTRHV       float
                Current Transformer Ratio for high-voltage side
                of power transformer, default=1
    CTRLV       float
                Current Transformer Ratio for low-voltage side
                of power transformer, default=1
    
    Returns
    -------
    Iop:        list of float
                The operating currents for phases A, B, and C.
    Irt:        list of float
                The restraint currents for phases A, B, and C.
    slope:      list of float
                The calculated slopes for phases A, B, and C.
    """
    IcorHV = correctedcurrents(IpriHV, TAPHV, corrHV, CTRHV)
    IcorLV = correctedcurrents(IpriLV, TAPLV, corrLV, CTRLV)
    Iop = _np.absolute(IcorHV + IcorLV)
    Irt = _np.absolute(IcorHV) + _np.absolute(IcorLV)
    slope = Iop / Irt
    return (Iop, Irt, slope)


def symrmsfaultcur(V, R, X, t=0.016666666666666666, freq=60):
    """
    Symmetrical/RMS Current Calculator
    
    Function to evaluate the time-constant tau,
    the symmetrical fault current, and the RMS
    current for a faulted circuit.
    
    Parameters
    ----------
    V:          float
                Voltage magnitude at fault point,
                not described as line-to-line or
                line-to-neutral.
    R:          float
                The fault resistance in ohms.
    X:          float
                The fault impedance in ohms.
    t:          float, optional
                The time in seconds.
    freq:       float, optional
                The system frequency in Hz.
    
    Returns
    -------
    tau:        float
                The time-constant tau in seconds.
    Isym:       float
                Symmetrical fault current in amps.
    Irms:       float
                RMS fault current in amps.
    """
    Z = _np.sqrt(R ** 2 + X ** 2)
    tau = X / (2 * _np.pi * freq * R)
    Isym = V / _np.sqrt(3) / Z
    Irms = _np.sqrt(1 + 2 * _np.exp(-2 * t / tau)) * Isym
    return (tau, Isym, Irms)


def faultratio(I, Ipickup, CTR=1):
    """
    Fault Multiple of Pickup (Ratio) Calculator
    
    Evaluates the CTR-scaled pickup measured to
    pickup current ratio.
    
    M = meas / pickup
    
    Parameters
    ----------
    I:          float
                Measured Current in Amps
    Ipickup:    float
                Fault Current Pickup Setting (in Amps)
    CTR:        float, optional
                Current Transformer Ratio for relay,
                default=1
    
    Returns
    -------
    M:          float
                The measured-to-pickup ratio
    """
    M = I / (CTR * Ipickup)
    return M


def residcomp(z1, z0, linelength=1):
    """
    Residual Compensation Factor Function
    
    Evaluates the residual compensation factor based on
    the line's positive and zero sequence impedance
    characteristics.
    
    Parameters
    ----------
    z1:         complex
                The positive-sequence impedance
                characteristic of the line, specified in 
                ohms-per-unit where the total line length
                (of same unit) is specified in
                *linelength* argument.
    z0:         complex
                The zero-sequence impedance characteristic
                of the line, specified in ohms-per-unit
                where the total line length (of same unit)
                is specified in *linelength* argument.
    linelength: float, optional
                The length (in same base unit as impedance
                characteristics) of the line. default=1
    
    Returns
    -------
    k0:         complex
                The residual compensation factor.
    """
    Z1L = z1 * linelength
    Z0L = z0 * linelength
    k0 = (Z0L - Z1L) / (3 * Z1L)
    return k0


def distmeasz(VLNmeas, If, Ip, Ipp, CTR=1, VTR=1, k0=None, z1=None, z0=None, linelength=1):
    """
    Distance Element Measured Impedance Function
    
    Function to evaluate the Relay-Measured-Impedance as calculated from
    the measured voltage, current, and line parameters.
    
    Parameters
    ----------
    VLNmeas:    complex
                Measured Line-to-Neutral voltage for the
                faulted phase in primary volts.
    If:         complex
                Faulted phase current measured in primary
                amps.
    Ip:         complex
                Secondary phase current measured in primary
                amps.
    Ipp:        complex
                Terchiary phase current measured in primary
                amps.
    CTR:        float, optional
                Current transformer ratio, default=1
    VTR:        float, optional
                Voltage transformer ratio, default=1
    k0:         complex, optional
                Residual Compensation Factor
    z1:         complex, optional
                The positive-sequence impedance
                characteristic of the line, specified in 
                ohms-per-unit where the total line length
                (of same unit) is specified in
                *linelength* argument.
    z0:         complex, optional
                The zero-sequence impedance characteristic
                of the line, specified in ohms-per-unit
                where the total line length (of same unit)
                is specified in *linelength* argument.
    linelength: float, optional
                The length (in same base unit as impedance
                characteristics) of the line. default=1
    
    Returns
    -------
    Zmeas:      complex
                The "measured" impedance as calculated by the relay.
    """
    if k0 == z1 == z0 == None:
        raise ValueError('Residual compensation arguments must be set.')
    if k0 == None:
        if z1 == None or z0 == None:
            raise ValueError('Both *z1* and *z0* must be specified.')
    if k0 == None:
        k0 = residcomp(z1, z0, linelength)
    V = VLNmeas / VTR
    Ir = (If + Ip + Ipp) / CTR
    I = If / CTR
    Zmeas = V / (I + k0 * Ir)
    return Zmeas


def transmismatch(I1, I2, tap1, tap2):
    """
    Transformer TAP Mismatch Function
    
    Function to evaluate the transformer ratio mismatch
    for protection.
    
    Parameters
    ----------
    I1:         complex
                Current (in amps) on transformer primary side.
    I2:         complex
                Current (in amps) on transformer secondary.
    tap1:       float
                Relay TAP setting on the primary side.
    tap2:       float
                Relay TAP setting on the secondary side.
    
    Returns
    -------
    mismatch:   float
                Transformer CT mismatch value associated with
                relay.
    """
    MR = min(abs(I1 / I2), abs(tap1 / tap2))
    mismatch = (abs(I1 / I2) - abs(tap1 / tap2)) * 100 / MR
    return mismatch


def highzvpickup(I, RL, Rct, CTR=1, threephase=False, Ks=1.5, Vstd=400, Kd=0.5):
    """
    High Impedance Pickup Setting Function
    
    Evaluates the voltage pickup setting for a high
    impedance bus protection system.
    
    Parameters
    ----------
    I:          float
                Fault current on primary side (in amps)
    RL:         float
                One-way line resistance in ohms
    Rct:        float
                Current Transformer Resistance in ohms
    CTR:        float, optional
                Current Transformer Ratio, default=1
    threephase: bool, optional
                Control argument to set the function to
                evaluate the result for a three-phase 
                fault or unbalanced fault. default=False
    Ks:         float, optional
                Security Factor for secure voltage pickup
                setting, default=1.5
    Vstd:       float, optional
                C-Class Voltage rating (i.e. C-400),
                default=400
    Kd:         float, optional
                The dependability factor for dependable
                voltage pickup setting, default=0.5
    
    Returns
    -------
    Vsens:      float
                The calculated sensetive voltage-pickup.
    Vdep:       float
                The calculated dependable voltage-pickup.
    """
    n = 2
    if threephase:
        n = 1
    Vsens = Ks * (n * RL + Rct) * I / CTR
    Vdep = Kd * Vstd
    return (Vsens, Vdep)


def highzmini(N, Ie, Irly=None, Vset=None, Rrly=2000, Imov=0, CTR=1):
    """
    Minimum Current for High Impedance Protection Calculator
    
    Evaluates the minimum pickup current required to cause
    high-impedance bus protection element pickup.
    
    Parameters
    ----------
    N:          int
                Number of Current Transformers included in scheme
    Ie:         float
                The excitation current at the voltage setting
    Irly:       float, optional
                The relay current at voltage setting
    Vset:       float, optional
                The relay's voltage pickup setting in volts.
    Rrly:       float, optional
                The relay's internal resistance in ohms, default=2000
    Imov:       float, optional
                The overvoltage protection current at the
                voltage setting. default=0.0
    CTR:        float, optional
                Current Transformer Ratio, default=1
    
    Returns
    -------
    Imin:       float
                Minimum current required to cause high-impedance
                bus protection element pickup.
    """
    if Irly == Vset == None:
        raise ValueError('Relay Current Required.')
    else:
        Ie = abs(Ie)
        Imov = abs(Imov)
        if Irly == None:
            Vset = abs(Vset)
            Irly = Vset / Rrly
        else:
            Irly = abs(Irly)
    Imin = (N * Ie + Irly + Imov) * CTR
    return Imin


def instoc(Imin, CTR=1, Ki=0.5):
    """
    Instantaneous OverCurrent Pickup Calculator
    
    Using a sensetivity factor and the CTR, evaluates
    the secondary-level pickup setting for an
    instantaneous overcurrent element.
    
    Parameters
    ----------
    Imin:       float
                The minimum fault current in primary amps.
    CTR:        float, optional
                Current Transformer Ratio, default=1
    Ki:         Sensetivity factor, default=0.5
    
    Returns
    -------
    Ipu:        float
                The pickup setting for the instantaneous
                overcurrent element as referred to the
                secondary side.
    """
    Ipu = Ki * abs(Imin) / CTR
    return Ipu


def genlossfield(Xd, Xpd, Zbase=1, CTR=1, VTR=1):
    """
    Generator Loss of Field Function
    
    Generates the Loss-of-Field Element settings
    for a generator using the Xd value and
    per-unit base information.
    
    Parameters
    ----------
    Xd:         float
                The Transient Reactance (Xd) term. May be
                specified in ohms or Per-Unit ohms if
                *Zbase* is set.
    Xpd:        float
                The Sub-Transient Reactance (X'd) term. May
                be specified in ohms or Per-Unit ohms if
                *Zbase* is set.
    Zbase:      float, optional
                Base impedance, used to convert per-unit
                Xd and Xpd to secondary values. default=1
    CTR:        float, optional
                Current Transformer Ratio, default=1
    VTR:        float, optional
                Voltage Transformer Ratio, default=1
    
    Returns
    -------
    ZoneOff:    float
                Zone Offset in ohms.
    Z1dia:      float
                Zone 1 diameter in ohms.
    Z2dia:      float
                Zone 2 diameter in ohms.
    """
    Xd = abs(Xd)
    Xpd = abs(Xpd)
    Zbase = abs(Zbase)
    Xd_sec = Xd * Zbase * (CTR / VTR)
    Xpd_sec = Xd * Zbase * (CTR / VTR)
    ZoneOff = Xpd_sec / 2
    Z1dia = Zbase * CTR / VTR
    Z2dia = Xd_sec
    return (
     ZoneOff, Z1dia, Z2dia)


def thermaltime(In, Ibase, tbase):
    r"""
    Simple Thermal Time Limit Calculator
    
    Computes the maximum allowable time for a specified
    current `In` given parameters for a maximum current
    and time at some other level, (`Ibase`, `tbase`).
    
    Uses the following formula:
    
    .. math:: t_n=\frac{I_{base}^2*t_{base}}{I_n^2}
    
    Parameters
    ----------
    In:         float
                Current at which to calculate max time.
    Ibase:      float
                Base current, at which maximum time
                `tbase` is allowable.
    tbase:      float
                Base time for which a maximum allowable
                current `Ibase` is specified. Unitless.
    
    Returns
    -------
    tn:         float
                Time allowable for specified current,
                `In`.
    """
    tn = Ibase ** 2 * tbase / In ** 2
    return tn