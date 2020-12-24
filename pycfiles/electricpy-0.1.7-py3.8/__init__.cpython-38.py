# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\electricpy\__init__.py
# Compiled at: 2019-12-19 12:29:33
# Size of source mod 2**32: 212824 bytes
"""
---------------
`electricpy.py`
---------------

 `A library of functions, constants and more
 that are related to Power in Electrical Engineering.`

 Written by Joe Stanley

Included Constants
------------------
 - Pico Multiple:                            p
 - Nano Multiple:                            n
 - Micro (mu) Multiple:                      u
 - Mili Multiple:                            m
 - Kilo Multiple:                            k
 - Mega Multiple:                            M
 - 'A' Operator for Symmetrical Components:  a
 - Not a Number value (NaN):                 NAN
 
Additional constants may not be listed. For a complete list,
visit constants page.

Symmetrical Components Matricies
--------------------------------
 - ABC to 012 Conversion:        Aabc
 - 012 to ABC Conversion:        A012

Included Functions
------------------
 - Phasor V/I Generator:                    phasor
 - Phasor Array V/I Generator:              phasorlist
 - Phasor Data Genorator:                   phasordata
 - Phase Angle Generator:                   phs
 - Time of Number of Cycles:                tcycle        
 - Phasor Impedance Generator:              phasorz
 - Complex Display Function:                cprint
 - Complex LaTeX Display Function:          clatex
 - Transfer Function LaTeX Generator:       tflatex
 - Parallel Impedance Adder:                parallelz
 - V/I Line/Phase Converter:                phaseline
 - Power Set Values:                        powerset
 - Power Triangle Function:                 powertriangle
 - Transformer SC OC Tests:                 transformertest
 - Phasor Plot Generator:                   phasorplot
 - Total Harmonic Distortion:               thd
 - Total Demand Distortion:                 tdd
 - Reactance Calculator:                    reactance
 - Non-Linear PF Calc:                      nlinpf
 - Harmonic Limit Calculator:               harmoniclimit
 - Power Factor Distiortion:                pfdist
 - Short-Circuit RL Current:                iscrl
 - Voltage Divider:                         voltdiv
 - Current Divider:                         curdiv
 - Instantaneous Power Calc.:               instpower
 - Delta-Wye Network Converter:             dynetz
 - Single Line Power Flow:                  powerflow
 - Thermocouple Temperature:                thermocouple
 - Cold Junction Voltage:                   coldjunction
 - RTD Temperature Calculator:              rtdtemp
 - Horsepower to Watts:                     hp_to_watts
 - Watts to Horsepower:                     watts_to_hp
 - Inductor Charge:                         inductorcharge
 - Inductor Discharge:                      inductordischarge
 - Inductor Stored Energy:                  inductorenergy      
 - Back-to-Back Cap. Surge:                 capbacktoback  
 - Capacitor Stored Energy:                 energy
 - Cap. Voltage after Time:                 VafterT
 - Cap. Voltage Discharge:                  vcapdischarge
 - Cap. Voltage Charge:                     vcapcharge
 - Rectifier Cap. Calculation:              rectifiercap
 - Cap. VAR to FARAD Conversion:            farads
 - VSC DC Bus Voltage Calculator:           vscdcbus
 - PLL-VSC Gains Calculator:                vscgains
 - Sinusoid Peak-to-RMS Converter:          rms
 - Sinusoid RMS-to-Peak Converter:          peak
 - Arbitrary Waveform RMS Calculator:       funcrms
 - Step Function:                           step
 - Multi-Argument Convolution:              convolve
 - Convolution Bar Graph Visualizer:        convbar
 - Gaussian Function:                       gaussian
 - Gaussian Distribution Calculator:        gausdist
 - Probability Density Calculator:          probdensity
 - Real FFT Evaluator:                      rfft
 - Normalized Power Spectrum:               wrms
 - Hartley's Data Capacity Equation:        hartleydata
 - Shannon's Data Capacity Equation:        shannondata
 - String to Bit-String Converter:          string_to_bits
 - CRC Message Generator:                   crcsender
 - CRC Remainder Calculator:                crcremainder
 - kWh to BTU:                              kwh_to_btu
 - BTU to kWh:                              btu_to_kwh
 - Per-Unit Impedance Calculator:           zpu
 - Per-Unit Current Calculator:             ipu
 - Per-Unit Change of Base Formula:         puchgbase
 - Per-Unit to Ohmic Impedance:             zrecompose
 - X over R to Ohmic Impedance:             rxrecompose
 - Generator Internal Voltage Calc:         geninternalv
 - Phase to Sequence Conversion:            abc_to_seq
 - Sequence to Phase Conversion:            seq_to_abc
 - Sequence Impedance Calculator:           sequencez
 - Function Harmonic (FFT) Evaluation:      funcfft
 - Dataset Harmonic (FFT) Evaluation:       sampfft
 - Harmonic (FFT) Component Plotter:        fftplot
 - Harmonic (FFT) Summation Plotter:        fftsumplot 
 - Harmonic System Generator:               harmonics   
 - Motor Startup Capacitor Formula:         motorstartcap
 - Power Factor Correction Formula:         pfcorrection
 - AC Power/Voltage/Current Relation:       acpiv
 - Transformer Primary Conversion:          primary
 - Transformer Secondary Conversion:        secondary
 - Natural Frequency Calculator             natfreq
 - 3-Phase Voltage/Current Unbalance:       unbalance
 - Characteristic Impedance Calculator:     characterz
 - Transformer Phase Shift Calculator:      xfmphs
 - Hertz to Radians Converter:              hz_to_rad
 - Radians to Hertz Converter:              rad_to_hz
 - Induction Machine Vth Calculator:        indmachvth
 - Induction Machine Zth Calculator:        indmachzth
 - Induction Machine Pem Calculator:        indmachpem
 - Induction Machine Tem Calculator:        indmachtem
 - Induction Machine Peak Slip Calculator:  indmachpkslip
 - Induction Machine Peak Torque Calc.:     indmachpktorq
 - Induction Machine Rotor Current:         indmachiar
 - Induction Machine Starting Torque:       indmachstarttorq
 - Stator Power for Induction Machine:      pstator
 - Rotor Power for Induction Machine:       protor
 - De Calculator:                           de_calc
 - Z Per Length Calculator:                 zperlength
 - Induction Machine FOC Rating Calculator: indmachfocratings
 - Induction Machine FOC Control Calc.:     imfoc_control
 - Synchronous Machine Internal Voltage:    synmach_Eq
 - Voltage / Current / PF Relation:         vipf
 - Radians/Second to RPM Converter:         rad_to_rpm
 - RPM to Radians/Second Converter:         rpm_to_rad
 - Hertz to RPM Converter:                  hz_to_rpm
 - RPM to Hertz Converter:                  rpm_to_hz
 - Synchronous Speed Calculator:            syncspeed
 - Machine Slip Calculator:                 machslip

Additional Available Sub-Modules
--------------------------------
 - fault.py
 - bode.py
 - sim.py

Functions Available in `electricpy.fault.py`
--------------------------------------------
 - Single Line to Ground                 phs1g
 - Double Line to Ground                 phs2g
 - Line to Line                          phs2
 - Three-Phase Fault                     phs3
 - Single Pole Open:                     poleopen1
 - Double Pole Open:                     poleopen2
 - Simple MVA Calculator:                scMVA
 - Three-Phase MVA Calculator:           phs3mvasc
 - Single-Phase MVA Calculator:          phs1mvasc
 - Faulted Bus Voltage                   busvolt
 - CT Saturation Function                ct_saturation
 - CT C-Class Calculator                 ct_cclass
 - CT Sat. V at rated Burden             ct_satratburden
 - CT Voltage Peak Formula               ct_vpeak
 - CT Time to Saturation                 ct_timetosat
 - Transient Recovery Voltage Calc.      pktransrecvolt
 - TRV Reduction Resistor                trvresistor
 - TOC Trip Time                         toctriptime
 - TOC Reset Time                        tocreset
 - Pickup Setting Assistant              pickup
 - Radial TOC Coordination Tool          tdradial
 - TAP Setting Calculator                protectiontap
 - Transformer Current Correction        correctedcurrents
 - Operate/Restraint Current Calc.       iopirt
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
 - Synchronous Machine Symm. Current:    synmach_Isym
 - Synchronous Machine Asymm. Current:   synmach_Iasym
 - Induction Machine Eigenvalue Calc.:   indmacheigenvalues
 - Induction Machine 3-Phase-SC Calc.:   indmachphs3sc
 - Induction Machine 3-Phs-Torq. Calc.:  indmachphs3torq

Functions Available in `electricpy.bode.py`
-------------------------------------------
 - Transfer Function Bode Plotter:       bode
 - S-Domain Bode Plotter:                sbode
 - Z-Domain Bode Plotter:                zbode

Functions Available in `electricpy.sim.py`
------------------------------------------
 - Digital Filter Simulator:             digifiltersim
 - Step Response Filter Simulator:       step_response
 - Ramp Response Filter Simulator:       ramp_response
 - Parabolic Response Filter Simulator:  parabolic_response
 - State-Space System Simulator:         statespace
 - Newton Raphson Calculator:            NewtonRaphson
 - Power Flow System Generator:          nr_pq
 - Multi-Bus Power Flow Calculator:      mbuspowerflow
"""
_name_ = 'electricpy'
_version_ = '0.1.7'
from .constants import *
from . import fault
from . import bode
from . import sim
import numpy as _np, matplotlib as _matplotlib
import matplotlib.pyplot as _plt
import cmath as _c
import scipy.optimize as _fsolve

def phs(ang):
    """
    Complex Phase Angle Generator
    
    Generate a complex value given the phase angle
    for the complex value.
    
    Same as `phase`.
    
    Parameters
    ----------
    ang:        float
                The angle (in degrees) for which
                the value should be calculated.
    
    See Also
    --------
    phasorlist: Phasor Generator for List or Array
    cprint:     Complex Variable Printing Function
    phasorz:    Impedance Phasor Generator
    phasor:     Phasor Generating Function
    """
    return _np.exp(complex(0.0, 1.0) * _np.radians(ang))


phase = phs

def phasor(mag, ang=0):
    """
    Complex Phasor Generator
    
    Generates the standard Pythonic complex representation
    of a phasor voltage or current when given the magnitude
    and angle of the specific voltage or current.
    
    Parameters
    ----------
    mag:        float
                The Magnitude of the Voltage/Current
    ang:        float
                The Angle (in degrees) of the Voltage/Current
    
    Returns
    -------
    phasor:     complex
                Standard Pythonic Complex Representation of
                the specified voltage or current.
    
    Examples
    --------
    >>> import electricpy as ep
    >>> ep.phasor(67, 120) # 67 volts at angle 120 degrees
    (-33.499999999999986+58.02370205355739j)
    
    See Also
    --------
    phasorlist: Phasor Generator for List or Array
    cprint:     Complex Variable Printing Function
    phasorz:    Impedance Phasor Generator
    phs:        Complex Phase Angle Generator
    """
    if isinstance(mag, (tuple, list, _np.ndarray)):
        ang = mag[1]
        mag = mag[0]
    return _c.rect(mag, _np.radians(ang))


def phasorlist(arr):
    """
    Complex Phasor Generator for 2-D Array or 2-D List
    
    Generates the standard Pythonic complex representation
    of a phasor voltage or current when given the magnitude
    and angle of the specific voltage or current for a list
    or array of values.
    
    Parameters
    ----------
    arr:        numpy.ndarray
                2-D array or list of magnitudes and angles.
                Each item must be set of magnitude and angle
                in form of: [mag, ang].
    
    Returns
    -------
    phasor:     complex
                Standard Pythonic Complex Representation of
                the specified voltage or current.
    
    Examples
    --------
    >>> import numpy as np
    >>> import electricpy as ep
    >>> voltages = _np.array([[67,0],
                             [67,-120],
                             [67,120]])
    >>> Vset = ep.phasorlist( voltages )
    >>> print(Vset)
    
    See Also
    --------
    phasor:     Phasor Generating Function
    cprint:     Complex Variable Printing Function
    phasorz:    Impedance Phasor Generator
    """
    outarr = _np.array([])
    for i in arr:
        outarr = _np.append(outarr, phasor(i))
    else:
        return outarr


def phasordata(mn, mx=None, npts=1000, mag=1, ang=0, freq=60, retstep=False, rettime=False, sine=False):
    """
    Complex Phasor Data Generator
    
    Generates a sinusoidal data set with minimum, maximum,
    frequency, magnitude, and phase angle arguments.
    
    Parameters
    ----------
    mn:         float, optional
                Minimum time (in seconds) to generate data for.
                default=0
    mx:         float
                Maximum time (in seconds) to generate data for.
    npts:       float, optional
                Number of data samples. default=1000
    mag:        float, optional
                Sinusoid magnitude, default=1
    ang:        float, optional
                Sinusoid angle in degrees, default=0
    freq:       float, optional
                Sinusoid frequency in Hz
    retstep:    bool, optional
                Control argument to request return of time
                step size (dt) in seconds.
    sine:       bool, optional
                Control argument to require data be generated
                with a sinusoidal function instead of cosine.
                
    Returns
    -------
    data:       numpy.ndarray
                The resultant data array.
    """
    if mx == None:
        mx = mn
        mn = 0
    else:
        w = 2 * _np.pi * freq
        t, dt = _np.linspace(mn, mx, npts, retstep=True)
        if not sine:
            data = mag * _np.cos(w * t + _np.radians(ang))
        else:
            data = mag * _np.sin(w * t + _np.radians(ang))
    dataset = [
     data]
    if retstep:
        dataset.append(dt)
    if rettime:
        dataset.append(t)
    if len(dataset) == 1:
        return dataset[0]
    return dataset


def clatex(val, round=3, polar=True, predollar=True, postdollar=True, double=False):
    """
    Complex Value Latex Generator
    
    Function to generate a LaTeX string of complex value(s)
    in either polar or rectangular form. May generate both dollar
    signs.
    
    Parameters
    ----------
    val:        complex
                The complex value to be printed, if value
                is a list or numpy array, the result will be
                demonstrated as a matrix.
    round:      int, optional
                Control to specify number of decimal places
                that should displayed. default=True
    polar:      bool, optional
                Control argument to force result into polar
                coordinates instead of rectangular. default=True
    predollar:  bool, optional
                Control argument to enable/disable the dollar
                sign before the string. default=True
    postdollar: bool, optional
                Control argument to enable/disable the dollar
                sign after the string. default=True
    double:     bool, optional
                Control argument to specify whether or not
                LaTeX dollar signs should be double or single,
                default=False
    
    Returns
    -------
    latex:      str
                LaTeX string for the complex value.
    """

    def polarstring(val, round):
        mag, ang_r = _c.polar(val)
        ang = _np.degrees(ang_r)
        mag = _np.around(mag, round)
        ang = _np.around(ang, round)
        latex = str(mag) + '∠' + str(ang) + '°'
        return latex

    def rectstring(val, round):
        real = _np.around(val.real, round)
        imag = _np.around(val.imag, round)
        if imag > 0:
            latex = str(real) + '+j' + str(imag)
        else:
            latex = str(real) + '-j' + str(abs(imag))
        return latex

    if isinstance(val, list):
        val = _np.asarray(val)
    else:
        if isinstance(val, _np.ndarray):
            shp = val.shape
            try:
                row, col = shp
            except:
                row = shp[0]
                col = 1
            else:
                sz = val.size
                latex = '\\begin{bmatrix}'
            for ri in range(row):
                if ri != 0:
                    latex += '\\\\'
                if col > 1:
                    for ci in range(col):
                        if ci != 0:
                            latex += ' & '
                        if polar:
                            latex += polarstring(val[ri][ci], round)
                        else:
                            latex += rectstring(val[ri][ci], round)

                elif polar:
                    latex += polarstring(val[ri], round)
                else:
                    latex += rectstring(val[ri], round)
            else:
                latex += '\\end{bmatrix}'

        else:
            if isinstance(val, complex):
                if polar:
                    latex = polarstring(val, round)
                else:
                    latex = rectstring(val, round)
            else:
                raise ValueError('Invalid Input Type')
        if double:
            dollar = '$$'
        else:
            dollar = '$'
    if predollar:
        latex = dollar + latex
    if postdollar:
        latex = latex + dollar
    return latex


def tflatex(sys, sysp=None, var='s', predollar=True, postdollar=True, double=False, tolerance=1e-08):
    r"""
    Transfer Function LaTeX String Generator
    
    LaTeX string generating function to create a transfer
    function string in LaTeX. Particularly useful for
    demonstrating systems in Interactive Python Notebooks.
    
    Parameters
    ----------
    sys:        list
                If provided in conjunction with optional
                parameter `sysp`, the parameter `sys` will
                act as the numerator set. Otherwise, can be
                passed as a list containing two sublists,
                the first being the numerator set, and the
                second being the denominator set.
    sysp:       list, optional
                If provided, this input will act as the
                denominator of the transfer function.
    var:        str, optional
                The variable that should be printed for each
                term (i.e. 's' or 'j\omega'). default='s'
    predollar:  bool, optional
                Control argument to enable/disable the dollar
                sign before the string. default=True
    postdollar: bool, optional
                Control argument to enable/disable the dollar
                sign after the string. default=True
    double:     bool, optional
                Control argument to specify whether or not
                LaTeX dollar signs should be double or single,
                default=False
    tolerance:  float, optional
                The floating point tolerance cutoff to evaluate
                each term against. If the absolute value of the
                particular term is greater than the tolerance,
                the value will be printed, if not, it will not
                be printed. default=1e-8
    
    Returns
    -------
    latex:      str
                LaTeX string for the transfer function.
    """
    if isinstance(sysp, (list, tuple, _np.ndarray)):
        num = sys
        den = sysp
    else:
        num, den = sys

    def genstring(val):
        length = len(val)
        strg = ''
        for i, v in enumerate(val):
            if abs(v) > tolerance:
                if i != 0:
                    strg += '+'
                strg += str(v)
                xpnt = length - i - 1
                if xpnt == 1:
                    strg += var
                elif xpnt == 0:
                    pass
                else:
                    strg += var + '^{' + str(xpnt) + '}'
            return strg

    latex = '\\frac{' + genstring(num) + '}{'
    latex += genstring(den) + '}'
    if double:
        dollar = '$$'
    else:
        dollar = '$'
    if predollar:
        latex = dollar + latex
    if postdollar:
        latex = latex + dollar
    return latex


def compose--- This code section failed: ---

 L. 620         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'arr'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 621        12  LOAD_FAST                'arr'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'arr'
             20_0  COME_FROM            10  '10'

 L. 623        20  LOAD_GLOBAL              _np
               22  LOAD_METHOD              asarray
               24  LOAD_FAST                'arr'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'arr'

 L. 625        30  SETUP_FINALLY       194  'to 194'

 L. 626        32  LOAD_FAST                'arr'
               34  LOAD_ATTR                shape
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'row'
               40  STORE_FAST               'col'

 L. 628        42  LOAD_GLOBAL              _np
               44  LOAD_METHOD              array
               46  BUILD_LIST_0          0 
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'retarr'

 L. 630        52  LOAD_FAST                'col'
               54  LOAD_CONST               2
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE   116  'to 116'

 L. 631        60  LOAD_GLOBAL              range
               62  LOAD_FAST                'row'
               64  CALL_FUNCTION_1       1  ''
               66  GET_ITER         
               68  FOR_ITER            114  'to 114'
               70  STORE_FAST               'i'

 L. 632        72  LOAD_FAST                'arr'
               74  LOAD_FAST                'i'
               76  BINARY_SUBSCR    
               78  LOAD_CONST               0
               80  BINARY_SUBSCR    
               82  LOAD_CONST               1j
               84  LOAD_FAST                'arr'
               86  LOAD_FAST                'i'
               88  BINARY_SUBSCR    
               90  LOAD_CONST               1
               92  BINARY_SUBSCR    
               94  BINARY_MULTIPLY  
               96  BINARY_ADD       
               98  STORE_FAST               'item'

 L. 633       100  LOAD_GLOBAL              _np
              102  LOAD_METHOD              append
              104  LOAD_FAST                'retarr'
              106  LOAD_FAST                'item'
              108  CALL_METHOD_2         2  ''
              110  STORE_FAST               'retarr'
              112  JUMP_BACK            68  'to 68'
              114  JUMP_FORWARD        188  'to 188'
            116_0  COME_FROM            58  '58'

 L. 634       116  LOAD_FAST                'row'
              118  LOAD_CONST               2
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   180  'to 180'

 L. 635       124  LOAD_GLOBAL              range
              126  LOAD_FAST                'col'
              128  CALL_FUNCTION_1       1  ''
              130  GET_ITER         
              132  FOR_ITER            178  'to 178'
              134  STORE_FAST               'i'

 L. 636       136  LOAD_FAST                'arr'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'i'
              144  BINARY_SUBSCR    
              146  LOAD_CONST               1j
              148  LOAD_FAST                'arr'
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'i'
              156  BINARY_SUBSCR    
              158  BINARY_MULTIPLY  
              160  BINARY_ADD       
              162  STORE_FAST               'item'

 L. 637       164  LOAD_GLOBAL              _np
              166  LOAD_METHOD              append
              168  LOAD_FAST                'retarr'
              170  LOAD_FAST                'item'
              172  CALL_METHOD_2         2  ''
              174  STORE_FAST               'retarr'
              176  JUMP_BACK           132  'to 132'
              178  JUMP_FORWARD        188  'to 188'
            180_0  COME_FROM           122  '122'

 L. 639       180  LOAD_GLOBAL              ValueError
              182  LOAD_STR                 'Invalid Array Shape, must be 2xN or Nx2.'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           114  '114'

 L. 641       188  LOAD_FAST                'retarr'
              190  POP_BLOCK        
              192  RETURN_VALUE     
            194_0  COME_FROM_FINALLY    30  '30'

 L. 642       194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L. 643       200  LOAD_FAST                'arr'
              202  LOAD_ATTR                size
              204  STORE_FAST               'length'

 L. 645       206  LOAD_FAST                'length'
              208  LOAD_CONST               2
              210  COMPARE_OP               !=
              212  POP_JUMP_IF_FALSE   230  'to 230'

 L. 646       214  LOAD_GLOBAL              ValueError
              216  LOAD_STR                 'Invalid Array Size, Saw Length of '
              218  LOAD_GLOBAL              str
              220  LOAD_FAST                'length'
              222  CALL_FUNCTION_1       1  ''
              224  BINARY_ADD       
              226  CALL_FUNCTION_1       1  ''
              228  RAISE_VARARGS_1       1  'exception instance'
            230_0  COME_FROM           212  '212'

 L. 648       230  LOAD_FAST                'arr'
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  LOAD_CONST               1j
              238  LOAD_FAST                'arr'
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  BINARY_MULTIPLY  
              246  BINARY_ADD       
              248  ROT_FOUR         
              250  POP_EXCEPT       
              252  RETURN_VALUE     
              254  END_FINALLY      

Parse error at or near `STORE_FAST' instruction at offset 204


def tcycle(ncycles=1, freq=60):
    r"""
    Time of Electrical Cycles
    
    Evaluates the time for a number of n
    cycles given the system frequency.
    
    .. math:: t = \frac{n_{cycles}}{freq}
    
    Parameters
    ----------
    ncycles:    float, optional    
                Number (n) of cycles to evaluate, default=1
    freq:       float, optional
                System frequency in Hz, default=60
    
    Returns
    -------
    t:          float
                Total time for *ncycles*
    """
    ncycles = _np.asarray(ncycles)
    freq = _np.asarray(freq)
    time = ncycles / freq
    if len(time) == 1:
        return time[0]
    return time


def reactance(z, freq=60, sensetivity=1e-12):
    r"""
    Capacitance/Inductance from Impedance
    
    Calculates the Capacitance or Inductance in Farads or Henreys
    (respectively) provided the impedance of an element.
    Will return capacitance (in Farads) if ohmic impedance is
    negative :eq:`cap`, or inductance (in Henrys) if ohmic impedance is
    positive :eq:`ind`. If imaginary: calculate with j factor
    (imaginary number).
    
    .. math:: C = \frac{1}{\omega*Z}
       :label: cap
    
    .. math:: L = \frac{Z}{\omega}
       :label: ind
    
    This requires that the radian frequency is found as follows:
    
    .. math:: \omega = 2*\pi*freq
    
    where `freq` is the frequency in Hertz.
    
    .. note::
       It's worth noting here, that the resistance will be found by
       extracting the real part of a complex value. That is:
       
       .. math:: R = Real( R + jX )
       
    
    Parameters
    ----------
    z:              complex
                    The Impedance Provided, may be complex (R+jI)
    freq:           float, optional
                    The Frequency Base for Provided Impedance, default=60
    sensetivity:    float, optional
                    The sensetivity used to check if a resistance was
                    provided, default=1e-12
    
    Returns
    -------
    out:            float
                    Capacitance or Inductance of Impedance
    """
    w = 2 * _np.pi * freq
    if isinstance(z, complex):
        if abs(z.real) > sensetivity:
            R = z.real
        else:
            R = 0
        if z.imag > 0:
            out = z / (w * complex(0.0, 1.0))
        else:
            out = 1 / (w * complex(0.0, 1.0) * z)
        out = abs(out)
        if R != 0:
            out = (
             R, out)
    else:
        if z > 0:
            out = z / w
        else:
            out = 1 / (w * z)
        out = abs(out)
    return out


def cprint(val, unit=None, label=None, title=None, pretty=True, printval=True, ret=False, round=3):
    """
    Phasor (Complex) Printing Function
    
    This function is designed to accept a complex value (val) and print
    the value in the standard electrical engineering notation:
    
    **magnitude ∠ angle °**
    
    This function will print the magnitude in degrees, and can print
    a unit and label in addition to the value itself.
    
    Parameters
    ----------
    val:        complex
                The Complex Value to be Printed, may be singular value,
                tuple of values, or list/array.
    unit:       string, optional
                The string to be printed corresponding to the unit mark.
    label:      str, optional
                The pre-pended string used as a descriptive labeling string.
    title:      str, optional
                The pre-pended string describing a set of complex values.
    pretty:     bool, optional
                Control argument to force printed result to a *pretty*
                format without array braces. default=True
    printval:   bool, optional
                Control argument enabling/disabling printing of the string.
                default=True
    ret:        bool, optional
                Control argument allowing the evaluated value to be returned.
                default=False
    round:      int, optional
                Control argument specifying how many decimals of the complex
                value to be printed. May be negative to round to spaces
                to the left of the decimal place (follows standard round()
                functionality). default=3
    
    Returns
    -------
    numarr:     numpy.ndarray
                The array of values corresponding to the magnitude and angle,
                values are returned in the form: [[ mag, ang ],...,[ mag, ang ]]
                where the angles are evaluated in degrees.
    
    Examples
    --------
    >>> import electricpy as ep
    >>> v = ep.phasor(67, 120)
    >>> ep.cprint(v)
    67.0 ∠ 120.0°
    >>> voltages = _np.array([[67,0],
                             [67,-120],
                             [67,120]])
    >>> Vset = ep.phasorlist( voltages )
    >>> ep.cprint(Vset)
    [['67.0 ∠ 0.0°']
    ['67.0 ∠ -120.0°']
    ['67.0 ∠ 120.0°']]

    
    See Also
    --------
    phasor:     Phasor Generating Function
    phasorlist: Phasor Generating Function for Lists or Arrays
    phasorz:    Impedance Phasor Generator
    """
    if isinstance(val, list):
        val = _np.asarray(val)
    else:
        if isinstance(val, _np.ndarray):
            shp = val.shape
            try:
                row, col = shp
            except:
                row = shp[0]
                col = 1
            else:
                sz = val.size
                if isinstance(label, (list, _np.ndarray)):
                    if len(label) == 1:
                        tmp = label
                        for _ in range(sz):
                            label = _np.append(label, [tmp])

                    else:
                        if sz != len(label):
                            raise ValueError('Too Few Label Arguments')
        else:
            if isinstance(label, str):
                tmp = label
                for _ in range(sz):
                    label = _np.append(label, [tmp])

            else:
                if label == None:
                    label = _np.array([])
                    for _ in range(sz):
                        label = _np.append(label, None)

                else:
                    raise ValueError('Invalid Label')
        if isinstance(unit, (list, _np.ndarray)):
            if len(unit) == 1:
                tmp = unit
                for _ in range(sz):
                    unit = _np.append(unit, [tmp])

            else:
                if sz != len(unit):
                    raise ValueError('Too Few Unit Arguments')
        else:
            if isinstance(unit, str):
                tmp = unit
                for _ in range(sz):
                    unit = _np.append(unit, [tmp])

            else:
                if unit == None:
                    unit = _np.array([])
                    for _ in range(sz):
                        unit = _np.append(unit, None)

                else:
                    raise ValueError('Invalid Unit')
        printarr = _np.array([])
        numarr = _np.array([])
        for i in range(row):
            _val = val[i]
            _label = label[i]
            _unit = unit[i]
            mag, ang_r = _c.polar(_val)
            ang = _np.degrees(ang_r)
            mag = _np.around(mag, round)
            ang = _np.around(ang, round)
            strg = ''
            if _label != None:
                strg += _label + ' '
            strg += str(mag) + ' ∠ ' + str(ang) + '°'
            if _unit != None:
                strg += ' ' + _unit
            printarr = _np.append(printarr, strg)
            numarr = _np.append(numarr, [mag, ang])
        else:
            printarr = _np.reshape(printarr, (row, col))
            numarr = _np.reshape(numarr, (sz, 2))
            if printval and row == 1:
                if title != None:
                    print(title)
                print(strg)
            else:
                if printval and pretty:
                    strg = ''
                    start = True
                    for i in printarr:
                        if not start:
                            strg += '\n'
                        strg += str(i[0])
                        start = False
                    else:
                        if title != None:
                            print(title)
                        print(strg)

                else:
                    if printval:
                        if title != None:
                            print(title)
                        print(printarr)
                    elif ret:
                        return numarr
                    else:
                        if isinstance(val, (int, float, complex)):
                            if unit != None and not isinstance(unit, str):
                                raise ValueError('Invalid Unit Type for Value')
                            if label != None and not isinstance(label, str):
                                raise ValueError('Invalid Label Type for Value')
                            mag, ang_r = _c.polar(val)
                            ang = _np.degrees(ang_r)
                            mag = _np.around(mag, round)
                            ang = _np.around(ang, round)
                            strg = ''
                            if label != None:
                                strg += label + ' '
                            strg += str(mag) + ' ∠ ' + str(ang) + '°'
                            if unit != None:
                                strg += ' ' + unit
                            if printval:
                                if title != None:
                                    print(title)
                                print(strg)
                            if ret:
                                return [
                                 mag, ang]
                        else:
                            raise ValueError('Invalid Input Type')


def phasorz(C=None, L=None, freq=60, complex=True):
    r"""
    Phasor Impedance Generator
    
    This function's purpose is to generate the phasor-based
    impedance of the specified input given as either the
    capacitance (in Farads) or the inductance (in Henreys).
    The function will return the phasor value (in Ohms).
    
    .. math:: Z = \frac{-j}{\omega*C}
    
    .. math:: Z = j*\omega*L
    
    where:
    
    .. math:: \omega = 2*\pi*freq
    
    Parameters
    ----------
    C:          float, optional
                The capacitance value (specified in Farads),
                default=None
    L:          float, optional
                The inductance value (specified in Henreys),
                default=None
    freq:       float, optional
                The system frequency to be calculated upon, default=60
    complex:    bool, optional
                Control argument to specify whether the returned
                value should be returned as a complex value.
                default=True
    
    Returns
    -------
    Z:      complex
            The ohmic impedance of either C or L (respectively).
    """
    w = 2 * _np.pi * freq
    if C != None:
        Z = -1 / (w * C)
    if L != None:
        Z = w * L
    if complex:
        Z *= complex(0.0, 1.0)
    return Z


def parallelz(*args):
    r"""
    Parallel Impedance Calculator
    
    This function is designed to generate the total parallel
    impedance of a set (tuple) of impedances specified as real
    or complex values.
    
    .. math::
       Z_{eq}=(\frac{1}{Z_1}+\frac{1}{Z_2}+\dots+\frac{1}{Z_n})^{-1}
    
    Parameters
    ----------
    Z:      tuple of complex
            The tupled input set of impedances, may be a tuple
            of any size greater than 2. May be real, complex, or
            a combination of the two.
    
    Returns
    -------
    Zp:     complex
            The calculated parallel impedance of the input tuple.
    """
    L = len(args)
    if L == 1:
        Z = args[0]
        try:
            L = len(Z)
            if L == 1:
                Zp = Z[0]
            else:
                Zp = (1 / Z[0] + 1 / Z[1]) ** (-1)
                if L > 2:
                    for i in range(2, L):
                        Zp = (1 / Zp + 1 / Z[i]) ** (-1)

        except:
            Zp = Z

    else:
        Z = args
        Zp = (1 / Z[0] + 1 / Z[1]) ** (-1)
        if L > 2:
            for i in range(2, L):
                Zp = (1 / Zp + 1 / Z[i]) ** (-1)

    return Zp


def phaseline(VLL=None, VLN=None, Iline=None, Iphase=None, complex=False):
    r"""
    Line-Line to Line-Neutral Converter
    
    This function is designed to return the phase- or line-equivalent
    of the voltage/current provided. It is designed to be used when
    converting delta- to wye-connections and vice-versa.
    Given a voltage of one type, this function will return the
    voltage of the opposite type. The same is true for current.
    
    .. math:: V_{LL} = \sqrt{3}∠30° * V_{LN}
       :label: voltages
    
    Typical American (United States) standard is to note voltages in
    Line-to-Line values (VLL), and often, the Line-to-Neutral voltage
    is of value, this function uses the voltage :eq:`voltages` relation
    to evaluate either voltage given the other.
    
    .. math:: I_{Φ} = \frac{I_{line}}{\sqrt{3}∠-30°}
       :label: currents
    
    Often, the phase current in a delta-connected device is of
    particular interest, and the line-current is provided. This
    function uses the current :eq:`currents` formula to evaluate
    phase- and line-current given the opposing term.
    
    Parameters
    ----------
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    Iline:      float, optional
                The Line-Current; default=None
    Iphase:     float, optional
                The Phase-Current; default=None
    complex:    bool, optional
                Control to return value in complex form; default=False
    """
    output = 0
    if VLL is not None:
        VLN = VLL / VLLcVLN
        output = VLN
    else:
        if VLN is not None:
            VLL = VLN * VLLcVLN
            output = VLL
        else:
            if Iphase is not None:
                Iline = Iphase * ILcIP
                output = Iline
            else:
                if Iline is not None:
                    Iphase = Iline / ILcIP
                    output = Iphase
                else:
                    print('ERROR: No value givenor innapropriate valuegiven.')
                    return 0
    if complex:
        return output
    return abs(output)


def powerset(P=None, Q=None, S=None, PF=None, find=''):
    """
    Power Triangle Conversion Function
    
    This function is designed to calculate all values
    in the set { P, Q, S, PF } when two (2) of the
    values are provided. The equations in this
    function are prepared for AC values, that is:
    real and reactive power, apparent power, and power
    factor.
    
    Parameters
    ----------
    P:      float, optional
            Real Power, unitless; default=None
    Q:      float, optional
            Reactive Power, unitless; default=None
    S:      float, optional
            Apparent Power, unitless; default=None
    PF:     float, optional
            Power Factor, unitless, provided as a
            decimal value, lagging is positive,
            leading is negative; default=None
    find:   str, optional
            Control argument to specify which value
            should be returned.
    
    Returns
    -------
    P:      float
            Calculated Real Power Magnitude
    Q:      float
            Calculated Reactive Power Magnitude
    S:      float
            Calculated Apparent Power Magnitude
    PF:     float
            Calculated Power Factor
    """
    if P != None and Q != None:
        S = _np.sqrt(P ** 2 + Q ** 2)
        PF = P / S
        if Q < 0:
            PF = -PF
    else:
        if S != None and PF != None:
            P = abs(S * PF)
            Q = _np.sqrt(S ** 2 - P ** 2)
            if PF < 0:
                Q = -Q
        else:
            if P != None and PF != None:
                S = P / PF
                Q = _np.sqrt(S ** 2 - P ** 2)
                if PF < 0:
                    Q = -Q
            else:
                if P != None and S != None:
                    Q = _np.sqrt(S ** 2 - P ** 2)
                    PF = P / S
                else:
                    if Q != None and S != None:
                        P = _np.sqrt(S ** 2 - Q ** 2)
                        PF = P / S
                    else:
                        raise ValueError('ERROR: Invalid Parameters or too few parameters given to calculate.')
    find = find.upper()
    if find == 'P':
        return P
    if find == 'Q':
        return Q
    if find == 'S':
        return S
    if find == 'PF':
        return PF
    return (P, Q, S, PF)


def powertriangle--- This code section failed: ---

 L.1233         0  LOAD_FAST                'P'
                2  LOAD_CONST               None
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     32  'to 32'
                8  LOAD_FAST                'Q'
               10  LOAD_CONST               None
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  LOAD_FAST                'S'
               18  LOAD_CONST               None
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'PF'
               26  LOAD_CONST               None
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    54  'to 54'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'

 L.1234        32  LOAD_GLOBAL              powerset
               34  LOAD_FAST                'P'
               36  LOAD_FAST                'Q'
               38  LOAD_FAST                'S'
               40  LOAD_FAST                'PF'
               42  CALL_FUNCTION_4       4  ''
               44  UNPACK_SEQUENCE_4     4 
               46  STORE_FAST               'P'
               48  STORE_FAST               'Q'
               50  STORE_FAST               'S'
               52  STORE_FAST               'PF'
             54_0  COME_FROM            30  '30'

 L.1237        54  LOAD_CONST               0
               56  LOAD_FAST                'P'
               58  BUILD_LIST_2          2 
               60  STORE_FAST               'Plnx'

 L.1238        62  LOAD_CONST               0
               64  LOAD_CONST               0
               66  BUILD_LIST_2          2 
               68  STORE_FAST               'Plny'

 L.1239        70  LOAD_FAST                'P'
               72  LOAD_FAST                'P'
               74  BUILD_LIST_2          2 
               76  STORE_FAST               'Qlnx'

 L.1240        78  LOAD_CONST               0
               80  LOAD_FAST                'Q'
               82  BUILD_LIST_2          2 
               84  STORE_FAST               'Qlny'

 L.1241        86  LOAD_CONST               0
               88  LOAD_FAST                'P'
               90  BUILD_LIST_2          2 
               92  STORE_FAST               'Slnx'

 L.1242        94  LOAD_CONST               0
               96  LOAD_FAST                'Q'
               98  BUILD_LIST_2          2 
              100  STORE_FAST               'Slny'

 L.1245       102  LOAD_GLOBAL              _plt
              104  LOAD_METHOD              figure
              106  LOAD_CONST               1
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L.1246       112  LOAD_GLOBAL              _plt
              114  LOAD_METHOD              title
              116  LOAD_FAST                'text'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L.1247       122  LOAD_GLOBAL              _plt
              124  LOAD_ATTR                plot
              126  LOAD_FAST                'Plnx'
              128  LOAD_FAST                'Plny'
              130  LOAD_FAST                'color'
              132  LOAD_CONST               ('color',)
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  POP_TOP          

 L.1248       138  LOAD_GLOBAL              _plt
              140  LOAD_ATTR                plot
              142  LOAD_FAST                'Qlnx'
              144  LOAD_FAST                'Qlny'
              146  LOAD_FAST                'color'
              148  LOAD_CONST               ('color',)
              150  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              152  POP_TOP          

 L.1249       154  LOAD_GLOBAL              _plt
              156  LOAD_ATTR                plot
              158  LOAD_FAST                'Slnx'
              160  LOAD_FAST                'Slny'
              162  LOAD_FAST                'color'
              164  LOAD_CONST               ('color',)
              166  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              168  POP_TOP          

 L.1250       170  LOAD_GLOBAL              _plt
              172  LOAD_METHOD              xlabel
              174  LOAD_STR                 'Real Power (W)'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.1251       180  LOAD_GLOBAL              _plt
              182  LOAD_METHOD              ylabel
              184  LOAD_STR                 'Reactive Power (VAR)'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L.1252       190  LOAD_GLOBAL              max
              192  LOAD_GLOBAL              abs
              194  LOAD_FAST                'P'
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_GLOBAL              abs
              200  LOAD_FAST                'Q'
              202  CALL_FUNCTION_1       1  ''
              204  CALL_FUNCTION_2       2  ''
              206  STORE_FAST               'mx'

 L.1254       208  LOAD_FAST                'P'
              210  LOAD_CONST               0
              212  COMPARE_OP               >
              214  POP_JUMP_IF_FALSE   238  'to 238'

 L.1255       216  LOAD_GLOBAL              _plt
              218  LOAD_METHOD              xlim
              220  LOAD_CONST               0
              222  LOAD_FAST                'mx'
              224  LOAD_CONST               1.1
              226  BINARY_MULTIPLY  
              228  CALL_METHOD_2         2  ''
              230  POP_TOP          

 L.1256       232  LOAD_FAST                'mx'
              234  STORE_FAST               'x'
              236  JUMP_FORWARD        262  'to 262'
            238_0  COME_FROM           214  '214'

 L.1258       238  LOAD_GLOBAL              _plt
              240  LOAD_METHOD              xlim
              242  LOAD_FAST                'mx'
              244  UNARY_NEGATIVE   
              246  LOAD_CONST               1.1
              248  BINARY_MULTIPLY  
              250  LOAD_CONST               0
              252  CALL_METHOD_2         2  ''
              254  POP_TOP          

 L.1259       256  LOAD_FAST                'mx'
              258  UNARY_NEGATIVE   
              260  STORE_FAST               'x'
            262_0  COME_FROM           236  '236'

 L.1260       262  LOAD_FAST                'Q'
              264  LOAD_CONST               0
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   294  'to 294'

 L.1261       272  LOAD_GLOBAL              _plt
              274  LOAD_METHOD              ylim
              276  LOAD_CONST               0
              278  LOAD_FAST                'mx'
              280  LOAD_CONST               1.1
              282  BINARY_MULTIPLY  
              284  CALL_METHOD_2         2  ''
              286  POP_TOP          

 L.1262       288  LOAD_FAST                'mx'
              290  STORE_FAST               'y'
              292  JUMP_FORWARD        318  'to 318'
            294_0  COME_FROM           268  '268'

 L.1264       294  LOAD_GLOBAL              _plt
              296  LOAD_METHOD              ylim
              298  LOAD_FAST                'mx'
              300  UNARY_NEGATIVE   
              302  LOAD_CONST               1.1
              304  BINARY_MULTIPLY  
              306  LOAD_CONST               0
              308  CALL_METHOD_2         2  ''
              310  POP_TOP          

 L.1265       312  LOAD_FAST                'mx'
              314  UNARY_NEGATIVE   
              316  STORE_FAST               'y'
            318_0  COME_FROM           292  '292'

 L.1266       318  LOAD_FAST                'PF'
              320  LOAD_CONST               0
              322  COMPARE_OP               >
          324_326  POP_JUMP_IF_FALSE   334  'to 334'

 L.1267       328  LOAD_STR                 ' Lagging'
              330  STORE_FAST               'PFtext'
              332  JUMP_FORWARD        338  'to 338'
            334_0  COME_FROM           324  '324'

 L.1269       334  LOAD_STR                 ' Leading'
              336  STORE_FAST               'PFtext'
            338_0  COME_FROM           332  '332'

 L.1270       338  LOAD_STR                 'P:   '
              340  LOAD_GLOBAL              str
              342  LOAD_FAST                'P'
              344  CALL_FUNCTION_1       1  ''
              346  BINARY_ADD       
              348  LOAD_STR                 ' W\n'
              350  BINARY_ADD       
              352  STORE_FAST               'text'

 L.1271       354  LOAD_FAST                'text'
              356  LOAD_STR                 'Q:   '
              358  BINARY_ADD       
              360  LOAD_GLOBAL              str
              362  LOAD_FAST                'Q'
              364  CALL_FUNCTION_1       1  ''
              366  BINARY_ADD       
              368  LOAD_STR                 ' VAR\n'
              370  BINARY_ADD       
              372  STORE_FAST               'text'

 L.1272       374  LOAD_FAST                'text'
              376  LOAD_STR                 'S:   '
              378  BINARY_ADD       
              380  LOAD_GLOBAL              str
              382  LOAD_FAST                'S'
              384  CALL_FUNCTION_1       1  ''
              386  BINARY_ADD       
              388  LOAD_STR                 ' VA\n'
              390  BINARY_ADD       
              392  STORE_FAST               'text'

 L.1273       394  LOAD_FAST                'text'
              396  LOAD_STR                 'PF:  '
              398  BINARY_ADD       
              400  LOAD_GLOBAL              str
              402  LOAD_GLOBAL              abs
              404  LOAD_FAST                'PF'
              406  CALL_FUNCTION_1       1  ''
              408  CALL_FUNCTION_1       1  ''
              410  BINARY_ADD       
              412  LOAD_FAST                'PFtext'
              414  BINARY_ADD       
              416  LOAD_STR                 '\n'
              418  BINARY_ADD       
              420  STORE_FAST               'text'

 L.1274       422  LOAD_FAST                'text'
              424  LOAD_STR                 'ΘPF: '
              426  BINARY_ADD       
              428  LOAD_GLOBAL              str
              430  LOAD_GLOBAL              _np
              432  LOAD_METHOD              degrees
              434  LOAD_GLOBAL              _np
              436  LOAD_METHOD              arccos
              438  LOAD_FAST                'PF'
              440  CALL_METHOD_1         1  ''
              442  CALL_METHOD_1         1  ''
              444  CALL_FUNCTION_1       1  ''
              446  BINARY_ADD       
              448  LOAD_STR                 '°'
              450  BINARY_ADD       
              452  LOAD_FAST                'PFtext'
              454  BINARY_ADD       
              456  STORE_FAST               'text'

 L.1276       458  LOAD_FAST                'printval'
          460_462  POP_JUMP_IF_FALSE   494  'to 494'

 L.1277       464  LOAD_GLOBAL              _plt
              466  LOAD_ATTR                text
              468  LOAD_FAST                'x'
              470  LOAD_CONST               20
              472  BINARY_TRUE_DIVIDE
              474  LOAD_FAST                'y'
              476  LOAD_CONST               4
              478  BINARY_MULTIPLY  
              480  LOAD_CONST               5
              482  BINARY_TRUE_DIVIDE
              484  LOAD_FAST                'text'
              486  LOAD_FAST                'color'
              488  LOAD_CONST               ('color',)
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              492  POP_TOP          
            494_0  COME_FROM           460  '460'

 L.1278       494  LOAD_GLOBAL              _plt
              496  LOAD_METHOD              show
              498  CALL_METHOD_0         0  ''
              500  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 498


def transformertest(Poc=False, Voc=False, Ioc=False, Psc=False, Vsc=False, Isc=False):
    """
    Transformer Rated Test Evaluator
    
    This function will determine the non-ideal circuit components of
    a transformer (Req and Xeq, or Rc and Xm) given the test-case
    parameters for the open-circuit test and/or the closed-circuit
    test. Requires one or both of two sets: { Poc, Voc, Ioc }, or
    { Psc, Vsc, Isc }.
    All values given must be given as absolute value, not complex.
    All values returned are given with respect to primary.
    
    Parameters
    ----------
    Poc:    float, optional
            The open-circuit measured power (real power), default=None
    Voc:    float, optional
            The open-circuit measured voltage (measured on X),
            default=None
    Ioc:    float, optional
            The open-circuit measured current (measured on primary),
            default=None
    Psc:    float, optional
            The short-circuit measured power (real power), default=None
    Vsc:    float, optional
            The short-circuit measured voltage (measured on X),
            default=None
    Isc:    float, optional
            The short-circuit measured current (measured on X),
            default=None
    
    Returns
    -------
    {Req,Xeq,Rc,Xm}:    Given all optional args
    {Rc, Xm}:           Given open-circuit parameters
    {Req, Xeq}:         Given short-circuit parameters
    """
    SC = False
    OC = False
    if Poc != None:
        if Voc != None:
            if Ioc != None:
                PF = Poc / (Voc * Ioc)
                Y = _c.rect(Ioc / Voc, -_np.arccos(PF))
                Rc = 1 / Y.real
                Xm = -1 / Y.imag
                OC = True
    if Psc != None:
        if Vsc != None:
            if Isc != None:
                PF = Psc / (Vsc * Isc)
                Zeq = _c.rect(Vsc / Isc, _np.arccos(PF))
                Req = Zeq.real
                Xeq = Zeq.imag
                SC = True
    if OC:
        if SC:
            return (
             Req, Xeq, Rc, Xm)
    if OC:
        return (
         Rc, Xm)
    if SC:
        return (
         Req, Xeq)
    print('An Error Was Encountered.\nNot enough arguments were provided.')


def phasorplot(phasor, title='Phasor Diagram', legend=False, bg=None, colors=None, radius=None, linewidth=None, size=None, filename=None, plot=True, label=False, labels=False, tolerance=None):
    """
    Phasor Plotting Function
    
    This function is designed to plot a phasor-diagram with angles in degrees
    for up to 12 phasor sets. Phasors must be passed as a complex number set,
    (e.g. [ m+ja, m+ja, m+ja, ... , m+ja ] ).
    
    Parameters
    ----------
    phasor:     list of complex
                The set of phasors to be plotted.
    title:      string, optional
                The Plot Title, default="Phasor Diagram"
    legend:     bool, optional
                Control argument to enable displaying the legend, must be passed
                as an array or list of strings. `label` and `labels` are mimic-
                arguments and will perform similar operation, default=False
    bg:         string, optional
                Background-Color control, default="#d5de9c"
    radius:     float, optional
                The diagram radius, unless specified, automatically scales
    colors:     list of str, optional
                List of hexidecimal color strings denoting the line colors to use.
    filename:   string, optional
                String of filename, if set, will force function to save image.
    plot:       bool, optional
                Control argument to disable plotting. default=True
    size:       float, optional
                Control argument for figure size. default=None
    linewidth:  float, optional
                Control argument to declare the line thickness. default=None
    tolerance:  float, optional
                Minimum magnitude to plot, anything less than tolerance will be
                plotted as a single point at the origin, by default, the tolerance
                is scaled to be 1/25-th the maximum radius. To disable the tolerance,
                simply provide either False or -1.
    """
    try:
        len(phasor)
    except TypeError:
        phasor = [
         phasor]
    else:
        if colors == None:
            colors = [
             '#FF0000', '#800000', '#FFFF00', '#808000', '#00ff00', '#008000',
             '#00ffff', '#008080', '#0000ff', '#000080', '#ff00ff', '#800080']
        else:
            if radius == None:
                radius = _np.abs(phasor).max()
            elif tolerance == None:
                tolerance = radius / 25
            else:
                if tolerance == False:
                    tolerance = -1
            if bg == None:
                bg = '#FFFFFF'
            if label != False:
                legend = label
            if labels != False:
                legend = labels
            numphs = len(phasor)
            numclr = len(colors)
            if numphs > numclr:
                raise ValueError('ERROR: Too many phasors provided. Specify more line colors.')
            if size == None:
                width, height = _matplotlib.rcParams['figure.figsize']
                size = min(width, height)
            fig = _plt.figure(figsize=(size, size))
            ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, facecolor=bg)
            _plt.grid(True)
            _plt.title(title + '\n')
            handles = _np.array([])
            for i in range(numphs):
                mag, ang_r = _c.polar(phasor[i])
                if legend != False:
                    if mag > tolerance:
                        hand = _plt.arrow(0, 0, ang_r, mag, color=(colors[i]), label=(legend[i]),
                          linewidth=linewidth)
                    else:
                        hand = _plt.plot(0, 0, 'o', markersize=(linewidth * 3), label=(legend[i]),
                          color=(colors[i]))
                    handles = _np.append(handles, [hand])
                else:
                    _plt.arrow(0, 0, ang_r, mag, color=(colors[i]), linewidth=linewidth)
            else:
                if legend != False:
                    _plt.legend(handles, legend)
                ax.set_rmax(radius)
                ax.set_rmin(0)
                if filename != None:
                    if not any((sub in filename for sub in ('.png', '.jpg'))):
                        filename += '.png'
                    _plt.savefig(filename)
                if plot:
                    _plt.show()
                else:
                    _plt.close()


def nlinpf(PFtrue=False, PFdist=False, PFdisp=False):
    """
    Non-Linear Power Factor Evaluator
    
    This function is designed to evaluate one of three unknowns
    given the other two. These particular unknowns are the arguments
    and as such, they are described in the representative sections
    below.
    
    Parameters
    ----------
    PFtrue:     float, exclusive
                The "True" power-factor, default=None
    PFdist:     float, exclusive
                The "Distorted" power-factor, default=None
    PFdisp:     float, exclusive
                The "Displacement" power-factor, default=None
    
    Returns
    -------
    {unknown}:  This function will return the unknown variable from
                the previously described set of variables.
    """
    if PFtrue != None and PFdist != None and PFdisp != None:
        raise ValueError('ERROR: Too many constraints, no solution.')
    else:
        if PFdist != None:
            if PFdisp != None:
                return PFdist * PFdisp
        else:
            if PFtrue != None:
                if PFdisp != None:
                    return PFtrue / PFdisp
            if PFtrue != None and PFdist != None:
                return PFtrue / PFdist
        raise ValueError('ERROR: Function requires at least two arguments.')


def iscrl(V, Z, t=None, f=None, mxcurrent=True, alpha=None):
    """
    Short-Circuit-Current (ISC) Calculator
    
    The Isc-RL function (Short Circuit Current for RL Circuit)
    is designed to calculate the short-circuit current for an
    RL circuit.
    
    Parameters
    ----------
    V:          float
                The absolute magnitude of the voltage.
    Z:          float
                The complex value of the impedance. (R + jX)
    t:          float, optional
                The time at which the value should be calculated,
                should be specified in seconds, default=None
    f:          float, optional
                The system frequency, specified in Hz, default=None
    mxcurrent:  bool, optional
                Control variable to enable calculating the value at
                maximum current, default=True
    alpha:      float, optional
                Angle specification, default=None
    
    Returns
    -------
    Opt 1 - (Irms, IAC, K):     The RMS current with maximum DC
                                offset, the AC current magnitude,
                                and the asymmetry factor.
    Opt 2 - (i, iAC, iDC, T):   The Instantaneous current with
                                maximum DC offset, the instantaneous
                                AC current, the instantaneous DC
                                current, and the time-constant T.
    Opt 3 - (Iac):              The RMS current without DC offset.
    """
    if f != None:
        omega = 2 * _np.pi * f
    else:
        omega = None
    R = abs(Z.real)
    X = abs(Z.imag)
    theta = _np.arctan(X / R)
    if mxcurrent and alpha == None:
        alpha = theta - _np.pi / 2
    else:
        if mxcurrent and alpha != None:
            raise ValueError('ERROR: Inappropriate Arguments Provided.\nNot both mxcurrent and alpha can be provided.')
    if t != None:
        if f != None:
            if alpha == None:
                if omega == None:
                    tau = t / 0.016666666666666666
                    K = _np.sqrt(1 + 2 * _np.exp(-4 * _np.pi * tau / (X / R)))
                    IAC = abs(V / Z)
                    Irms = K * IAC
                    return (
                     Irms, IAC, K)
                elif alpha == None or omega == None:
                    raise ValueError('ERROR: Inappropriate Arguments Provided.')
                else:
                    omega = _np.radians(omega)
                    alpha = _np.radians(alpha)
                    theta = _np.radians(theta)
                    T = X / (2 * _np.pi * f * R)
                    iAC = _np.sqrt(2) * V / Z * _np.sin(omega * t + alpha - theta)
                    iDC = -_np.sqrt(2) * V / Z * _np.sin(alpha - theta) * _np.exp(-t / T)
                    i = iAC + iDC
                    return (
                     i, iAC, iDC, T)
            else:
                pass
    if not (t != None and f == None):
        if not t == None or f != None:
            raise ValueError('ERROR: Inappropriate Arguments Provided.\nMust provide both t and f or neither.')
        else:
            IAC = abs(V / Z)
            return Iac


def voltdiv(Vin, R1, R2, Rload=None):
    r"""
    Voltage Divider Function
    
    This function is designed to calculate the output
    voltage of a voltage divider given the input voltage,
    the resistances (or impedances) and the load resistance
    (or impedance) if present.
    
    .. math:: V_{out} = V_{in} * \frac{R_2}{R_1+R+2}
    
    .. math:: V_{out}=V_{in}*\frac{R_2||R_{load}}{R_1+(R_2||R_{load})}
    
    Parameters
    ----------
    Vin:    float
            The Input Voltage, may be real or complex
    R1:     float
            The top resistor of the divider (real or complex)
    R2:     float
            The bottom resistor of the divider, the one which
            the output voltage is measured across, may be
            either real or complex
    Rload:  float, optional
            The Load Resistor (or impedance), default=None
    
    Returns
    -------
    Vout:   float
            The Output voltage as measured across R2 and/or Rload
    """
    if Rload == None:
        Vout = Vin * R2 / (R1 + R2)
    else:
        Rp = parallelz((R2, Rload))
        Vout = Vin * Rp / (R1 + Rp)
    return Vout


def curdiv(Ri, Rset, Vin=None, Iin=None, Vout=False, combine=True):
    """
    Current Divider Function
    
    This function is disigned to accept the input current, or input
    voltage to a resistor (or impedance) network of parallel resistors
    (impedances) and calculate the current through a particular element.
    
    Parameters
    ----------
    Ri:         float
                The Particular Resistor of Interest, should not be included in
                the tuple passed to Rset.
    Rset:       float
                Tuple of remaining resistances (impedances) in network.
    Vin:        float, optional
                The input voltage for the system, default=None
    Iin:        float, optional
                The input current for the system, default=None
    Vout:       bool, optional
                Control argument to enable return of the voltage across the
                resistor (impedance) of interest (Ri)
    combine:    bool, optional
                Control argument to force resistance combination. default=True
    
    Returns
    -------
    Opt1 - Ii:          The Current through the resistor (impedance) of interest
    Opt2 - (Ii,Vi):     The afore mentioned current, and voltage across the
                        resistor (impedance) of interest
    """
    if not isinstance(Rset, tuple):
        Rset = (
         Rset,)
    elif combine:
        Rtot = parallelz(Rset + (Ri,))
    else:
        Rtot = parallelz(Rset)
    if Vin != None and Iin == None:
        Iin = Vin / Rtot
        Ii = Iin * Rtot / Ri
    else:
        if Vin == None and Iin != None:
            Ii = Iin * Rtot / Ri
        else:
            raise ValueError('ERROR: Too many or too few constraints provided.')
    if Vout:
        Vi = Ii * Ri
        return (Ii, Vi)
    return Ii


def instpower(P, Q, t, freq=60):
    r"""
    Instantaneous Power Function
    
    This function is designed to calculate the instantaneous power at a
    specified time t given the magnitudes of P and Q.
    
    .. math:: P_{inst} = P+P*cos(2*\omega*t)-Q*sin(2*\omega*t)
    
    Parameters
    ----------
    P:      float
            Magnitude of Real Power
    Q:      float
            Magnitude of Reactive Power
    t:      float
            Time at which to evaluate
    freq:   float, optional
            System frequency (in Hz), default=60
    
    Returns
    -------
    Pinst:  float
            Instantaneous Power at time t
    """
    w = 2 * _np.pi * freq
    Pinst = P + P * _np.cos(2 * w * t) - Q * _np.sin(2 * w * t)
    return Pinst


def dynetz(delta=None, wye=None, round=None):
    r"""
    Delta-Wye Impedance Converter
    
    This function is designed to act as the conversion utility
    to transform delta-connected impedance values to wye-
    connected and vice-versa.
    
    .. math:: 
       Z_{sum} = Z_{1/2} + Z_{2/3} + Z_{3/1}//
       Z_1 = \frac{Z_{1/2}*Z_{3/1}}{Z_{sum}}//
       Z_2 = \frac{Z_{1/2}*Z_{2/3}}{Z_{sum}}//
       Z_3 = \frac{Z_{2/3}*Z_{3/1}}{Z_{sum}}
    
    .. math::
       Z_{ms} = Z_1*Z_2 + Z_2*Z_3 + Z_3*Z_1//
       Z_{2/3} = \frac{Z_{ms}}{Z_1}//
       Z_{3/1} = \frac{Z_{ms}}{Z_2}//
       Z_{1/2} = \frac{Z_{ms}}{Z_3}
    
    Parameters
    ----------
    delta:  tuple of float, exclusive
            Tuple of the delta-connected impedance values as:
            { Z12, Z23, Z31 }, default=None
    wye:    tuple of float, exclusive
            Tuple of the wye-connected impedance valuse as:
            { Z1, Z2, Z3 }, default=None
    
    Returns
    -------
    delta-set:  tuple of float
                Delta-Connected impedance values { Z12, Z23, Z31 }
    wye-set:    tuple of float
                Wye-Connected impedance values { Z1, Z2, Z3 }
    """
    if delta != None:
        if wye == None:
            Z12, Z23, Z31 = delta
            Zsum = Z12 + Z23 + Z31
            Z1 = Z12 * Z31 / Zsum
            Z2 = Z12 * Z23 / Zsum
            Z3 = Z23 * Z31 / Zsum
            Zset = (Z1, Z2, Z3)
            if round != None:
                Zset = _np.around(Zset, round)
            return Zset
    if delta == None:
        if wye != None:
            Z1, Z2, Z3 = wye
            Zmultsum = Z1 * Z2 + Z2 * Z3 + Z3 * Z1
            Z23 = Zmultsum / Z1
            Z31 = Zmultsum / Z2
            Z12 = Zmultsum / Z3
            Zset = (Z12, Z23, Z31)
            if round != None:
                Zset = _np.around(Zset, round)
            return Zset
    raise ValueError('ERROR: Either delta or wye impedances must be specified.')


def powerflow(Vsend, Vrec, Zline):
    r"""
    Simple Power-Flow Calculator
    
    This function is designed to calculate the ammount of real
    power transferred from the sending end to the recieving end
    of an electrical line given the sending voltage (complex),
    the receiving voltage (complex) and the line impedance.
    
    .. math::
       P_{flow}=\frac{|V_{send}|*|V_{rec}|}{Z_{line}}*sin(\theta_{send}
       -\theta_{rec})
    
    Parameters
    ----------
    Vsend:      complex
                The sending-end voltage, should be complex
    Vrec:       complex
                The receiving-end voltage, should be complex
    Zline:      complex
                The line impedance, should be complex
    
    Returns
    -------
    pflow:      complex
                The power transferred from sending-end to
                receiving-end, positive values denote power
                flow from send to receive, negative values
                denote vice-versa.
    """
    Vs = abs(Vsend)
    ds = _c.phase(Vsend)
    Vr = abs(Vrec)
    dr = _c.phase(Vrec)
    pflow = Vs * Vr / Zline * _np.sin(ds - dr)
    return pflow


def zsource(S, V, XoR, Sbase=None, Vbase=None, perunit=True):
    """
    Source Impedance Calculator
    
    Used to calculate the source impedance given the apparent power
    magnitude and the X/R ratio.
    
    Parameters
    ----------
    S:          float
                The (rated) apparent power magnitude of the source.
                This may also be refferred to as the "Short-Circuit MVA"
    V:          float
                The (rated) voltage of the source terminals, not
                specifically identified as either Line-to-Line or Line-to-
                Neutral.
    XoR:        float
                The X/R ratio rated for the source, may optionally be a list
                of floats to accomidate sequence impedances or otherwise.
    Sbase:      float, optional
                The per-unit base for the apparent power. If set to
                None, will automatically force Sbase to equal S.
                If set to True will treat S as the per-unit value.
    Vbase:      float, optional
                The per-unit base for the terminal voltage. If set to
                None, will automaticlaly force Vbase to equal V. If
                set to True, will treat V as the per-unit value.
    perunit:    boolean, optional
                Control value to enable the return of output in per-
                unit base. default=True
    
    Returns
    -------
    Zsource_pu: complex
                The per-unit evaluation of the source impedance.
                Will be returned in ohmic (not per-unit) value if
                *perunit* argument is specified as False.
    """
    if Vbase == None:
        Vbase = V
    else:
        if Sbase == None:
            Sbase = S
        else:
            if Vbase == True:
                Vbase = 1
            if Sbase == True:
                Sbase = 1
            Spu = S / Sbase
            Vpu = V / Vbase
            Zsource_pu = Vpu ** 2 / Spu
            nu = _np.degrees(_np.arctan(XoR))
            if isinstance(nu, (list, _np.ndarray)):
                Zsource_pu = []
                for angle in nu:
                    Zsource_pu.append(phasor(Zsource_pu, angle))

            else:
                Zsource_pu = phasor(Zsource_pu, nu)
        Zsource = perunit or Zsource_pu * Vbase ** 2 / Sbase
        return Zsource
    return Zsource_pu


def zdecompose(Zmag, XoR):
    """
    Impedance Decomposition Function
    
    A function to decompose the impedance magnitude into its
    corresponding resistance and reactance using the X/R ratio.
    
    It is possible to "neglect" R, or make it a very small number;
    this is done by setting the X/R ratio to a very large number
    (X being much larger than R).
    
    Parameters
    ----------
    Zmag:       float
                The magnitude of the impedance.
    XoR:        float
                The X/R ratio (reactance over impedance).
    
    Returns
    -------
    R:          float
                The resistance (in ohms)
    X:          float
                The reactance (in ohms)
    """
    R = Zmag / _np.sqrt(XoR ** 2 + 1)
    X = R * XoR
    return (
     R, X)


def hp_to_watts(hp):
    r"""
    Horsepower to Watts Formula
    
    Calculates the power (in watts) given the
    horsepower.
    
    .. math:: P_{\text{watts}}=P_{\text{horsepower}}\cdot745.699872
    
    Same as `watts`.
    
    Parameters
    ----------
    hp:         float
                The horspower to compute.
    
    Returns
    -------
    watts:      float
                The power in watts.
    """
    return hp * 745.699872


watts = hp_to_watts

def watts_to_hp(watts):
    r"""
    Watts to Horsepower Function
    
    Calculates the power (in horsepower) given
    the power in watts.
    
    .. math:: P_{\text{horsepower}}=\frac{P_{\text{watts}}}{745.699872}
    
    Same as `horsepower`.
    
    Parameters
    ----------
    watts:      float
                The wattage to compute.
    
    Returns
    -------
    hp:         float
                The power in horsepower.
    """
    return watts / 745.699872


horsepower = watts_to_hp

def powerimpedance(S, V, PF=None, parallel=False, terms=False):
    r"""
    Impedance from Apparent Power Formula
    
    Function to determine the ohmic resistance/reactance
    (impedance) represented by the apparent power (S).
    
    .. math:: Z = \frac{V^2}{S}
       :label: series
    
    .. math:: Z = \frac{V^2}{(3*S)}
       :label: parallel
    
    This function can evaluate the component values for
    both series :eq:`series` and parallel :eq:`parallel`
    connected circuits.
    
    Parameters
    ----------
    S:          complex, float
                The apparent power of the passive element,
                may be purely resistive or purely reactive.
    V:          float
                The operating voltage of the passive element.
                Note that this is specifically not Line-Line or
                Line-Neutral voltage, rather the voltage of the
                element.
    PF:         float, optional
                The operating Power-Factor, should be specified
                if S is given as a float (not complex). Positive
                PF correlates to lagging, negative to leading.
                default=None
    parallel:   bool, optional
                Control point to specify whether the ohmic
                impedance should be returned as series components
                (False opt.) or parallel components (True opt.).
    terms:      bool, optional
                Control point to specify whether return should
                be made as resistance and reactance, or simply
                the complex impedance. Setting of False will
                return complex impedance, setting of True will
                return individual components (R, X).
    
    Returns
    -------
    R:          float
                The ohmic resistance required to consume the
                specified apparent power (S) at the rated
                voltage (V).
    X:          float
                The ohmic reactance required to consume the
                specified apparent power (S) at the rated
                voltage (V).
    """
    V = abs(V)
    if isinstance(S, complex) or PF != None:
        if PF != None:
            P, Q, S, PF = powerset(S=S, PF=PF)
        else:
            P = S.real
            Q = S.imag
        if parallel:
            R = V ** 2 / (3 * P)
            X = V ** 2 / (3 * Q)
        else:
            R = V ** 2 / P
            X = V ** 2 / Q
        if terms:
            return (
             R, X)
        return R + complex(0.0, 1.0) * X
    R = V ** 2 / S
    return R


def coldjunction(Tcj, coupletype='K', To=None, Vo=None, P1=None, P2=None, P3=None, P4=None, Q1=None, Q2=None, round=None):
    """
    Thermocouple Cold-Junction Formula
    
    Function to calculate the expected cold-junction-voltage given
    the temperature at the cold-junction.
    
    Parameters
    ----------
    Tcj:        float
                The temperature (in degrees C) that the junction is
                currently subjected to.
    coupletype: string, optional
                Thermocouple Type, may be one of (B,E,J,K,N,R,S,T), default="K"
    To:         float, optional
                Temperature Constant used in Polynomial.
    Vo:         float, optional
                Voltage Constant used in Polynomial.
    P1:         float, optional
                Polynomial constant.
    P2:         float, optional
                Polynomial constant.
    P3:         float, optional
                Polynomial constant.
    P4:         float, optional
                Polynomial constant.
    Q1:         float, optional
                Polynomial constant.
    Q2:         float, optional
                Polynomial constant.
    Q3:         float, optional
                Polynomial constant.
    round:      int, optional
                Control input to specify how many decimal places the result
                should be rounded to, default=1.
    
    Returns
    -------
    Vcj:        float
                The calculated cold-junction-voltage in volts.
    """
    coupletype = coupletype.upper()
    if coupletype == 'B':
        raise 0 < Tcj and Tcj < 70 or ValueError('Temperature out of range.')
    else:
        raise -20 < Tcj and Tcj < 70 or ValueError('Temperature out of range.')
    lookup = ['B', 'E', 'J', 'K', 'N', 'R', 'S', 'T']
    if coupletype not in lookup:
        raise ValueError('Invalid Thermocouple Type')
    index = lookup.index(coupletype)
    constants = {'To':[
      42.0, 25.0, 25.0, 25.0, 7.0, 25.0, 25.0, 25.0], 
     'Vo':[
      0.00033933898, 1.4950582, 1.2773432, 1.0003453, 0.18210024, 0.14067016, 0.14269163, 0.99198279], 
     'P1':[
      0.00021196684, 0.060958443, 0.051744084, 0.040514854, 0.026228256, 0.0059330356, 0.0059829057, 0.040716564], 
     'P2':[
      3.380125e-06, -0.00027351789, -5.4138663e-05, -3.8789638e-05, -0.00015485539, 2.7736904e-05, 4.5292259e-06, 0.00071170297], 
     'P3':[
      -1.4793289e-07, -1.9130146e-05, -2.2895769e-06, -2.8608478e-06, 2.1366031e-06, -1.0819644e-06, -1.3380281e-06, 6.8782631e-07], 
     'P4':[
      -3.3571424e-09, -1.394884e-08, -7.7947143e-10, -9.5367041e-10, 9.2047105e-10, -2.3098349e-09, -2.3742577e-09, 4.3295061e-11], 
     'Q1':[
      -0.01092041, -0.0052382378, -0.0015173342, -0.0013948675, -0.0064070932, 0.0026146871, -0.0010650446, 0.016458102], 
     'Q2':[
      -0.00049782932, -0.00030970168, -4.2314514e-05, -6.7976627e-05, 8.2161781e-05, -0.00018621487, -0.0002204242, 0.0]}
    if To == None:
        To = constants['To'][index]
    if Vo == None:
        Vo = constants['Vo'][index]
    if P1 == None:
        P1 = constants['P1'][index]
    if P2 == None:
        P2 = constants['P2'][index]
    if P3 == None:
        P3 = constants['P3'][index]
    if P4 == None:
        P4 = constants['P4'][index]
    if Q1 == None:
        Q1 = constants['Q1'][index]
    if Q2 == None:
        Q2 = constants['Q2'][index]
    tx = Tcj - To
    num = tx * (P1 + tx * (P2 + tx * (P3 + P4 * tx)))
    den = 1 + tx * (Q1 + Q2 * tx)
    Vcj = Vo + num / den
    if round != None:
        Vcj = _np.around(Vcj, round)
    return Vcj * m


def thermocouple(V, coupletype='K', fahrenheit=False, cjt=None, To=None, Vo=None, P1=None, P2=None, P3=None, P4=None, Q1=None, Q2=None, Q3=None, round=1):
    """
    Thermocouple Temperature Calculator
    
    Utilizes polynomial formula to calculate the temperature being monitored
    by a thermocouple. Allows for various thermocouple types (B,E,J,K,N,R,S,T)
    and various cold-junction-temperatures.
    
    Parameters
    ----------
    V:          float
                Measured voltage (in Volts)
    coupletype: string, optional
                Thermocouple Type, may be one of (B,E,J,K,N,R,S,T), default="K"
    fahrenheit: bool, optional
                Control to enable return value as Fahrenheit instead of Celsius,
                default=False
    cjt:        float, optional
                Cold-Junction-Temperature
    To:         float, optional
                Temperature Constant used in Polynomial.
    Vo:         float, optional
                Voltage Constant used in Polynomial.
    P1:         float, optional
                Polynomial constant.
    P2:         float, optional
                Polynomial constant.
    P3:         float, optional
                Polynomial constant.
    P4:         float, optional
                Polynomial constant.
    Q1:         float, optional
                Polynomial constant.
    Q2:         float, optional
                Polynomial constant.
    Q3:         float, optional
                Polynomial constant.
    round:      int, optional
                Control input to specify how many decimal places the result
                should be rounded to, default=1.
    
    Returns
    -------
    T:          float
                The temperature (by default in degrees C, but optionally in
                degrees F) as computed by the function.
    """
    coupletype = coupletype.upper()
    V = V / m
    if cjt != None:
        Vcj = coldjunction(cjt, coupletype, To, Vo, P1, P2, P3, P4, Q1, Q2, round)
        V += Vcj / m
    else:
        lookup = [
         'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T']
        if coupletype not in lookup:
            raise ValueError('Invalid Thermocouple Type')
        else:
            voltages = {'J':[
              -8.095, 0, 21.84, 45.494, 57.953, 69.553], 
             'K':[
              -6.404, -3.554, 4.096, 16.397, 33.275, 69.553], 
             'B':[
              0.291, 2.431, 13.82, None, None, None], 
             'E':[
              -9.835, -5.237, 0.591, 24.964, 53.112, 76.373], 
             'N':[
              -4.313, 0, 20.613, 47.513, None, None], 
             'R':[
              -0.226, 1.469, 7.461, 14.277, 21.101, None], 
             'S':[
              -0.236, 1.441, 6.913, 12.856, 18.693, None], 
             'T':[
              -6.18, -4.648, 0, 9.288, 20.872, None]}
            vset = voltages[coupletype]
            if V < vset[0] * m:
                raise ValueError('Voltage Below Lower Bound')
            else:
                if vset[0] <= V < vset[1]:
                    select = 0
                else:
                    pass
            if vset[1] <= V < vset[2]:
                select = 1
            else:
                if vset[2] <= V < vset[3]:
                    select = 2
                else:
                    if vset[3] <= V < vset[4]:
                        select = 3
                    else:
                        if vset[4] <= V <= vset[5]:
                            select = 4
                        else:
                            if vset[5] < V:
                                raise ValueError('Voltage Above Upper Bound')
                            else:
                                raise ValueError('Internal Error!')
    data = {'J':[
      [
       -64.936529, 250.66947, 649.50262, 925.1055, 1051.1294],
      [
       -3.1169773, 13.592329, 36.040848, 53.433832, 60.956091],
      [
       22.133797, 18.014787, 16.593395, 16.243326, 17.156001],
      [
       2.0476437, -0.065218881, 0.7300959, 0.92793267, -2.5931041],
      [
       -0.46867532, -0.012179108, 0.024157343, 0.0064644193, -0.058339803],
      [
       -0.036673992, 0.00020061707, 0.0012787077, 0.0020464414, 0.019954137],
      [
       0.11746348, -0.0039494552, 0.049172861, 0.052541788, -0.15305581],
      [
       -0.020903413, -0.00073728206, 0.001681381, 0.00013682959, -0.0029523967],
      [
       -0.0021823704, 1.6679731e-05, 7.6067922e-05, 0.00013454746, 0.0011340164]], 
     'K':[
      [
       -121.47164, -8.7935962, 310.18976, 605.72562, 1018.4705],
      [
       -4.1790858, -0.34489914, 12.631386, 25.148718, 41.993851],
      [
       36.069513, 25.678719, 24.061949, 23.539401, 25.783239],
      [
       30.722076, -0.49887904, 4.0158622, 0.046547228, -1.8363403],
      [
       7.791386, -0.44705222, 0.26853917, 0.0134444, 0.056176662],
      [
       0.52593991, -0.044869203, -0.0097188544, 0.00059236853, 0.000185324],
      [
       0.93939547, 0.00023893439, 0.16995872, 0.00083445513, -0.074803355],
      [
       0.27791285, -0.02039775, 0.011413069, 0.00046121445, 0.002384186],
      [
       0.025163349, -0.0018424107, -0.00039275155, 2.5488122e-05, 0.0]], 
     'B':[
      [
       500.0, 1246.1474],
      [
       1.24179, 7.2701221],
      [
       198.58097, 94.321033],
      [
       24.284248, 7.3899296],
      [
       -97.27164, -0.15880987],
      [
       -15.701178, 0.012681877],
      [
       0.31009445, 0.10113834],
      [
       -0.50880251, -0.0016145962],
      [
       -0.16163342, -4.1086314e-06]], 
     'E':[
      [
       -117.21668, -50.0, 250.146, 601.3989, 804.35911],
      [
       -5.9901698, -2.7871777, 17.191713, 45.206167, 61.359178],
      [
       23.647275, 19.022736, 13.115522, 12.399357, 12.759508],
      [
       12.807377, -1.7042725, 1.1780364, 0.43399963, -1.1116072],
      [
       2.0665069, -0.35195189, 0.036422433, 0.0091967085, 0.035332536],
      [
       0.086513472, 0.0047766102, 0.00039584261, 0.00016901585, 3.308038e-05],
      [
       0.5899586, -0.06537976, 0.093112756, 0.03442468, -0.088196889],
      [
       0.10960713, -0.021732833, 0.0029804232, 0.00069741215, 0.0028497415],
      [
       0.0061769588, 0.0, 3.3263032e-05, 1.2946992e-05, 0.0]], 
     'N':[
      [
       -59.610511, 315.34505, 1034.0172],
      [
       -1.5, 9.8870997, 37.565475],
      [
       42.021322, 27.988676, 26.029492],
      [
       4.7244037, 1.5417343, -0.60783095],
      [
       -6.1153213, -0.14689457, -0.0097742562],
      [
       -0.99980337, -0.0068322712, -3.3148813e-06],
      [
       0.16385664, 0.062600036, -0.025351881],
      [
       -0.14994026, -0.0051489572, -0.00038746827],
      [
       -0.030810372, -0.00028835863, 1.7088177e-06]], 
     'R':[
      [
       130.54315, 541.88181, 1038.2132, 1567.6133],
      [
       0.8833309, 4.9312886, 11.014763, 18.39791],
      [
       125.57377, 90.20819, 74.669343, 71.646299],
      [
       139.00275, 6.1762254, 3.4090711, -1.0866763],
      [
       33.035469, -1.2279323, -0.14511205, -2.0968371],
      [
       -0.85195924, 0.014873153, 0.0063077387, -0.76741168],
      [
       1.2232896, 0.087670455, 0.056880253, -0.019712341],
      [
       0.35603023, -0.012906694, -0.0020512736, -0.029903595],
      [
       0.0, 0.0, 0.0, -0.010766878]], 
     'S':[
      [
       137.9263, 476.73468, 979.46589, 1601.0461],
      [
       0.93395024, 4.0037367, 9.3508283, 16.789315],
      [
       127.61836, 101.74512, 87.12673, 84.315871],
      [
       110.8905, -8.9306371, -2.3139202, -10.185043],
      [
       19.898457, -4.2942435, -0.032682118, -4.6283954],
      [
       0.096152996, 0.20453847, 0.0046090022, -1.0158749],
      [
       0.96545918, -0.071227776, -0.01429979, -0.12877783],
      [
       0.2081385, -0.044618306, -0.0012289882, -0.055802216],
      [
       0.0, 0.0016822887, 0.0, -0.012146518]], 
     'T':[
      [
       -192.43, -60.0, 135.0, 300.0],
      [
       -5.4798963, -2.152835, 5.95886, 14.86178],
      [
       59.572141, 30.449332, 20.325591, 17.214707],
      [
       1.9675733, -1.294656, 3.3013079, -0.93862713],
      [
       -78.176011, -3.0500735, 0.12638462, -0.073509066],
      [
       -10.96328, -0.19226856, -0.00082883695, 0.0002957614],
      [
       0.27498092, 0.0069877863, 0.17595577, -0.048095795],
      [
       -1.3768944, -0.10596207, 0.0079740521, -0.0047352054],
      [
       -0.45209805, -0.010774995, 0.0, 0.0]]}
    if To == None:
        To = data[coupletype][0][select]
    if Vo == None:
        Vo = data[coupletype][1][select]
    if P1 == None:
        P1 = data[coupletype][2][select]
    if P2 == None:
        P2 = data[coupletype][3][select]
    if P3 == None:
        P3 = data[coupletype][4][select]
    if P4 == None:
        P4 = data[coupletype][5][select]
    if Q1 == None:
        Q1 = data[coupletype][6][select]
    if Q2 == None:
        Q2 = data[coupletype][7][select]
    if Q3 == None:
        Q3 = data[coupletype][8][select]
    num = (V - Vo) * (P1 + (V - Vo) * (P2 + (V - Vo) * (P3 + P4 * (V - Vo))))
    den = 1 + (V - Vo) * (Q1 + (V - Vo) * (Q2 + Q3 * (V - Vo)))
    temp = To + num / den
    if fahrenheit:
        temp = temp * 9 / 5 + 32
    temp = _np.around(temp, round)
    return temp


def rtdtemp(RT, rtdtype='PT100', fahrenheit=False, Rref=None, Tref=None, a=None, round=1):
    """
    RTD Temperature Calculator
    
    Evaluates the measured temperature based on the measured resistance
    and the RTD type.
    
    Parameters
    ----------
    RT:         float
                The measured resistance (in ohms).
    rtdtype:    string
                RTD Type string, may be one of: (PT100, PT1000,
                CU100, NI100, NI120, NIFE), default=PT100
    fahrenheit: bool, optional
                Control parameter to force return into degrees
                fahrenheit, default=False
    Rref:       float, optional
                Resistance reference, commonly used if non-standard
                RTD type being used. Specified in ohms.
    Tref:       float, optional
                Temperature reference, commonly used if non-standard
                RTD type being used. Specified in degrees Celsius.
    a:          float, optional
                Scaling value, commonly used if non-standard
                RTD type being used.
    round:      int, optional
                Control argument to specify number of decimal points
                in returned value.
    
    Returns
    -------
    temp:       float
                Calculated temperature, defaults to degrees Celsius.
    """
    types = {'PT100':[
      100, 0.00385], 
     'PT1000':[
      1000, 0.00385], 
     'CU100':[
      100, 0.00427], 
     'NI100':[
      100, 0.00618], 
     'NI120':[
      120, 0.00672], 
     'NIFE':[
      604, 0.00518]}
    if Rref == None:
        Rref = types[rtdtype][0]
    if Tref == None:
        Tref = 0
    if a == None:
        a = types[rtdtype][1]
    num = RT - Rref + Rref * a * Tref
    den = Rref * a
    temp = num / den
    if fahrenheit:
        temp = temp * 9 / 5 + 32
    temp = _np.around(temp, round)
    return temp


def vcapdischarge(t, Vs, R, C):
    r"""
    Discharging Capacitor Function
    
    Function to calculate the voltage of a
    capacitor that is discharging given the time.
    
    .. math:: V_c=V_s*e^{\frac{-t}{R*C}}
    
    Parameters
    ----------
    t:          float
                The time at which to calculate the voltage.
    Vs:         float
                The starting voltage for the capacitor.
    R:          float
                The ohmic value of the resistor being used
                to discharge.
    C:          float
                Capacitive value (in Farads).
    
    Returns
    -------
    Vc:         float
                The calculated voltage of the capacitor.
    """
    Vc = Vs * _np.exp(-t / (R * C))
    return Vc


def vcapcharge(t, Vs, R, C):
    r"""
    Charging Capacitor Voltage
    
    Function to calculate the voltage of a
    capacitor that is charging given the time.
    
    .. math:: V_c=V_s*(1-e^{\frac{-t}{R*C}})
    
    Parameters
    ----------
    t:          float
                The time at which to calculate the voltage.
    Vs:         float
                The charging voltage for the capacitor.
    R:          float
                The ohmic value of the resistor being used
                to discharge.
    C:          float
                Capacitive value (in Farads).
    
    Returns
    -------
    Vc:         float
                The calculated voltage of the capacitor.
    """
    Vc = Vs * (1 - _np.exp(-t / (R * C)))
    return Vc


def captransfer(t, Vs, R, Cs, Cd):
    """
    Capacitor Energy Transfer Function
    
    Calculate the voltage across a joining
    resistor (R) that connects Cs and Cd, the
    energy-source and -destination capacitors,
    respectively. Calculate the final voltage
    across both capacitors.
    
    Parameters
    ----------
    t:          float
                Time at which to calculate resistor voltage.
    Vs:         float
                Initial voltage across source-capacitor (Cs).
    R:          float
                Value of resistor that connects capacitors.
    Cs:         float
                Source capacitance value in Farads.
    Cd:         float
                Destination capacitance value in Farads.
    
    Returns
    -------
    rvolt:      float
                Voltage across the resistor at time t.
    vfinal:     float
                Final voltage that both capacitors settle to.
    """
    tau = R * Cs * Cd / (Cs + Cd)
    rvolt = Vs * _np.exp(-t / tau)
    vfinal = Vs * Cs / (Cs + Cd)
    return (rvolt, vfinal)


def inductorenergy(L, I):
    r"""
    Energy Stored in Inductor Formula
    
    Function to calculate the energy stored in an inductor
    given the inductance (in Henries) and the current.
    
    .. math:: E=\frac{1}{2}*L*I^2
    
    Parameters
    ----------
    L:          float
                Inductance Value (in Henries)
    I:          float
                Current traveling through inductor.
    
    Returns
    -------
    E:          float
                The energy stored in the inductor (in Joules).
    """
    return 0.5 * L * I ** 2


def inductorcharge(t, Vs, R, L):
    r"""
    Charging Inductor Formula
    
    Calculates the Voltage and Current of an inductor
    that is charging/storing energy.
    
    .. math::
       V_L = V_s*e^{\frac{-R*t}{L}}//
       I_L = \frac{V_s}{R}*(1-e^{\frac{-R*t}{L}})
    
    Parameters
    ----------
    t:          float
                Time at which to calculate voltage and current.
    Vs:         float
                Charging voltage across inductor and resistor.
    R:          float
                Resistance related to inductor.
    L:          float
                Inductance value in Henries.
    
    Returns
    -------
    Vl:         float
                Voltage across inductor at time t.
    Il:         float
                Current through inductor at time t.
    """
    Vl = Vs * _np.exp(-R * t / L)
    Il = Vs / R * (1 - _np.exp(-R * t / L))
    return (Vl, Il)


def capbacktoback(C1, C2, Lm, VLN=None, VLL=None):
    """
    Back to Back Capacitor Transient Current Calculator
    
    Function to calculate the maximum current and the 
    frequency of the inrush current of two capacitors
    connected in parallel when one (energized) capacitor
    is switched into another (non-engergized) capacitor.
    
    .. note:: This formula is only valid for three-phase systems.
    
    Parameters
    ----------
    C1:         float
                The capacitance of the
    VLN:        float, exclusive
                The line-to-neutral voltage experienced by
                any one of the (three) capacitors in the
                three-phase capacitor bank.
    VLL:        float, exclusive
                The line-to-line voltage experienced by the
                three-phase capacitor bank.
    
    Returns
    -------
    imax:       float
                Maximum Current Magnitude during Transient
    ifreq:      float
                Transient current frequency
    """
    imax = _np.sqrt(0.6666666666666666) * VLL * _np.sqrt(C1 * C2 / ((C1 + C2) * Lm))
    ifreq = 1 / (2 * _np.pi * _np.sqrt(Lm * (C1 * C2) / (C1 + C2)))
    return (imax, ifreq)


def inductordischarge(t, Io, R, L):
    r"""
    Discharging Inductor Formula
    
    Calculates the Voltage and Current of an inductor
    that is discharging its stored energy.
    
    .. math::
       I_L=I_0*e^{\frac{-R*t}{L}}//
       V_L=I_0*R*(1-e^{\frac{-R*t}{L}})
    
    Parameters
    ----------
    t:          float
                Time at which to calculate voltage and current.
    Io:         float
                Initial current traveling through inductor.
    R:          float
                Resistance being discharged to.
    L:          float
                Inductance value in Henries.
    
    Returns
    -------
    Vl:         float
                Voltage across inductor at time t.
    Il:         float
                Current through inductor at time t.
    """
    Il = Io * _np.exp(-R * t / L)
    Vl = Io * R * (1 - _np.exp(-R * t / L))
    return (Vl, Il)


def farads(VAR, V, freq=60):
    r"""
    Capacitance from Apparent Power Formula
    
    Function to calculate the required capacitance
    in Farads to provide the desired power rating
    (VARs).
    
    .. math:: C = \frac{VAR}{2*\pi*freq*V^2}
    
    Parameters
    ----------
    VAR:        float
                The rated power to meet.
    V:          float
                The voltage across the capacitor;
                not described as VLL or VLN, merely
                the capacitor voltage.
    freq:       float, optional
                The System frequency
    
    Returns
    -------
    C:          float
                The evaluated capacitance (in Farads).
    """
    return VAR / (2 * _np.pi * freq * V ** 2)


def capenergy(C, v):
    r"""
    Capacitor Energy Formula
    
    A simple function to calculate the stored voltage (in Joules)
    in a capacitor with a charged voltage.
    
    .. math:: E=\frac{1}{2}*C*V^2
    
    Parameters
    ----------
    C:          float
                Capacitance in Farads.
    V:          float
                Voltage across capacitor.
    
    Returns
    -------
    energy:     float
                Energy stored in capacitor (Joules).
    """
    energy = 0.5 * C * V ** 2
    return energy


def loadedvcapdischarge(t, vo, C, P):
    r"""
    Loaded Capacitor Discharge Formula
    
    Returns the voltage of a discharging capacitor after time (t - 
    seconds) given initial voltage (vo - volts), capacitor size
    (cap - Farads), and load (P - Watts).
    
    .. math:: V_t=\sqrt{v_0^2-2*P*\frac{t}{C}}
    
    Parameters
    ----------
    t:          float
                Time at which to calculate voltage.
    vo:         float
                Initial capacitor voltage.
    C:          float
                Capacitance (in Farads)
    P:          float
                Load power consumption (in Watts).
    
    Returns
    -------
    Vt:         float
                Voltage of capacitor at time t.
    """
    Vt = _np.sqrt(vo ** 2 - 2 * P * t / C)
    return Vt


def timedischarge(Vinit, Vmin, C, P, dt=0.001, RMS=True, Eremain=False):
    """
    Capacitor Discharge Time Formula
    
    Returns the time to discharge a capacitor to a specified
    voltage given set of inputs.
    
    Parameters
    ----------
    Vinit:      float
                Initial Voltage (in volts)
    Vmin:       float
                Final Voltage (the minimum allowable voltage) (in volts)
    C:          float
                Capacitance (in Farads)
    P:          float
                Load Power being consumed (in Watts)
    dt:         float, optional
                Time step-size (in seconds) (defaults to 1e-3 | 1ms)
    RMS:        bool, optional
                if true converts RMS Vin to peak
    Eremain:    bool, optional
                if true: also returns the energy remaining in cap
    
    Returns
    -------
    Returns time to discharge from Vinit to Vmin in seconds.
    May also return remaining energy in capacitor if Eremain=True
    """
    t = 0
    if RMS:
        vo = Vinit * _np.sqrt(2)
    else:
        vo = Vinit
    vc = loadedvcapdischargetvoCP
    while vc >= Vmin:
        t = t + dt
        vcp = vc
        vc = loadedvcapdischargetvoCP

    if Eremain:
        E = energy(C, vcp)
        return (t - dt, E)
    return t - dt


def rectifiercap(Iload, fswitch, dVout):
    r"""
    Rectifier Capacitor Formula
    
    Returns the capacitance (in Farads) for a needed capacitor in
    a rectifier configuration given the system frequency (in Hz),
    the load (in amps) and the desired voltage ripple.
    
    .. math:: C=\frac{I_{load}}{f_{switch}*\Delta V_{out}}
    
    Parameters
    ----------
    Iload:      float
                The load current that must be met.
    fswitch:    float
                The switching frequency of the system.
    dVout:      float
                Desired delta-V on the output.
    
    Returns
    -------
    C:          float
                Required capacitance (in Farads) to meet arguments.
    """
    C = Iload / (fswitch * dVout)
    return C


def vscdcbus(VLL, Zs, P, Q=0, mmax=0.8, debug=False):
    """
    Voltage Sourced Converter DC Bus Voltage Function
    
    The purpose of this function is to calculate the
    required DC-bus voltage for a Voltage-Sourced-
    Converter (VSC) given the desired P/Q parameters
    and the known source impedance (Vs) of the VSC.
    
    Parameters
    ----------
    VLL:    complex
            Line-to-Line voltage on the line-side of
            the source impedance.
    Zs:     complex
            The source impedance of the VSC
    P:      float
            The desired real-power output
    Q:      float, optional
            The desired reactive-power output, default=0
    mmax:   float, optional
            The maximum of the m value for the converter
            default=0.8
    debug:  bool, optional
            Control value to enable printing stages of
            the calculation, default=False
            
    Return
    ------
    VDC:    float
            The DC bus voltage.
    """
    Iload = _np.conj((P + complex(0.0, 1.0) * Q) / (VLL * _np.sqrt(3)))
    Vtln = abs(VLL / _np.sqrt(3) + Iload * Zs)
    Vtpk = _np.sqrt(2) * Vtln
    VDC = 2 * Vtpk / mmax
    if debug:
        print('Iload', Iload)
        print('Vtln', Vtln)
        print('Vtpk', Vtpk)
        print('VDC', VDC)
    return VDC


def vscgains(Rs, Ls, tau=0.005, freq=60):
    """
    Voltage Sourced Converter Gains Calculator
    
    This function is designed to calculate the kp, ki,
    and omega-not-L values for a Phase-Lock-Loop based VSC.
    
    Parameters
    ----------
    Rs:     float
            The equiv-resistance (in ohms) of the VSC
    Ls:     float
            The equiv-inductance (in Henrys) of the VSC
    tau:    float, optional
            The desired time-constant, default=0.005
    freq:   float, optional
            The system frequency (in Hz), default=60
    
    Returns
    -------
    kp:     float
            The Kp-Gain Value
    ki:     float
            The Ki-Gain Value
    w0L:    float
            The omega-not-L gain value
    """
    kp = Ls / tau
    ki = kp * Rs / Ls
    w0L = 2 * _np.pi * freq * Ls
    return (kp, ki, w0L)


def convbar(h, x, outline=True):
    """
    Convolution Bar-Graph Plotter Function
    
    Generates plots of each of two input arrays as bar-graphs, then
    generates a convolved bar-graph of the two inputs to demonstrate
    and illustrate convolution, typically for an educational purpose.
    
    Parameters
    ----------
    h:      numpy.ndarray
            Impulse Response - Given as Array (Prefferably Numpy Array)
    x:      numpy.ndarray
            Input Function - Given as Array (Prefferably Numpy Array)
    """
    M = len(h)
    t = _np.arange(M)
    _plt.subplot(121)
    if outline:
        _plt.plot(t, h, color='red')
    _plt.bar(t, h, color='black')
    _plt.xticks([0, 5, 9])
    _plt.ylabel('h')
    _plt.title('Impulse Response')
    _plt.grid()
    N = len(x)
    s = _np.arange(N)
    _plt.subplot(122)
    if outline:
        _plt.plot(s, x, color='red')
    _plt.bar(s, x, color='black')
    _plt.xticks([0, 10, 19])
    _plt.title('Input Function')
    _plt.grid()
    _plt.ylabel('x')
    L = M + N - 1
    w = _np.arange(L)
    _plt.figure(3)
    y = _np.convolve(h, x)
    if outline:
        _plt.plot(w, y, color='red')
    _plt.bar(w, y, color='black')
    _plt.ylabel('y')
    _plt.grid()
    _plt.title('Convolved Output')
    _plt.show()


def convolve(tuple):
    """
    Filter Convolution Function
    
    Given a tuple of terms, convolves all terms in tuple to
    return one tuple as a numpy array.
    
    Parameters
    ---------
    tuple:      tuple of numpy.ndarray
                Tuple of terms to be convolved.
    
    Returns
    -------
    c:          The convolved set of the individual terms.
                i.e. numpy.ndarray([ x1, x2, x3, ..., xn ])
    """
    c = sig.convolve(tuple[0], tuple[1])
    if len(tuple) > 2:
        for i in range(2, len(tuple)):
            c = sig.convolve(c, tuple[i])

    return c


def step(t):
    """
    Step Function [ u(t) ]
    
    Simple implimentation of numpy.heaviside function
    to provide standard step-function as specified to
    be zero at x<0, and one at x>=0.
    """
    return _np.heaviside(t, 1)


def peak(val):
    """
    Sinusoid RMS to Peak Converter
    
    Provides a readable format to convert an
    RMS (Root-Mean-Square) value to its peak
    representation. Performs a simple multiplication
    with the square-root of two.
    """
    return _np.sqrt(2) * val


def rms(val):
    """
    Sinusoid Peak to RMS Converter
    
    Provides a readable format to convert a peak
    value to its RMS (Root-Mean-Square) representation.
    Performs a simple division by the square-root of
    two.
    """
    return val * _np.sqrt(0.5)


def funcrms(f, T):
    """
    Function Root-Mean-Square (RMS) Evaluator
    
    Integral-based RMS calculator, evaluates the RMS value
    of a repetative signal (f) given the signal's specific
    period (T)

    Parameters
    ----------
    f:      float
            The periodic function, a callable like f(t)
    T:      float
            The period of the function f, so that f(0)==f(T)

    Returns
    -------
    RMS:    The RMS value of the function (f) over the interval ( 0, T )

    """
    fn = lambda x: f(x) ** 2
    integral = integrate(fn, 0, T)
    RMS = _np.sqrt(1 / T * integral)
    return RMS


def gaussian(x, mu=0, sigma=1):
    """
    Gaussian Function:
    
    This function is designed to generate the gaussian
    distribution curve with configuration mu and sigma.
    
    Parameters
    ----------
    x:      float
            The input (array) x.
    mu:     float, optional
            Optional control argument, default=0
    sigma:  float, optional
            Optional control argument, default=1
    
    Returns
    -------
    Computed gaussian (numpy.ndarray) of the input x
    """
    return 1 / (sigma * _np.sqrt(2 * _np.pi)) * _np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def gausdist(x, mu=0, sigma=1):
    """
    Gaussian Distribution Function:
    
    This function is designed to calculate the generic
    distribution of a gaussian function with controls
    for mu and sigma.
    
    Parameters
    ----------
    x:      numpy.ndarray
            The input (array) x
    mu:     float, optional
            Optional control argument, default=0
    sigma:  float, optional
            Optional control argument, default=1
    
    Returns
    -------
    F:      numpy.ndarray
            Computed distribution of the gausian function at the
            points specified by (array) x
    """
    F = _np.array([])
    try:
        lx = len(x)
    except:
        lx = 1
        x = [x]
    else:
        for i in range(lx):
            x_tmp = x[i]
            X = (x_tmp - mu) / sigma

            def integrand(sq):
                return _np.exp(-sq ** 2 / 2)

            integral = integrate(integrand, _np.NINF, X)
            result = 1 / _np.sqrt(2 * _np.pi) * integral[0]
            F = _np.append(F, result)
        else:
            if len(F) == 1:
                F = F[0]
            return F


def probdensity(func, x, x0=0, scale=True):
    """
    Probability Density Function:
    
    This function uses an integral to compute the probability
    density of a given function.
    
    Parameters
    ----------
    func:   function
            The function for which to calculate the PDF
    x:      numpy.ndarray
            The (array of) value(s) at which to calculate
            the PDF
    x0:     float, optional
            The lower-bound of the integral, starting point
            for the PDF to be calculated over, default=0
    scale:  bool, optional
            The scaling to be applied to the output,
            default=True
    
    Returns
    -------
    sumx:   numpy.ndarray
            The (array of) value(s) computed as the PDF at
            point(s) x
    """
    sumx = _np.array([])
    try:
        lx = len(x)
    except:
        lx = 1
        x = [x]
    else:
        for i in range(lx):
            sumx = _np.append(sumx, integrate(func, x0, x[i])[0])
        else:
            if len(sumx) == 1:
                sumx = sumx[0]
            else:
                if scale == True:
                    mx = sumx.max()
                    sumx /= mx
                else:
                    if scale != False:
                        sumx /= scale
            return sumx


def rfft(arr, dt=0.01, absolute=True, resample=True):
    """
    RFFT Function
    
    This function is designed to evaluat the real FFT
    of a input signal in the form of an array or list.
    
    Parameters
    ----------
    arr:        numpy.ndarray
                The input array representing the signal
    dt:         float, optional
                The time-step used for the array,
                default=0.01
    absolute:   bool, optional
                Control argument to force absolute
                values, default=True
    resample:   bool, optional
                Control argument specifying whether
                the FFT output should be resampled,
                or if it should have a specific
                resampling rate, default=True
    
    Returns
    -------
    FFT Array
    """
    if absolute:
        fourier = abs(_np.fft.rfft(arr))
    else:
        foruier = _np.fft.rfft(arr)
    if resample == True:
        dn = int(dt * len(arr))
        fixedfft = filter.dnsample(fourier, dn)
        return fixedfft
    if resample == False:
        return fourier
    resample = int(resample)
    fixedfft = filter.dnsample(fourier, resample)
    return fixedfft


def wrms(func, dw=0.1, NN=100, quad=False, plot=True, title='Power Density Spectrum', round=3):
    """
    WRMS Function:
    
    This function is designed to calculate the RMS
    bandwidth (Wrms) using a numerical process.
    
    Parameters
    ----------
    func:       function
                The callable function to use for evaluation
    dw:         float, optional
                The delta-omega to be used, default=0.1
    NN:         int, optional
                The total number of points, default=100
    quad:       bool, optional
                Control value to enable use of integrals
                default=False
    plot:       bool, optional
                Control to enable plotting, default=True
    title:      string, optional
                Title displayed with plot,
                default="Power Density Spectrum"
    round:      int, optional
                Control to round the Wrms on plot,
                default=3
    
    Returns
    -------
    W:          float
                Calculated RMS Bandwidth (rad/sec)
    """
    omega = _np.linspace(0, (NN - 1) * del_w, NN)
    Stot = Sw2 = 0
    Sxx = _np.array([])
    for n in range(NN):
        Sxx = _np.append(Sxx, func(omega[n]))
        Stot = Stot + Sxx[n]
        Sw2 = Sw2 + omega[n] ** 2 * Sxx[n]
    else:
        if quad:

            def intf(w):
                return w ** 2 * func(w)

            num = integrate(intf, 0, _np.inf)[0]
            den = integrate(func, 0, _np.inf)[0]
            W = _np.sqrt(num / den)
        else:
            W = _np.sqrt(Sw2 / Stot)
        Wr = _np.around(W, round)
        if plot:
            _plt.plot(omega, Sxx)
            _plt.title(title)
            x = 0.65 * max(omega)
            y = 0.8 * max(Sxx)
            _plt.text(x, y, 'Wrms: ' + str(Wr))
            _plt.show()
        return W


def hartleydata(BW, M):
    """
    Hartley Data Function
    
    Function to calculate Hartley's Law,
    the maximum data rate achievable for
    a given noiseless channel.
    
    Parameters
    ----------
    BW:         float
                Bandwidth of the data channel.
    M:          float
                Number of signal levels.
    
    Returns:
    --------
    C:          float
                Capacity of channel (in bits per second)
    """
    C = 2 * BW * _np.log2(M)
    return C


def shannondata(BW, S, N):
    """
    Shannon Data Function
    
    Function to calculate the maximum data
    rate that may be achieved given a data
    channel and signal/noise characteristics
    using Shannon's equation.
    
    Parameters
    ----------
    BW:         float
                Bandwidth of the data channel.
    S:          float
                Signal strength (in Watts).
    N:          float
                Noise strength (in Watts).
    
    Returns
    -------
    C:          float
                Capacity of channel (in bits per second)
    """
    C = BW * _np.log2(1 + S / N)
    return C


def crcsender(data, key):
    """
    CRC Sender Function
    
    Function to generate a CRC-embedded
    message ready for transmission.
    
    Contributing Author Credit:
    Shaurya Uppal
    Available from: geeksforgeeks.org
    
    Parameters
    ----------
    data:       string of bits
                The bit-string to be encoded.
    key:        string of bits
                Bit-string representing key.
    
    Returns
    -------
    codeword:   string of bits
                Bit-string representation of
                encoded message.
    """

    def xor(a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
        else:
            return ''.join(result)

    def mod2div(divident, divisor):
        pick = len(divisor)
        tmp = divident[0:pick]
        while pick < len(divident):
            if tmp[0] == '1':
                tmp = xor(divisor, tmp) + divident[pick]
            else:
                tmp = xor('0' * pick, tmp) + divident[pick]
            pick += 1

        if tmp[0] == '1':
            tmp = xor(divisor, tmp)
        else:
            tmp = xor('0' * pick, tmp)
        checkword = tmp
        return checkword

    data = str(data)
    key = str(key)
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword


def crcremainder(data, key):
    """
    CRC Remainder Function
    
    Function to calculate the CRC
    remainder of a CRC message.
    
    Contributing Author Credit:
    Shaurya Uppal
    Available from: geeksforgeeks.org
    
    Parameters
    ----------
    data:       string of bits
                The bit-string to be decoded.
    key:        string of bits
                Bit-string representing key.
    
    Returns
    -------
    remainder: string of bits
                Bit-string representation of
                encoded message.
    """

    def xor(a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
        else:
            return ''.join(result)

    def mod2div(divident, divisor):
        pick = len(divisor)
        tmp = divident[0:pick]
        while pick < len(divident):
            if tmp[0] == '1':
                tmp = xor(divisor, tmp) + divident[pick]
            else:
                tmp = xor('0' * pick, tmp) + divident[pick]
            pick += 1

        if tmp[0] == '1':
            tmp = xor(divisor, tmp)
        else:
            tmp = xor('0' * pick, tmp)
        checkword = tmp
        return checkword

    data = str(data)
    key = str(key)
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    return remainder


def string_to_bits(str):
    """
    String to Bits Converter
    
    Converts a Pythonic string to the string's
    binary representation.
    
    Parameters
    ----------
    str:        string
                The string to be converted.
    
    Returns
    -------
    data:       string
                The binary representation of the
                input string.
    """
    data = ''.join((format(ord(x), 'b') for x in str))
    return data


def kwh_to_btu(kWh):
    r"""
    Killo-Watt-Hours to BTU Function:
    
    Converts kWh (killo-Watt-hours) to BTU
    (British Thermal Units).
    
    .. math:: \text{BTU} = \text{kWh}\cdot3412.14
    
    Same as `btu`.
    
    Parameters
    ----------
    kWh:        float
                The number of killo-Watt-hours
    
    Returns
    -------
    BTU:        float
                The number of British Thermal Units
    """
    return kWh * 3412.14


btu = kwh_to_btu

def btu_to_kwh(BTU):
    r"""
    BTU to Killo-Watt-Hours Function:
    
    Converts BTU (British Thermal Units) to
    kWh (killo-Watt-hours).
    
    .. math:: \text{kWh} = \frac{\text{BTU}}{3412.14}
    
    Same as `kwh`.
    
    Parameters
    ----------
    BTU:        float
                The number of British Thermal Units
    
    Returns
    -------
    kWh:        float
                The number of killo-Watt-hours
    """
    return BTU / 3412.14


kwh = btu_to_kwh

def zpu(S, VLL=None, VLN=None):
    r"""
    Per-Unit Impedance Evaluator
    
    Evaluates the per-unit impedance value given the per-unit
    power and voltage bases.
    
    .. math:: Z_{pu}=\frac{V_{LL}^2}{S}
    
    .. math:: Z_{pu}=\frac{(\sqrt{3}*V_{LN})^2}{S}
    
    Parameters
    ----------
    S:          float
                The per-unit power base.
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    
    Returns
    -------
    Zbase:      float
                The per-unit impedance base.
    """
    if VLL == None:
        if VLN == None:
            raise ValueError('ERROR: One voltage must be provided.')
    if VLL != None:
        return VLL ** 2 / S
    return (_np.sqrt(3) * VLN) ** 2 / S


def ipu(S, VLL=None, VLN=None, V1phs=None):
    r"""
    Per-Unit Current Evaluator
    
    Evaluates the per-unit current value given the per-unit
    power and voltage bases.
    
    .. math:: I_{pu}=\frac{S}{\sqrt{3}*V_{LL}}
    
    .. math:: I_{pu}=\frac{S}{3*V_{LN}}
    
    Parameters
    ----------
    S:          float
                The per-unit power base.
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    V1phs:      float, optional
                The voltage base of the single phase system.
    
    Returns
    -------
    Ibase:      float
                The per-unit current base.
    """
    if VLL == None:
        if VLN == None:
            raise ValueError('ERROR: One voltage must be provided.')
    if VLL != None:
        return S / (_np.sqrt(3) * VLL)
    if VLN != None:
        return S / (3 * VLN)
    return S / V1phs


def puchgbase(quantity, puB_old, puB_new):
    r"""
    Per-Unit Change of Base Function
    
    Performs a per-unit change of base operation for the given
    value constrained by the old base and new base.
    
    .. math:: Z_{pu-new}=Z_{pu-old}*\frac{BASE_{OLD}}{BASE_{NEW}}
    
    Parameters
    ----------
    quantity:   complex
                Current per-unit value in old base.
    puB_old:    float
                Old per-unit base.
    puB_new:    float
                New per-unit base.
    
    Returns
    -------
    pu_new:     complex
                New per-unit value.
    """
    pu_new = quantity * puB_old / puB_new
    return pu_new


def zrecompose(z_pu, S3phs, VLL=None, VLN=None):
    """
    Impedance from Per-Unit System Evaluator
    
    Function to reverse per-unit conversion and return the ohmic value
    of an impedance given its per-unit parameters of R and X (as Z).
    
    Parameters
    ----------
    z_pu:       complex
                The per-unit, complex value corresponding to the
                impedance
    S3phs:      float
                The total three-phase power rating of the system.
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    
    Returns
    -------
    z:          complex
                The ohmic impedance evaluated from the per-unit base.
    """
    zbase = zpu(S3phs, VLL, VLN)
    z = z_pu * zbase
    return z


def rxrecompose(x_pu, XoR, S3phs=None, VLL=None, VLN=None):
    """
    Resistance/Reactance from Per-Unit System Evaluator
    
    Function to reverse per-unit conversion and return the ohmic value
    of an impedance given its per-unit parameters of X.
    
    Parameters
    ----------
    x_pu:       float
                The per-unit, complex value corresponding to the
                impedance
    XoR:        float
                The X/R ratio (reactance over impedance).
    S3phs:      float, optional
                The total three-phase power rating of the system.
                If left as None, the per-unit values will be set
                to 1, resulting in an unscaled impedance
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    
    Returns
    -------
    z:          complex
                The ohmic impedance evaluated from the per-unit base.
    """
    x_pu = abs(x_pu)
    r_pu = x_pu / XoR
    z_pu = r_pu + complex(0.0, 1.0) * x_pu
    if S3phs == None:
        return z_pu
    z = zrecomposez_puS3phsVLLVLN
    return z


def geninternalv(I, Zs, Vt, Vgn=None, Zm=None, Ip=None, Ipp=None):
    """
    Generator Internal Voltage Evaluator
    
    Evaluates the internal voltage for a generator given the
    generator's internal impedance and internal mutual coupling
    impedance values.
    
    Parameters
    ----------
    I:          complex
                The current on the phase of interest.
    Zs:         complex
                The internal impedance of the phase of
                interest in ohms.
    Vt:         complex
                The generator's terminal voltage.
    Vgn:        complex, optional
                The ground-to-neutral connection voltage.
    Zmp:        complex, optional
                The mutual coupling with the first additional
                phase impedance in ohms.
    Zmpp:       complex, optional
                The mutual coupling with the second additional
                phase impedance in ohms.
    Ip:         complex, optional
                The first mutual phase current in amps.
    Ipp:        complex, optional
                The second mutual phase current in amps.
    
    Returns
    -------
    Ea:         complex
                The internal voltage of the generator.
    """
    if Zmp == Zmpp  == Ip == Ipp != None:
        if Vgn == None:
            Vgn = 0
        Ea = Zs * I + Zmp * Ip + Zmpp * Ipp + Vt + Vgn
    else:
        if Vgn == Zm  == Ip == Ipp == None:
            Ea = Zs * I + Vt
        else:
            raise ValueError('Invalid Parameter Set')
    return Ea


def abc_to_seq(Mabc, reference='A'):
    r"""
    Phase-System to Sequence-System Conversion
    
    Converts phase-based values to sequence
    components.
    
    .. math:: M_{\text{012}}=A_{\text{012}}\cdot M_{\text{ABC}}
    
    Same as phs_to_seq.
    
    Parameters
    ----------
    Mabc:       list of complex
                Phase-based values to be converted.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    M012:       numpy.ndarray
                Sequence-based values in order of 0-1-2
    
    See Also
    --------
    seq_to_abc: Sequence to Phase Conversion
    sequencez:  Phase Impedance to Sequence Converter
    """
    reference = reference.upper()
    if reference == 'A':
        M = Aabc
    else:
        if reference == 'B':
            M = _np.roll(Aabc, 1, 0)
        else:
            if reference == 'C':
                M = _np.roll(Aabc, 2, 0)
            else:
                raise ValueError('Invalid Phase Reference.')
    return M.dot(Mabc)


phs_to_seq = abc_to_seq

def seq_to_abc(M012, reference='A'):
    r"""
    Sequence-System to Phase-System Conversion
    
    Converts sequence-based values to phase
    components.
    
    .. math:: M_{\text{ABC}}=A_{\text{012}}^{-1}\cdot M_{\text{012}}
    
    Same as seq_to_phs.
    
    Parameters
    ----------
    M012:       list of complex
                Sequence-based values to convert.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    
    Returns
    -------
    Mabc:       numpy.ndarray
                Phase-based values in order of A-B-C
    
    See Also
    --------
    abc_to_seq: Phase to Sequence Conversion
    sequencez:  Phase Impedance to Sequence Converter
    """
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


seq_to_phs = seq_to_abc

def sequencez(Zabc, reference='A', resolve=False, diag=False, round=3):
    r"""
    Sequence Impedance Calculator
    
    Accepts the phase (ABC-domain) impedances for a
    system and calculates the sequence (012-domain)
    impedances for the same system. If the argument
    `resolve` is set to true, the function will
    combine terms into the set of [Z0, Z1, Z2].
    
    When resolve is False:
    
    .. math:: Z_{\text{012-M}}=A_{\text{012}}^{-1}Z_{\text{ABC}}A_{\text{012}}
    
    When resolve is True:
    
    .. math:: Z_{\text{012}}=A_{\text{012}}Z_{\text{ABC}}A_{\text{012}}^{-1}
    
    Parameters
    ----------
    Zabc:       numpy.ndarray of complex
                2-D (3x3) matrix of complex values
                representing the phasor impedances
                in the ABC-domain.
    reference:  {'A', 'B', 'C'}
                Single character denoting the reference,
                default='A'
    resolve:    bool, optional
                Control argument to force the function to
                evaluate the individual sequence impedances
                [Z0, Z1, Z2], default=False
    diag:       bool, optional
                Control argument to force the function to
                reduce the matrix to its diagonal terms.
    round:      int, optional
                Integer denoting number of decimal places
                resulting matrix should be rounded to.
                default=3
    
    Returns
    -------
    Z012:       numpy.ndarray of complex
                2-D (3x3) matrix of complex values
                representing the sequence impedances
                in the 012-domain
    
    See Also
    --------
    seq_to_abc: Sequence to Phase Conversion
    abc_to_seq: Phase to Sequence Conversion
    """
    reference = reference.upper()
    rollrate = {'A':0,  'B':1,  'C':2}
    if reference not in rollrate:
        raise ValueError('Invalad Phase Reference')
    else:
        roll = rollrate[reference]
        M012 = _np.roll(A012, roll, 0)
        Minv = _np.linalg.inv(M012)
        if resolve:
            Z012 = M012.dot(Zabc.dot(Minv))
        else:
            Z012 = Minv.dot(Zabc.dot(M012))
    if diag:
        Z012 = [
         Z012[0][0], Z012[1][1], Z012[2][2]]
    return _np.around(Z012, round)


def funcfft(func, minfreq=60, maxmult=15, complex=False):
    """
    Function FFT Evaluator
    
    Given the callable function handle for a periodic function,
    evaluates the harmonic components of the function.
    
    Parameters
    ----------
    func:       function
                Callable function from which to evaluate values.
    minfreq:    float, optional
                Minimum frequency (in Hz) at which to evaluate FFT.
                default=60
    maxmult:    int, optional
                Maximum harmonic (multiple of minfreq) which to
                evaluate. default=15
    complex:    bool, optional
                Control argument to force returned values into
                complex format.
    
    Returns
    -------
    DC:         float
                The DC offset of the FFT result.
    A:          list of float
                The real components from the FFT.
    B:          list of float
                The imaginary components from the FFT.
    """
    NN = 2 * maxmult + 2
    T = 1 / minfreq
    t, dt = _np.linspace(0, T, NN, endpoint=False, retstep=True)
    y = _np.fft.rfft(func(t)) / t.size
    if complex:
        return y
    y *= 2
    return (y[0].real, y[1:-1].real, -y[1:-1].imag)


def sampfft(data, dt, minfreq=60.0, complex=False):
    """
    Sampled Dataset FFT Evaluator
    
    Given a data array and the delta-t for the data array, evaluates
    the harmonic composition of the data.
    
    Parameters
    ----------
    data:       numpy.ndarray
                Numpy data array containing 1-D values.
    dt:         float
                Time-difference (delta-t) between data samples.
    minfreq:    float, optional
                Minimum frequency (in Hz) at which to evaluate FFT.
                default=60
    complex:    bool, optional
                Control argument to force returned values into
                complex format.
    
    Returns
    -------
    DC:         float
                The DC offset of the FFT result.
    A:          list of float
                The real components from the FFT.
    B:          list of float
                The imaginary components from the FFT.
    """
    FR = 1 / (dt * len(data))
    NN = 1 // (dt * minfreq)
    if FR > minfreq:
        raise ValueError('Too few data samples to evaluate FFT at specified minimum frequency.')
    else:
        if FR == minfreq:
            y = _np.fft.rfft(data) / len(data)
        else:
            cut_data = data[:int(NN)]
            y = _np.fft.rfft(cut_data) / len(cut_data)
    if complex:
        return y
    y *= 2
    return (y[0].real, y[1:-1].real, -y[1:-1].imag)


def fftplot(dc, real, imag=None, title='Fourier Coefficients'):
    """
    FFT System Plotter
    
    Plotting function for FFT (harmonic) values,
    plots the DC, Real, and Imaginary components.
    
    Parameters
    ----------
    dc:         float
                The DC offset term
    real:       list of float
                Real terms of FFT (cosine terms)
    imag:       list of float, optional
                Imaginary terms of FFT (sine terms)
    title:      str, optional
                String appended to plot title,
                default="Fourier Coefficients"
    """
    rng = range(1, len(real) + 1, 1)
    xtic = range(0, len(real) + 1, 1)
    a0x = [
     0, 0]
    a0y = [0, dc / 2]
    _plt.title(title)
    _plt.plot(a0x, a0y, 'g', label='DC-Term')
    _plt.stem(rng, real, 'r', 'ro', label='Real-Terms', use_line_collection=True)
    try:
        imag != None
    except ValueError:
        _plt.stem(rng, imag, 'b', 'bo', label='Imaginary-Terms', use_line_collection=True)
    else:
        _plt.xlabel('Harmonics (Multiple of Fundamental)')
        _plt.ylabel('Harmonic Magnitude')
        _plt.axhline(0.0, color='k')
        _plt.legend()
        if len(xtic) < 50:
            _plt.xticks(xtic)
        _plt.show()


def fftsumplot(dc, real, imag=None, freq=60, xrange=None, npts=1000, plotall=False, title='Fourier Series Summation'):
    """
    FFT Summation Plotter
    
    Function to generate the plot of the sumed FFT results.
    
    Parameters
    ----------
    dc:         float
                The DC offset term
    real:       list of float
                Real terms of FFT (cosine terms)
    imag:       list of float
                Imaginary terms of FFT (sine terms)
    freq:       float, optional
                Fundamental (minimum nonzero) frequency in Hz,
                default=60
    xrange:     list of float, optional
                List of two floats containing the minimum
                time and the maximum time.
    npts:       int, optional
                Number of time step points, default=1000
    title:      str, optional
                String appended to plot title,
                default="Fourier Series Summation"
    """
    N = len(real)
    T = 1 / freq
    if xrange == None:
        x = _np.linspace(0, T, npts)
    else:
        x = _np.linspace(xrange[0], xrange[1], npts)
    yout = _np.ones(len(x)) * dc
    for k in range(1, N):
        if plotall:
            _plt.plot(x, yout)
        yout += real[(k - 1)] * _np.cos(k * 2 * _np.pi * x / T)
        if imag != None:
            yout += imag[(k - 1)] * _np.sin(k * 2 * _np.pi * x / T)
        _plt.plot(x, yout)
        _plt.title(title)
        _plt.xlabel('Time (seconds)')
        _plt.ylabel('Magnitude')
        _plt.show()


def harmonics(real, imag=None, dc=0, freq=60, domain=None):
    """
    Harmonic Function Generator
    
    Generate a function or dataset for a harmonic system
    given the real (cosine), imaginary (sine), and DC
    components of the system.
    
    Parameters
    ----------
    real:       list of float
                The real (cosine) component coefficients
                for the harmonic system.
    imag:       list of float, optional
                The imaginary (sine) component coefficients
                for the harmonic system.
    dc:         float, optional
                The DC offset for the harmonic system,
                default=0
    freq:       float, optional
                The fundamental frequency of the system in
                Hz, default=60
    domain:     list of float, optional
                Domain of time samples at which to calculate
                the harmonic system, must be array-like, will
                cause function to return numpy array instead
                of function object.
    
    Returns
    -------
    system:     function
                Function object handle which can be used to
                call the function to evaluate the harmonic
                system at specified times.
    """
    if not isinstance(real, (list, _np.ndarray)):
        raise ValueError('Argument *real* must be array-like.')
    else:
        if imag != None:
            if not isinstance(imag, (list, _np.ndarray)):
                raise ValueError('Argument *imag* must be array-like.')
        w = 2 * _np.pi * freq

        def _harmonic_(t):
            out = dc
            for k in range(len(real)):
                A = real[k]
                if imag != None:
                    B = imag[k]
                else:
                    B = 0
                m = k + 1
                out += A * _np.cos(m * w * t) + B * _np.sin(m * w * t)
            else:
                return out

        if domain is None:
            system = _harmonic_
        else:
            system = _harmonic_(domain)
    return system


def motorstartcap(V, I, freq=60):
    """
    Single Phase Motor Starting Capacitor Function
    
    Function to evaluate a reccomended value for the
    startup capacitor associated with a single phase
    motor.
    
    Parameters
    ----------
    V:          float
                Magnitude of motor terminal voltage in volts.
    I:          float
                Magnitude of motor no-load current in amps.
    freq:       float, optional
                Motor/System frequency, default=60.
                
    Returns
    -------
    C:          float
                Suggested capacitance in Farads.
    """
    I = abs(I)
    V = abs(V)
    C = I / (2 * _np.pi * freq * V)
    return C


def pfcorrection(S, PFold, PFnew, VLL=None, VLN=None, V=None, freq=60):
    """
    Power Factor Correction Function
    
    Function to evaluate the additional reactive power and
    capacitance required to achieve the desired power factor
    given the old power factor and new power factor.
    
    Parameters
    ----------
    S:          float
                Apparent power consumed by the load.
    PFold:      float
                The current (old) power factor, should be a decimal
                value.
    PFnew:      float
                The desired (new) power factor, should be a decimal
                value.
    VLL:        float, optional
                The Line-to-Line Voltage; default=None
    VLN:        float, optional
                The Line-to-Neutral Voltage; default=None
    V:          float, optional
                Voltage across the capacitor, ignores line-to-line
                or line-to-neutral constraints. default=None
    freq:       float, optional
                System frequency, default=60
    
    Returns
    -------
    C:          float
                Required capacitance in Farads.
    Qc:         float
                Difference of reactive power, (Qc = Qnew - Qold)
    """
    S = abs(S)
    Pold = S * PFold
    Qold = _np.sqrt(S ** 2 - Pold ** 2)
    Scorrected = Pold / PFnew
    Qcorrected = _np.sqrt(Scorrected ** 2 - Pold ** 2)
    Qc = Qold - Qcorrected
    if VLL == VLN == V == None:
        raise ValueError('One voltage must be specified.')
    else:
        if VLN != None:
            C = Qc / (2 * _np.pi * freq * 3 * VLN ** 2)
        else:
            if VLL != None:
                V = VLL
            C = Qc / (2 * _np.pi * freq * V ** 2)
    return (
     C, Qc)


def acpiv(S=None, I=None, VLL=None, VLN=None, V=None, PF=None):
    """
    AC Power-Voltage-Current Relation Function
    
    Relationship function to return apparent power, voltage, or
    current in one of various forms.
    
    Parameters
    ----------
    S:          complex, optional
                Apparent power, may be single or three-phase,
                specified in volt-amps (VAs)
    I:          complex, optional
                Phase current in amps
    VLL:        complex, optional
                Line-to-Line voltage in volts
    VLN:        complex, optional
                Line-to-Neutral voltage in volts
    V:          complex, optional
                Single-phase voltage in volts
    
    Returns
    -------
    S:          complex
                Apparent power, returned only if one voltage
                and current is specified
    I:          complex
                Phase current, returned only if one voltage
                and apparent power is specified
    VLL:        complex
                Line-to-Line voltage, returned only if current
                and apparent power specified, returned as set
                with other voltages in form: (VLL, VLN, V)
    VLN:        complex
                Line-to-Neutral voltage, returned only if
                current and apparent power specified, returned
                as set with other voltages in form: (VLL, VLN, V)
    V:          complex
                Single-phase voltage, returned only if current
                and apparent power specified, returned as set
                with other voltages in form: (VLL, VLN, V)
    PF:         float, optional
                Supporting argument to convert floating-point
                apparent power to complex representation.
    """
    if S == I == None:
        raise ValueError('To few arguments.')
    elif PF != None:
        S = S * PF + complex(0.0, 1.0) * _np.sqrt(S ** 2 - (S * PF) ** 2)
    elif V != None:
        if S == None:
            S = V * _np.conj(I)
            return S
        I = _np.conj(S / V)
        return I
    else:
        if VLL != None:
            if S == None:
                S = _np.sqrt(3) * VLL * _np.conj(I)
                return S
            I = _np.conj(S / (_np.sqrt(3) * VLL))
            return I
        else:
            if VLN != None:
                if S == None:
                    S = 3 * VLN * _np.conj(I)
                    return S
                I = _np.conj(S / (3 * VLN))
                return I
            else:
                V = S / _np.conj(I)
                VLL = S / (_np.sqrt(3) * _np.conj(I))
                VLN = S / (3 * _np.conj(I))
                return (VLL, VLN, V)


def primary(val, Np, Ns=1, invert=False):
    """
    Transformer Primary Evaluator
    
    Returns a current or voltage value reflected across
    a transformer with a specified turns ratio Np/Ns.
    Converts to the primary side.
    
    Parameters
    ----------
    val:        complex
                Value to be reflected across transformer.
    Np:         float
                Number of turns on primary side.
    Ns:         float, optional
                Number of turns on secondary side.
    invert:     bool, optional
                Control argument to invert the turns ratio,
                used when reflecting current across a
                voltage transformer, or voltage across a
                current transformer.
    
    Returns
    -------
    reflection: complex
                The reflected value referred to the primary
                side according to Np and Ns.
    """
    if invert:
        return val * Ns / Np
    return val * Np / Ns


def secondary(val, Np, Ns=1, invert=False):
    """
    Transformer Secondary Evaluator
    
    Returns a current or voltage value reflected across
    a transformer with a specified turns ratio Np/Ns.
    Converts to the secondary side.
    
    Parameters
    ----------
    val:        complex
                Value to be reflected across transformer.
    Np:         float
                Number of turns on primary side.
    Ns:         float, optional
                Number of turns on secondary side.
    invert:     bool, optional
                Control argument to invert the turns ratio,
                used when reflecting current across a
                voltage transformer, or voltage across a
                current transformer.
    
    Returns
    -------
    reflection: complex
                The reflected value referred to the secondary
                side according to Np and Ns.
    """
    if invert:
        return val * Np / Ns
    return val * Ns / Np


def natfreq(C, L, Hz=True):
    r"""
    Natural Frequency Evaluator
    
    Evaluates the natural frequency (resonant frequency)
    of a circuit given the circuit's C and L values. Defaults
    to returning values in Hz, but may also return in rad/sec.
    
    .. math:: freq=\frac{1}{\sqrt{L*C}*(2*\pi)}
    
    Parameters
    ----------
    C:          float
                Capacitance Value in Farads.
    L:          float
                Inductance in Henries.
    Hz:         bool, optional
                Control argument to set return value in either
                Hz or rad/sec; default=True.
    
    Returns
    -------
    freq:       float
                Natural (Resonant) frequency, will be in Hz if
                argument *Hz* is set True (default), or rad/sec
                if argument is set False.
    """
    freq = 1 / _np.sqrt(L * C)
    if Hz:
        freq = freq / (2 * _np.pi)
    return freq


def unbalance(A, B, C, all=False):
    """
    Voltage/Current Unbalance Function
    
    Performs a voltage/current unbalance calculation
    to determine the maximum current/voltage
    unbalance. Returns result as a decimal percentage.
    
    Parameters
    ----------
    A:          float
                Phase-A value
    B:          float
                Phase-B value
    C:          float
                Phase-C value
    all:        bool, optional
                Control argument to require function
                to return all voltage/current unbalances.
    
    Returns
    -------
    unbalance:  float
                The unbalance as a percentage of the
                average. (i.e. 80% = 0.8)
    """
    A = abs(A)
    B = abs(B)
    C = abs(C)
    avg = (A + B + C) / 3
    dA = abs(A - avg)
    dB = abs(B - avg)
    dC = abs(C - avg)
    mx = max(dA, dB, dC)
    unbalance = mx / avg
    if all:
        return (
         dA / avg, dB / avg, dC / avg)
    return unbalance


def cosfilt(arr, Srate, domain=False):
    """
    Cosine Filter Function
    
    Cosine Filter function for filtering a dataset
    representing a sinusoidal function with or without
    harmonics to evaluate the fundamental value.
    
    Parameters
    ----------
    arr:        numpy.ndarray
                The input data array.
    Srate:      int
                Sampling rate for dataset, specified in
                number of values per fundamental cycle.
    domain:     bool, optional
                Control argument to force return of
                x-axis array for the filtered data.
    
    Returns
    -------
    cosf:       numpy.ndarray
                Cosine-filtered data
    xarray:     numpy.ndarray
                X-axis array for the filtered data.
    """
    ind = _np.arange(Srate - 1, len(arr) - 1)

    def cos(k, Srate):
        return _np.cos(2 * _np.pi * k / Srate)

    const = 2 / Srate
    cosf = 0
    for k in range(0, Srate - 1):
        slc = ind - (Srate - 1) + k
        cosf += cos(k, Srate) * arr[slc]
    else:
        cosf = const * cosf
        if domain:
            xarray = _np.linspace(Srate + Srate / 4 - 1, len(arr) - 1, len(cosf))
            xarray = xarray / Srate
            return (cosf, xarray)
        return cosf


def sinfilt(arr, Srate, domain=False):
    """
    Sine Filter Function
    
    Sine Filter function for filtering a dataset
    representing a sinusoidal function with or without
    harmonics to evaluate the fundamental value.
    
    Parameters
    ----------
    arr:        numpy.ndarray
                The input data array.
    Srate:      int
                Sampling rate for dataset, specified in
                number of values per fundamental cycle.
    domain:     bool, optional
                Control argument to force return of
                x-axis array for the filtered data.
    
    Returns
    -------
    sinf:       numpy.ndarray
                Sine-filtered data
    xarray:     numpy.ndarray
                X-axis array for the filtered data.
    """
    ind = _np.arange(Srate - 1, len(arr) - 1)

    def sin(k, Srate):
        return _np.sin(2 * _np.pi * k / Srate)

    const = 2 / Srate
    sinf = 0
    for k in range(0, Srate - 1):
        slc = ind - (Srate - 1) + k
        sinf += sin(k, Srate) * arr[slc]
    else:
        sinf = const * sinf
        if domain:
            xarray = _np.linspace(Srate + Srate / 4 - 1, len(arr) - 1, len(sinf))
            xarray = xarray / Srate
            return (sinf, xarray)
        return sinf


def characterz(R, G, L, C, freq=60):
    r"""
    Characteristic Impedance Calculator
    
    Function to evaluate the characteristic 
    impedance of a system with specefied
    line parameters as defined. System uses
    the standard characteristic impedance
    equation :eq:`Zc`.
    
    .. math:: Z_c = \sqrt{\frac{R+j\omega L}{G+j\omega C}}
       :label: Zc
    
    Parameters
    ----------
    R:          float
                Resistance in ohms.
    G:          float
                Conductance in mhos (siemens).
    L:          float
                Inductance in Henries.
    C:          float
                Capacitance in Farads.
    freq:       float, optional
                System frequency in Hz, default=60
    
    Returns
    -------
    Zc:         complex
                Charcteristic Impedance of specified line.
    """
    w = 2 * _np.pi * freq
    Zc = _np.sqrt((R + complex(0.0, 1.0) * w * L) / (G + complex(0.0, 1.0) * w * C))
    return Zc


def xfmphs(style='DY', shift=30):
    """
    Simple Transformer Phase-Shift Calculator
    
    Use with transformer orientation to evaluate
    the phase-shift across a transformer. For
    example, find the phase shift for a Delta-Wye
    transformer as seen from the delta side.
    
    Parameters
    ----------
    style:      {'DY','YD','DD','YY'}, optional
                String that denotes the transformer
                orientation. default='DY'
    shift:      float, optional
                Transformer angle shift, default=30
    
    Returns
    -------
    phase:      complex
                Phasor including the phase shift and
                positive or negative characteristic.
    
    Examples
    --------
    >>> import electricpy as ep
    >>> # Find shift of Delta-Wye Transformer w/ 30° shift
    >>> shift = ep.xfmphs(style="DY",shift=30)
    >>> ep.cprint(shift)
    1.0 ∠ 30.0°
    """
    orientation = {'DY':1, 
     'YD':-1, 
     'DD':0, 
     'YY':0}
    v = orientation[style.upper()]
    phase = _np.exp(complex(0.0, 1.0) * _np.radians(v * abs(shift)))
    return phase


def rad_to_hz(radians):
    r"""
    Simple Radians to Hertz Converter
    
    Accepts a frequency in radians/sec and calculates
    the hertzian frequency (in Hz).
    
    .. math:: f_{\text{Hz}} = \frac{f_{\text{rad/sec}}}{2\cdot\pi}
    
    Same as `hertz`.
    
    Paramters
    ---------
    radians:    float
                The frequency (represented in radians/sec)
    
    Returns
    -------
    hertz:      float
                The frequency (represented in Hertz)
    """
    return radians / (2 * _np.pi)


hertz = rad_to_hz

def hz_to_rad(hertz):
    r"""
    Simple Hertz to Radians Converter
    
    Accepts a frequency in Hertz and calculates
    the frequency in radians/sec.
    
    .. math:: f_{\text{rad/sec}} = f_{\text{Hz}}\cdot2\cdot\pi
    
    Same as `radsec`.
    
    Paramters
    ---------
    hertz:      float
                The frequency (represented in Hertz)
    
    Returns
    -------
    radians:    float
                The frequency (represented in radians/sec)
    """
    return hertz * (2 * _np.pi)


radsec = hz_to_rad

def indmachvth(Vas, Rs, Lm, Lls=0, Ls=None, freq=60, calcX=True):
    r"""
    Induction Machine Thevenin Voltage Calculator
    
    Function to calculate the Thevenin equivalent voltage of an
    induction machine given a specific set of parameters.
    
    .. math:: V_{th}=\frac{j\omega L_m}{R_s+j\omega(L_{ls}+L_m)}V_{as}
    
    where:
    
    .. math:: \omega = \omega_{es} = 2\pi\cdot f_{\text{electric}}
    
    Parameters
    ----------
    Vas:        complex
                Terminal Stator Voltage in Volts
    Rs:         float
                Stator resistance in ohms
    Lm:         float
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Vth:        complex
                Thevenin-Equivalent voltage (in volts) of induction
                machine described.
    
    See Also
    --------
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    if Ls != None:
        Lls = Ls - Lm
    if calcX:
        w = 2 * _np.pi * freq
        Lm *= w
        Lls *= w
    Vth = complex(0.0, 1.0) * Lm / (Rs + complex(0.0, 1.0) * (Lls + Lm)) * Vas
    return Vth


def indmachzth(Rs, Lm, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Induction Machine Thevenin Impedance Calculator
    
    Function to calculate the Thevenin equivalent impedance of an
    induction machine given a specific set of parameters.
    
    .. math::
       Z_{th} = \frac{(R_s+j\omega L_{ls})j\omega L_m}
       {R_s+j\omega(L_{ls}+L_m)}+j\omega L_{lr}
    
    where:
    
    .. math:: \omega = \omega_{es} = 2\pi\cdot f_{\text{electric}}
    
    Parameters
    ----------
    Rs:         float
                Stator resistance in ohms
    Lm:         float
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Zth:        complex
                Thevenin-Equivalent impedance (in ohms) of induction
                machine described.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if calcX:
        w = 2 * _np.pi * freq
        Lm *= w
        Lls *= w
        Llr *= w
    Zth = (Rs + complex(0.0, 1.0) * Lls) * (complex(0.0, 1.0) * Lm) / (Rs + complex(0.0, 1.0) * (Lls + Lm)) + complex(0.0, 1.0) * Llr
    return Zth


def indmachpem(slip, Rr, Vth=None, Zth=None, Vas=0, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Mechanical Power Calculator for Induction Machines
    
    Function to calculate the mechanical power using the thevenin
    equivalent circuit terms.
    
    .. math:: 
       P_{em}=\frac{|V_{th_{\text{stator}}}|^2\cdot\frac{R_r}{slip}}
       {\left[\left(\frac{R_r}{slip}+R_{th_{\text{stator}}}\right)^2
       +X_{th_{\text{stator}}}^2\right]\cdot\omega_{es}}\cdot(1-slip)
    
    Parameters
    ----------
    slip:       float
                The mechanical/electrical slip factor of the
                induction machine.
    Rr:         float
                Rotor resistance in ohms
    Vth:        complex, optional
                Thevenin-equivalent stator voltage of the
                induction machine, may be calculated internally
                if given stator voltage and machine parameters.
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Vas:        complex, optional
                Terminal Stator Voltage in Volts
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Pem:        float
                Power (in watts) that is produced or consumed
                by the mechanical portion of the induction machine.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    if Vth == None:
        if not all((Vas, Rs, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Vth = indmachvth(Vas, Rs, Lm, Lls, Ls, freq, calcX)
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Llr, Ls, Lr, freq, calcX)
    Rth = Zth.real
    Xth = Zth.imag
    Pem = abs(Vth) ** 2 * Rr / slip / (((Rr / slip + Rth) ** 2 + Xth ** 2) * w) * (1 - slip)
    return Pem


def indmachtem(slip, Rr, p=0, Vth=None, Zth=None, Vas=0, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, wsyn=None, freq=60, calcX=True):
    r"""
    Induction Machine Torque Calculator
    
    Calculate the torque generated or consumed by an induction
    machine given the machine parameters of Vth and Zth by use
    of the equation below.
    
    .. math:: 
       T_{em}=\frac{3|V_{th_{\text{stator}}}|^2}
       {\left[\left(\frac{R_r}{slip}+R_{th_{\text{stator}}}\right)^2
       +X_{th_{\text{stator}}}\right]}\frac{R_r}{slip*\omega_{sync}}
    
    where:
    
    .. math:: 
       \omega_{sync}=\frac{\omega_{es}}{\left(\frac{poles}{2}\right)}
    
    Parameters
    ----------
    slip:       float
                The mechanical/electrical slip factor of the
                induction machine.
    Rr:         float
                Rotor resistance in ohms
    p:          int, optional
                Number of poles in the induction machine
    Vth:        complex, optional
                Thevenin-equivalent stator voltage of the
                induction machine, may be calculated internally
                if given stator voltage and machine parameters.
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Vas:        complex, optional
                Terminal Stator Voltage in Volts
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    wsyn:       float, optional
                Synchronous speed in rad/sec, may be specified
                directly as a replacement of p (number of poles).
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Tem:        float
                Torque (in Newton-meters) that is produced or consumed
                by the mechanical portion of the induction machine.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if p != 0:
        wsyn = w / (p / 2)
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    if not any((p, wsync)):
        raise ValueError('Poles or Synchronous Speed must be specified.')
    if Vth == None:
        if not all((Vas, Rs, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Vth = indmachvth(Vas, Rs, Lm, Lls, Ls, freq, calcX)
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Ll, Ls, Lr, freq, calcX)
    Rth = Zth.real
    Xth = Zth.imag
    Tem = 3 * abs(Vth) ** 2 / ((Rr / slip + Rth) ** 2 + Xth) * Rr / (slip * wsyn)
    return Tem


def indmachpkslip(Rr, Zth=None, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Induction Machine Slip at Peak Torque Calculator
    
    Function to calculate the slip encountered by an induction machine
    with the parameters specified when the machine is generating peak
    torque. Uses formula as shown below.
    
    .. math:: \text{slip} = \frac{R_r}{|Z_{th}|}
    
    where:

    .. math::
       Z_{th} = \frac{(R_s+j\omega L_{ls})j\omega L_m}
       {R_s+j\omega(L_{ls}+L_m)}+j\omega L_{lr}
    
    Parameters
    ----------
    Rr:         float
                Rotor resistance in ohms
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    s_peak:     float
                The peak slip for the induction machine described.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Ll, Ls, Lr, freq, calcX)
    s_peak = Rr / abs(Zth)
    return s_peak


def indmachiar(Vth=None, Zth=None, Vas=0, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Induction Machine Rotor Current Calculator
    
    Calculation function to find the phase-A, rotor current for an
    induction machine given the thevenin voltage and impedance.
    
    This current is calculated using the following formulas:
    
    .. math:: I_{a_{\text{rotor}}} = \frac{V_{th}}{|Z_{th}|+Z_{th}}
    
    where:
    
    .. math:: V_{th}=\frac{j\omega L_m}{R_s+j\omega(L_{ls}+L_m)}V_{as}
    
    .. math::
       Z_{th} = \frac{(R_s+j\omega L_{ls})j\omega L_m}
       {R_s+j\omega(L_{ls}+L_m)}+j\omega L_{lr}
    
    .. math:: \omega = \omega_{es} = 2\pi\cdot f_{\text{electric}}
    
    Parameters
    ----------
    Vth:        complex, optional
                Thevenin-equivalent stator voltage of the
                induction machine, may be calculated internally
                if given stator voltage and machine parameters.
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Vas:        complex, optional
                Terminal Stator Voltage in Volts
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Iar:        complex
                The rotor, phase-A current in amps.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if p != 0:
        wsyn = w / (p / 2)
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    if Vth == None:
        if not all((Vas, Rs, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Vth = indmachvth(Vas, Rs, Lm, Lls, Ls, freq, calcX)
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Ll, Ls, Lr, freq, calcX)
    Iar = Vth / (Zth.real + Zth)
    return Iar


def indmachpktorq(Rr, s_pk=None, Iar=None, Vth=None, Zth=None, Vas=0, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Induction Machine Peak Torque Calculator
    
    Calculation function to find the peak torque for an
    induction machine given the thevenin voltage and impedance.
    
    This current is calculated using the following formulas:
    
    .. math:: 
       T_{em}=(|I_{a_{\text{rotor}}}|)^2\cdot\frac{R_r}
       {\text{slip}_{\text{peak}}}
    
    where:
    
    .. math:: I_{a_{\text{rotor}}} = \frac{V_{th}}{|Z_{th}|+Z_{th}}
    
    .. math:: V_{th}=\frac{j\omega L_m}{R_s+j\omega(L_{ls}+L_m)}V_{as}
    
    .. math::
       Z_{th} = \frac{(R_s+j\omega L_{ls})j\omega L_m}
       {R_s+j\omega(L_{ls}+L_m)}+j\omega L_{lr}
    
    .. math:: \omega = \omega_{es} = 2\pi\cdot f_{\text{electric}}
    
    Parameters
    ----------
    Rr:         float
                Rotor resistance in Ohms
    s_pk:       float, optional
                Peak induction machine slip, may be calculated
                internally if remaining machine characteristics are
                provided.
    Iar:        complex, optional
                Phase-A, Rotor Current in Amps, may be calculated
                internally if remaining machine characteristics are
                provided.
    Vth:        complex, optional
                Thevenin-equivalent stator voltage of the
                induction machine, may be calculated internally
                if given stator voltage and machine parameters.
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Vas:        complex, optional
                Terminal Stator Voltage in Volts
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Tpk:        float
                Peak torque of specified induction machine in
                newton-meters.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    indmachstarttorq:   Induction Machine Starting Torque Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if p != 0:
        wsyn = w / (p / 2)
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    if Vth == None:
        if not all((Vas, Rs, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Vth = indmachvth(Vas, Rs, Lm, Lls, Ls, freq, calcX)
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Ll, Ls, Lr, freq, calcX)
    if Iar == None:
        if not all((Vth, Zth)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Iar = indmachiar(Vth=Vth, Zth=Zth)
    if s_pk == None:
        if not all((Rr, Zth)):
            raise ValueError('Invalid Argument Set, too few provided.')
        s_pk = indmachpkslip(Rr=Rr, Zth=Zth)
    Tpk = abs(Iar) ** 2 * Rr / s_pk
    return Tpk


def indmachstarttorq(Rr, Iar=None, Vth=None, Zth=None, Vas=0, Rs=0, Lm=0, Lls=0, Llr=0, Ls=None, Lr=None, freq=60, calcX=True):
    r"""
    Induction Machine Starting Torque Calculator
    
    Calculation function to find the starting torque for an
    induction machine given the thevenin voltage and impedance.
    
    This current is calculated using the following formulas:
    
    .. math:: 
       T_{em}=(|I_{a_{\text{rotor}}}|)^2\cdot\frac{R_r}
       {\text{slip}_{\text{peak}}}
    
    where:
    
    .. math:: \text{slip} = 1
    
    .. math::
       I_{a_{\text{rotor}}} = \frac{V_{th}}{\frac{R_r}{\text{slip}}+Z_{th}}
    
    .. math:: V_{th}=\frac{j\omega L_m}{R_s+j\omega(L_{ls}+L_m)}V_{as}
    
    .. math::
       Z_{th} = \frac{(R_s+j\omega L_{ls})j\omega L_m}
       {R_s+j\omega(L_{ls}+L_m)}+j\omega L_{lr}
    
    .. math:: \omega = \omega_{es} = 2\pi\cdot f_{\text{electric}}
    
    Parameters
    ----------
    Rr:         float
                Rotor resistance in Ohms
    Iar:        complex, optional
                Phase-A, Rotor Current in Amps, may be calculated
                internally if remaining machine characteristics are
                provided.
    Vth:        complex, optional
                Thevenin-equivalent stator voltage of the
                induction machine, may be calculated internally
                if given stator voltage and machine parameters.
    Zth:        complex, optional
                Thevenin-equivalent inductance (in ohms) of the
                induction machine, may be calculated internally
                if given machine parameters.
    Vas:        complex, optional
                Terminal Stator Voltage in Volts
    Rs:         float, optional
                Stator resistance in ohms
    Lm:         float, optional
                Magnetizing inductance in Henrys
    Lls:        float, optional
                Stator leakage inductance in Henrys, default=0
    Llr:        float, optional
                Rotor leakage inductance in Henrys, default=0
    Ls:         float, optional
                Stator inductance in Henrys
    Lr:         float, optional
                Rotor inductance in Henrys
    freq:       float, optional
                System (electrical) frequency in Hz, default=60
    calcX:      bool, optional
                Control argument to force system to calculate
                system reactances with system frequency, or to
                treat them as previously-calculated reactances.
                default=True
    
    Returns
    -------
    Tstart:     float
                Peak torque of specified induction machine in
                newton-meters.
    
    See Also
    --------
    indmachvth:         Induction Machine Thevenin Voltage Calculator
    indmachzth:         Induction Machine Thevenin Impedance Calculator
    indmachpem:         Induction Machine Electro-Mechanical Power Calculator
    indmachtem:         Induction Machine Electro-Mechanical Torque Calculator
    indmachpkslip:      Induction Machine Peak Slip Calculator
    indmachpktorq:      Induction Machine Peak Torque Calculator
    indmachiar:         Induction Machine Phase-A Rotor Current Calculator
    """
    w = 2 * _np.pi * freq
    if Ls != None:
        Lls = Ls - Lm
    if Lr != None:
        Llr = Lr - Lm
    if p != 0:
        wsyn = w / (p / 2)
    if calcX:
        Lm *= w
        Lls *= w
        Llr *= w
    slip = 1
    if Vth == None:
        if not all((Vas, Rs, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Vth = indmachvth(Vas, Rs, Lm, Lls, Ls, freq, calcX)
    if Zth == None:
        if not all((Rs, Llr, Lm, Lls)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Zth = indmachzth(Rs, Lm, Lls, Ll, Ls, Lr, freq, calcX)
    if Iar == None:
        if not all((Vth, Zth)):
            raise ValueError('Invalid Argument Set, too few provided.')
        Iar = Vth / (Rr / slip + Zth)
    Tstart = abs(Iar) ** 2 * Rr / s_pk
    return Tstart


def pstator(Pem, slip):
    r"""
    Stator Power Calculator for Induction Machine
    
    Given the electromechanical power and the slip,
    this function will calculate the power related to the
    stator (provided or consumed).
    
    .. math:: P_s=\frac{P_{em}}{1-\text{slip}}
    
    Parameters
    ----------
    Pem:        float
                Electromechanical power in watts.
    slip:       float
                Slip factor in rad/sec.
    
    Returns
    -------
    Ps:         float
                Power related to the stator in watts.
    
    See Also
    --------
    protor:         Rotor Power Calculator for Induction Machines
    """
    Ps = Pem / (1 - slip)
    return Ps


def protor(Pem, slip):
    r"""
    Rotor Power Calculator for Induction Machine
    
    Given the electromechanical power and the slip,
    this function will calculate the power related to the
    rotor (provided or consumed).
    
    .. math:: P_r=-\text{slip}\cdot\frac{P_{em}}{1-\text{slip}}
    
    Parameters
    ----------
    Pem:        float
                Electromechanical power in watts.
    slip:       float
                Slip factor in rad/sec.
    
    Returns
    -------
    Pr:         float
                Power related to the rotor in watts.
    
    See Also
    --------
    pstator:         Stator Power Calculator for Induction Machines
    """
    Pr = -slip * (Pem / (1 - slip))
    return Pr


def de_calc(rho, freq=60):
    r"""
    Calculator for De Transmission Line Value
    
    Simple calculator to find the De value for a line
    with particular earth resistivity (rho).
    
    .. math:: D_e=D_{e_{\text{constant}}}\sqrt{\frac{\rho}{freq}}
    
    Parameters
    ----------
    rho:        float
                Earth resistivity (in ohm-meters), may also
                be passed a string in the set: {SEA, SWAMP,
                AVG,AVERAGE,DAMP,DRY,SAND,SANDSTONE}
    freq:       float, optional
                System frequency in Hertz, default=60
    """
    if isinstance(rho, str):
        rho = rho.upper()
        rho = {'SEA':0.01,  'SWAMP':10, 
         'AVG':100, 
         'AVERAGE':100, 
         'DAMP':100, 
         'DRY':1000, 
         'SAND':1000000000.0, 
         'SANDSTONE':1000000000.0}[rho]
    De = De0 * _np.sqrt(rho / freq)
    return De


def zperlength(Rd=None, Rself=None, Rac=None, Rgwac=None, De=None, rho='AVG', Ds=None, Dsgw=None, dia_gw=None, Dab=None, Dbc=None, Dca=None, Dagw=None, Dbgw=None, Dcgw=None, resolve=True, freq=60):
    """
    Transmission Line Impedance (RL) Calculator
    
    Simple impedance matrix generator to provide the full
    impedance per length matrix.
    
    Parameters
    ----------
    Rd:         float, optional
                Resistance Rd term in ohms, will be generated
                automatically if set to None, default=None
    Rself:      float, optional
                Self Resistance term in ohms.
    Rac:        float, optional
                AC resistance in ohms.
    Rgwac:      float, optional
                Ground-Wire AC resistance in ohms.
    De:         float, optional
                De term, in feet, if None provided, and `rho`
                parameter is specified, will interpretively be
                calculated.
    rho:        float, optional
                Earth resistivity in ohm-meters. default="AVG"
    Ds:         float, optional
                Distance (self) for each phase conductor in feet,
                commonly known as GMD.
    Dsgw:       float, optional
                Distance (self) for the ground wire conductor in
                feet, commonly known as GMD.
    dia_gw:     float, optional
                Ground-Wire diameter in feet, may be used to
                calculate an approximate Dsgw if no Dsgw is provided.
    Dab:        float, optional
                Distance between phases A and B, in feet.
    Dbc:        float, optional
                Distance between phases B and C, in feet.
    Dca:        float, optional
                Distance between phases C and A, in feet.
    Dagw:       float, optional
                Distance between phase A and ground conductor, in feet.
    Dbgw:       float, optional
                Distance between phase B and ground conductor, in feet.
    Dcgw:       float, optional
                Distance between phase C and ground conductor, in feet.
    resolve:    bool, optional
                Control argument to specify whether the resultant
                ground-wire inclusive per-length impedance matrix
                should be reduced to a 3x3 equivalent matrix.
                default=True
    freq:       float, optional
                System frequency in Hertz.
    """
    Rperlen = 0
    Lperlen = 0
    if Rd == None:
        Rd = freq * carson_r
    if Dsgw == None:
        if dia_gw != None:
            Dsgw = _np.exp(-0.25) * dia_gw / 2
    if Rd > 0:
        if Rself == None:
            if not all((Rd, Rac)):
                raise ValueError('Too few arguments')
            Rself = Rac + Rd
        Rperlen = _np.array([
         [
          Rself, Rd, Rd],
         [
          Rd, Rself, Rd],
         [
          Rd, Rd, Rself]])
        if all((Rgwac, Dsgw, Dagw, Dbgw, Dcgw)):
            Rselfgw = Rgwac + Rd
            Rperlen = _np.append(Rperlen, [
             [
              Rd], [Rd], [Rd]],
              axis=1)
            Rperlen = _np.append(Rperlen, [
             [
              Rd, Rd, Rd, Rselfgw]],
              axis=0)
    if any((De, Ds, rho)):
        if not all((Dab, Dbc, Dca)):
            raise ValueError('Distance Terms [Dab,Dbc,Dca] Required')
        if Ds == None:
            raise ValueError('Distance Self (Ds) Required')
        if De == None:
            if rho == None:
                raise ValueError('Too few arguments')
            De = de_calc(rho, freq)
        Lperlen = _np.array([
         [
          _np.log(De / Ds), _np.log(De / Dab), _np.log(De / Dca)],
         [
          _np.log(De / Dab), _np.log(De / Ds), _np.log(De / Dbc)],
         [
          _np.log(De / Dca), _np.log(De / Dbc), _np.log(De / Ds)]])
        if all((Rgwac, Dsgw, Dagw, Dbgw, Dcgw)):
            Lperlen = _np.append(Lperlen, [
             [
              _np.log(De / Dagw)], [_np.log(De / Dbgw)], [_np.log(De / Dcgw)]],
              axis=1)
            Lperlen = _np.append(Lperlen, [
             [
              _np.log(De / Dagw), _np.log(De / Dbgw),
              _np.log(De / Dcgw), _np.log(De / Dsgw)]],
              axis=0)
        Lperlen = Lperlen * (complex(0.0, 1.0) * u0 * freq)
    Zperlen = Rperlen + Lperlen
    if resolve:
        if all((Rgwac, Dsgw, Dagw, Dbgw, Dcgw)):
            Za = Zperlen[:3, :3]
            Zb = Zperlen[:3, 3:4]
            Zc = Zperlen[3:4, :3]
            Zd = Zperlen[3:4, 3:4]
            Zperlen = Za - _np.dot(Zb, _np.dot(_np.linalg.inv(Zd), Zc))
    return Zperlen


def transposez(Zeq, fabc=0.3333333333333333, fcab=0.3333333333333333, fbca=0.3333333333333333, linelen=1):
    r"""
    Transmission Matrix Equivalent Transposition Calculator
    
    Given the impedance matrix and the percent of the line spent
    in each transposition relation (ABC, CAB, and BCA).
    
    .. math::
       f_{abc}Z_{eq}+f_{cab}R_p^{-1}\cdot Z_{eq}\cdot R_p+
       f_{bca}Z_{eq}R_p\cdot Z_{eq}\cdot R_p^{-1}
    
    where:
    
    .. math:
       R_p=\begin{bmatrix}\\
       0 & 0 & 1 \\
       1 & 0 & 0 \\
       0 & 1 & 0 \\
       \end{bmatrix}
    
    Parameters
    ----------
    Zeq:        array_like
                Per-Length (or total length) line impedance in ohms.
    fabc:       float, optional
                Percentage of line set with phase relation ABC,
                default=1/3
    fcab:       float, optional
                Percentage of line set with phase relation CAB,
                default=1/3
    fbca:       float, optional
                Percentage of line set with phase relation BCA,
                default=1/3
    linelen:    Length of line (unitless), default=1
    """
    Zeq = _np.asarray(Zeq)
    Rp = _np.array([
     [
      0, 0, 1],
     [
      1, 0, 0],
     [
      0, 1, 0]])
    _Rp = np.linalg.inv(Rp)
    Zeq = fabc * Zeq + fcab * _Rp.dot(Zeq.dot(Rp)) + fbca * Rp.dot(Zeq.dot(_Rp))
    Zeq = Zeq * linelen
    return Zeq


def gmd(Ds, *args):
    r"""
    Simple GMD Calculator
    
    Calculates the GMD (Geometric Mean Distance) for a system
    with the parameters of a list of arguments.
    
    .. math:: GMD=(D_s*D_1*\ddot*D_n)^{\frac{1}{1+n}}
    
    Parameters
    ----------
    Ds:         float
                Self distance (unitless), normally provided from
                datasheet/reference
    *args:      floats, optional
                Remaining set of distance values (unitless)
    """
    root = len(args) + 1
    gmdx = Ds
    for dist in args:
        gmdx *= dist
    else:
        GMD = gmdx ** (1 / root)
        return GMD


def indmachfocratings(Rr, Rs, Lm, Llr=0, Lls=0, Lr=None, Ls=None, Vdqs=1, Tem=1, wes=1):
    """
    FOC Ind. Machine Rated Operation Calculator
    
    Determines the parameters and characteristics of a Field-
    Oriented-Controlled Induction Machine operating at its
    rated limits.
    
    Parameters
    ----------
    Rr:         float
                Rotor resistance in per-unit-ohms
    Rs:         float
                Stator resistance in per-unit-ohms
    Lm:         float
                Magnetizing inductance in per-unit-Henrys
    Llr:        float, optional
                Rotor leakage inductance in per-unit-Henrys,
                default=0
    Lls:        float, optional
                Stator leakage inductance in per-unit-Henrys,
                default=0
    Lr:         float, optional
                Rotor inductance in per-unit-Henrys
    Ls:         float, optional
                Stator inductance in per-unit-Henrys
    Vdqs:       complex, optional
                The combined DQ-axis voltage required for rated
                operation, in per-unit-volts, default=1+j0
    Tem:        float, optional
                The mechanical torque required for rated operation,
                in per-unit-newton-meters, default=1
    wes:        float, optional
                The per-unit electrical system frequency, default=1
    
    Returns
    -------
    Idqr:       complex
                Combined DQ-axis Rotor Current in per-unit-amps
    Idqs:       complex
                Combined DQ-axis Stator Current in per-unit-amps
    LAMdqr:     complex
                Combined DQ-axis Rotor Flux in per-unit
    LAMdqs:     complex
                Combined DQ-axis Stator Flux in per-unit
    slip_rat:   float
                Rated Slip as percent of rotational and system frequencies
    w_rat:      float
                Rated System frequency in per-unit-rad/sec
    lamdr_rat:  float
                Rated D-axis rotor flux in per-unit
    """
    if Ls == None:
        Ls = Lls + Lm
    if Lr == None:
        Lr = Llr + Lm

    def equations(val):
        Idr, Iqr, Ids, Iqs, LAMdr, LAMqr, LAMds, LAMqs, wr = val
        A = Rs * Ids - wes * LAMqs - Vdqs
        B = Rs * Iqs - wes * LAMds
        C = Rr * Idr - (wes - wr) * LAMqr
        D = Rr * Iqr + (wes - wr) * LAMdr
        E = Ls * Ids + Lm * Idr - LAMds
        F = Ls * Iqs + Lm * Iqr - LAMqs
        G = Lm * Ids + Lr * Idr - LAMdr
        H = Lm * Iqs + Lr * Iqr - LAMqr
        I = Lm / Lr * (LAMdr * Iqs - LAMqr * Ids) - Tem
        return (A, B, C, D, E, F, G, H, I)

    Idr0 = -1
    Iqr0 = -1
    Ids0 = 1
    Iqs0 = 1
    LAMdr0 = Lm * Ids0 + Lr * Idr0
    LAMqr0 = Lm * Iqs0 + Lr * Iqr0
    LAMds0 = Ls * Ids0 + Lm * Idr0
    LAMqs0 = Ls * Iqs0 + Lm * Iqr0
    wr = 1
    Idr, Iqr, Ids, Iqs, LAMdr, LAMqr, LAMds, LAMqs, wr = _fsolve(equations, (
     Idr0, Iqr0, Ids0, Iqs0, LAMdr0, LAMqr0, LAMds0, LAMqs0, wr))
    slip_rated = (wes - wr) / wes
    w_rated = wr
    lamdr_rated = abs(LAMdr + complex(0.0, 1.0) * LAMqr)
    return (
     compose(Idr, Iqr),
     compose(Ids, Iqs),
     compose(LAMdr, LAMqr),
     compose(LAMds, LAMqs),
     slip_rated,
     w_rated,
     lamdr_rated)


def imfoc_control(Tem_cmd, LAMdr_cmd, wr_cmd, Rr, Rs, Lm, Llr=0, Lls=0, Lr=None, Ls=None, s_err=0):
    """
    FOC Ind. Machine Rated Operation Calculator
    
    Determines the parameters and characteristics of a Field-
    Oriented-Controlled Induction Machine operating at its
    rated limits.
    
    Parameters
    ----------
    Tem_cmd:    float
                Mechanical torque setpoint in per-unit-newton-meters
    LAMdr_cmd:  float
                D-axis flux setpoint in per-unit
    wr_cmd:     float
                Mechanical (rotor) speed in per-unit-rad/sec
    Rr:         float
                Rotor resistance in per-unit-ohms
    Rs:         float
                Stator resistance in per-unit-ohms
    Lm:         float
                Magnetizing inductance in per-unit-Henrys
    Llr:        float, optional
                Rotor leakage inductance in per-unit-Henrys,
                default=0
    Lls:        float, optional
                Stator leakage inductance in per-unit-Henrys,
                default=0
    Lr:         float, optional
                Rotor inductance in per-unit-Henrys
    Ls:         float, optional
                Stator inductance in per-unit-Henrys
    s_err:      float, optional
                Error in slip calculation as a percent (e.g. 0.25),
                default=0
    
    Returns
    -------
    Vdqs:       complex
                Combined DQ-axis Stator Voltage in per-unit volts
    Idqr:       complex
                Combined DQ-axis Rotor Current in per-unit-amps
    Idqs:       complex
                Combined DQ-axis Stator Current in per-unit-amps
    LAMdqr:     complex
                Combined DQ-axis Rotor Flux in per-unit
    LAMdqs:     complex
                Combined DQ-axis Stator Flux in per-unit
    wslip:      float
                Machine Slip frequency in per-unit-rad/sec
    wes:        float
                The electrical system frequency in per-unit-rad/sec
    """
    if Ls == None:
        Ls = Lls + Lm
    if Lr == None:
        Lr = Llr + Lm
    sigma = 1 - Lm ** 2 / (Ls * Lr)
    accuracy = 1 + s_err
    Ids = LAMdr_cmd / Lm
    Iqs = Tem_cmd / (Lm / Lr * LAMdr_cmd)
    wslip = Rr / (Lr * accuracy) * (Lm * Iqs) / LAMdr_cmd
    wes = wslip + wr_cmd
    Vds = Rs * Ids - wes * sigma * Ls * Iqs
    Vqs = Rs * Iqs - wes * Ls * Ids
    Iqr = -Lm / Lr * Iqs
    Idr = 0
    LAMqr = 0
    LAMqs = sigma * Ls * Iqs
    LAMds = Ls * Ids
    return (
     compose(Vds, Vqs),
     compose(Idr, Iqr),
     compose(Ids, Iqs),
     compose(LAMdr_cmd, LAMqr),
     compose(LAMds, LAMqs),
     wslip,
     wes)


def synmach_Eq(Vt_pu, Itmag, PF, Ra, Xd, Xq):
    r"""
    Synchronous Machine Eq Calculator
    
    Given specified parameter set, will calculate
    the internal voltage on the q-axis (Eq).
    
    .. math:: E_q=V_{t_{pu}}-\left[R_a\cdot I_{t_{pu}}+
       j\cdot X_q\cdot I_{t_{pu}}+j(X_d-X_q)\cdot I_{ad}\right]
    
    where:
    
    .. math:: I_{t_{pu}}=I_{t_{mag}}\cdot e^{-j(
       \angle{V_{t_{pu}}}-\cos^{-1}(PF))}
    
    .. math:: \theta_q=\angle{V_{t_{pu}}-\left(R_a
       I_{t_{pu}}+j\cdot X_qI_{t_{pu}}\right)
    
    .. math:: I_{ad}=\left|I_{t_{pu}}\cdot\sin(
       -\cos^{-1}(PF)+\theta_q)\right|e^{j(\theta_q
       -90°)}
    
    Parameters
    ----------
    Vt_pu:      complex
                Terminal voltage in per-unit-volts
    Itmag:      float
                Terminal current magnitude in per-
                unit-amps
    PF:         float
                Machine Power Factor, (+)ive values denote
                leading power factor, (-)ive values denote
                lagging power factor
    Ra:         float
                AC resistance in per-unit-ohms
    Xd:         float
                D-axis reactance in per-unit-ohms
    Xq:         float
                Q-axis reactance in per-unit-ohms
    
    Returns
    -------
    Eq:         complex
                Internal Synchronous Machine Voltage
                in per-unit-volts
    """
    phi = _np.arccos(PF)
    Itmag = abs(Itmag)
    It_pu = Itmag * _np.exp(complex(-0.0, -1.0) * (_np.angle(Vt_pu) + phi))
    th_q = _np.angle(Vt_pu - (Ra * It_pu + complex(0.0, 1.0) * Xq * It_pu))
    Iad = abs(It_pu) * _np.sin(phi + th_q) * _np.exp(complex(0.0, 1.0) * (th_q - _np.pi / 2))
    Eq = Vt_pu - (Ra * It_pu + complex(0.0, 1.0) * Xq * It_pu + complex(0.0, 1.0) * (Xd - Xq) * Iad)
    return Eq


def vipf(V=None, I=None, PF=1, find=''):
    """
    Voltage / Current / Power Factor Solver
    
    Given two of the three parameters, will solve for the
    third; beit voltage, current, or power factor.
    
    Parameters
    ----------
    V:          complex
                System voltage (in volts), default=None
    I:          complex
                System current (in amps), default=None
    PF:         float
                System power factor, (+)ive values denote
                leading power factor, (-)ive values denote
                lagging power factor; default=1
    find:       str, optional
                Control argument to specify which value
                should be returned.
    
    Returns
    -------
    V:          complex
                System voltage (in volts), default=None
    I:          complex
                System current (in amps), default=None
    PF:         float
                System power factor, (+)ive values denote
                leading power factor, (-)ive values denote
                lagging poer factor; default=1
    """
    if isinstance(V, float) and isinstance(I, complex):
        phi = -_np.sign(PF) * _np.arccos(PF)
        V = V * _np.exp(complex(-0.0, -1.0) * phi)
    else:
        if isinstance(V, complex) and isinstance(I, float):
            phi = _np.sign(PF) * _np.arccos(PF)
            I = I * _np.exp(complex(-0.0, -1.0) * phi)
        else:
            if all([V, I]):
                phi = _np.angle(V) - _np.angle(I)
                PF = _np.cos(phi)
            else:
                raise ValueError('All values must be provided.')
    find = find.upper()
    if find == 'V':
        return V
    if find == 'I':
        return I
    if find == 'PF':
        return PF
    return (V, I, PF)


def rad_to_rpm(rad):
    """
    Radians-per-Second to RPM Converter
    
    Given the angular velocity in rad/sec, this
    function will evaluate the velocity in RPM
    (Revolutions-Per-Minute).
    
    Parameters
    ----------
    rad:        float
                The angular velocity in radians-
                per-second
    
    Returns
    -------
    rpm:        float
                The angular velocity in revolutions-
                per-minute (RPM)
    """
    rpm = 60 / (2 * _np.pi) * rad
    return rpm


def rpm_to_rad(rpm):
    """
    RPM to Radians-per-Second Converter
    
    Given the angular velocity in RPM (Revolutions-
    Per-Minute), this function will evaluate the
    velocity in rad/sec.
    
    Parameters
    ----------
    rpm:        float
                The angular velocity in revolutions-
                per-minute (RPM)
    
    Returns
    -------
    rad:        float
                The angular velocity in radians-
                per-second
    """
    rad = 2 * _np.pi / 60 * rpm
    return rad


def hz_to_rpm(hz):
    """
    Hertz to RPM Converter
    
    Given the angular velocity in Hertz, this
    function will evaluate the velocity in RPM
    (Revolutions-Per-Minute).
    
    Parameters
    ----------
    hz:         float
                The angular velocity in Hertz
    
    Returns
    -------
    rpm:        float
                The angular velocity in revolutions-
                per-minute (RPM)
    """
    rpm = hz * 60
    return rpm


def rpm_to_hz(rpm):
    """
    RPM to Hertz Converter
    
    Given the angular velocity in RPM (Revolutions-
    Per-Minute), this function will evaluate the
    velocity in Hertz.
    
    Parameters
    ----------
    rpm:        float
                The angular velocity in revolutions-
                per-minute (RPM)
    
    Returns
    -------
    hz:         float
                The angular velocity in Hertz
    """
    hz = rpm / 60
    return hz


def syncspeed(Npol, freq=60, Hz=False):
    r"""
    Synchronous Speed Calculator Function
    
    Simple method of calculating the synchronous
    speed of an induction machine given the number
    of poles in the machine's construction, and
    the machine's operating electrical frequency.
    
    .. math:: \omega_{\text{syn}}=\frac{2\pi
       \cdot\text{freq}}{\frac{N_{\text{pol}}}{2}}
    
    Parameters
    ----------
    Npol:       int
                Number of electrical poles in
                machine's construction.
    freq:       float, optional
                Frequency of electrical system in
                Hertz, default=60
    Hz:         bool, optional
                Boolean control to enable return
                in Hertz. default=False
    
    Returns
    -------
    wsyn:       float
                Synchronous Speed of Induction Machine,
                defaults to units of rad/sec, but may
                be set to Hertz if `Hz` set to True.
    """
    wsyn = 2 * _np.pi * freq / (Npol / 2)
    if Hz:
        return wsyn / (2 * _np.pi)
    return wsyn


def machslip(mech, syn=60):
    r"""
    Machine Slip Calculator
    
    Given the two parameters (mechanical and synchronous
    speed, or frequency) this function will return the
    unitless slip of the rotating machine.
    
    .. math:: \text{slip}=\frac{\text{syn}-\text{mech}}
       {\text{syn}}
    
    Parameters
    ----------
    mech:       float
                The mechanical frequency (or speed),
                of the rotating machine.
    syn:        float, optional
                The synchronous frequency (or speed),
                defaults as a frequency set to 60Hz,
                default=60
    
    Returns
    -------
    slip:       float
                The rotating machine's slip constant.
    """
    slip = (syn - mech) / syn
    return slip