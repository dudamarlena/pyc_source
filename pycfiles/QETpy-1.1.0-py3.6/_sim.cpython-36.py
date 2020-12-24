# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qetpy/sim/_sim.py
# Compiled at: 2019-02-07 14:38:29
# Size of source mod 2**32: 28330 bytes
import numpy as np, scipy.constants as constants
__all__ = [
 'loadfromdidv', 'TESnoise', 'energy_res_estimate']

def energy_res_estimate(freqs, tau_collect, Sp, collection_eff):
    """
    Function to estimate the energy resolution based on
    given noise and ideal pulse shape
    
    Parameters
    ----------
    freqs : array,
        Array of frequency values to integrate over
    tau_collect : float
        The collection time of the sensor
    Sp : array 
        Power spectral density (either one sided or two,
        but make sure to include negative freqs if using
        two sided psd)
    collection_eff : float
        The collection efficiency of the detector
        
    Returns
    -------
    energy_res : float
        The estimated energy resolution in eV
     
    """
    omega = 2 * np.pi * freqs
    single_pole = collection_eff / (1.0 + omega * tau_collect * complex(0.0, 1.0))
    integrand = 2 * np.abs(single_pole) ** 2 / (np.pi * Sp)
    energy_res = np.sqrt(1 / np.trapz(integrand, x=omega)) / constants.e
    return energy_res


def loadfromdidv(DIDVobj, G=5e-10, qetbias=0.00016, tc=0.04, tload=0.9, tbath=0.02, squiddc=2.5e-12, squidpole=0.0, squidn=1.0, noisetype='transition', lgcpriors=False):
    """
    Function for loading the parameters from a DIDV class object.
    
    Parameters
    ----------
    DIDVobj : Object
        A DIDV class object after a fit has been run, such that there are Irwin parameters that
        can be used to model the noise.
    G : float, optional
        The thermal conductance of the TES in W/K
    qetbias : float, optional
        The QET bias in Amps
    tc : float
        The critical temperature of the TES in K
    tload : float
        The effective temperature of the load resistor in K
    tbath : float
        The bath temperature in K
    squiddc : float, optional
        The DC value of the SQUID and downstream electronics noise, in Amps/rtHz. The SQUID/electronics
        noise should have been fit beforehand, using the following model:
            (squiddc*(1.0+(squidpole/f)**squidn))**2.0
    squidpole : float, optional
        The frequency pole for the SQUID and downstream electronics noise, in Hz. The SQUID/electronics
        noise should have been fit beforehand, using the following model:
            (squiddc*(1.0+(squidpole/f)**squidn))**2.0
    squidn : float, optional
        The power of the SQUID and downstream electronics noise, in Hz. The SQUID/electronics
        noise should have been fit beforehand, using the following model:
            (squiddc*(1.0+(squidpole/f)**squidn))**2.0
    noisetype : str, optional
        The type of the noise that is to be loaded. The options are
        transition : Use the Irwin parameters from the two pole fit as the transition noise model
        superconducting : Use the Irwin parameters from the one pole fit as the superconducting noise model
        normal : Use the Irwin parameters from the one pole fit as the normal noise model
    lgcpriors : bool, optional
        If True, the priors fit values are loaded from the didv object, if False, the regular fit values are 
        loaded
            
                
    Returns
    -------
    TESobj : Object
        A TESnoise class object with all of the fit parameters loaded.
    """
    if noisetype is 'superconducting':
        didv_dict = DIDVobj.get_irwinparams_dict(1)
        rshunt = DIDVobj.rshunt
        rload = didv_dict['rtot']
        inductance = didv_dict['L']
        r0 = 0
        beta = 0
        loopgain = 0
        tau0 = 0
        G = 0
        TESobj = TESnoise(rload=rload, r0=r0, rshunt=rshunt, inductance=inductance, beta=beta,
          loopgain=loopgain,
          tau0=tau0,
          G=G,
          qetbias=qetbias,
          tc=tc,
          tload=tload,
          tbath=tbath,
          squiddc=squiddc,
          squidpole=squidpole,
          squidn=squidn)
    else:
        if noisetype is 'normal':
            didv_dict = DIDVobj.get_irwinparams_dict(1)
            rshunt = DIDVobj.rshunt
            rload = didv_dict['rload']
            inductance = didv_dict['L']
            r0 = didv_dict['r0']
            beta = 0
            loopgain = 0
            tau0 = 0
            G = 0
            TESobj = TESnoise(rload=rload, r0=r0, rshunt=rshunt, inductance=inductance, beta=beta,
              loopgain=loopgain,
              tau0=tau0,
              G=G,
              qetbias=qetbias,
              tc=tc,
              tload=tload,
              tbath=tbath,
              squiddc=squiddc,
              squidpole=squidpole,
              squidn=squidn)
        else:
            if noisetype is 'transition':
                didv_dict = DIDVobj.get_irwinparams_dict(2, lgcpriors)
                rshunt = DIDVobj.rshunt
                rload = didv_dict['rload']
                inductance = didv_dict['L']
                r0 = didv_dict['r0']
                beta = didv_dict['beta']
                loopgain = didv_dict['l']
                tau0 = didv_dict['tau0']
                TESobj = TESnoise(rload=rload, r0=r0, rshunt=rshunt, inductance=inductance, beta=beta,
                  loopgain=loopgain,
                  tau0=tau0,
                  G=G,
                  qetbias=qetbias,
                  tc=tc,
                  tload=tload,
                  tbath=tbath,
                  squiddc=squiddc,
                  squidpole=squidpole,
                  squidn=squidn)
            else:
                raise ValueError('Unrecognized noisetype')
    return TESobj


class TESnoise:
    __doc__ = '\n    Class for the simulation of the TES noise using the simple Irwin theory. Supports noise simulation for \n    in transition, superconducting, and normal.\n    \n    Attributes\n    ----------\n    freqs : float, array_like\n        The frequencies for which we will calculate the noise simulation\n    rload : float\n        The load resistance of the TES (sum of shunt and parasitic resistances) in Ohms\n    r0 : float\n        The bias resistance of the TES in Ohms\n    rshunt : float\n        The shunt resistance of the TES circuit in Ohms\n    beta : float\n        The current sensitivity of the TES (dlogR/dlogI), unitless\n    loopgain : float\n        The Irwin loop gain of the TES, unitless\n    inductance : float\n        The inductance of the TES circuit in Henries\n    tau0 : float\n        The thermal time constant (equals C/G) in s\n    G : float\n        The thermal conductance of the TES in W/K\n    qetbias : float\n        The QET bias in Amps\n    tc : float\n        The critical temperature of the TES in K\n    tload : float\n        The effective temperature of the load resistor in K\n    tbath : float\n        The bath temperature in K\n    n : float\n        The power-law dependence of the power flow to the heat bath\n    lgcb : boolean\n        Boolean flag that determines whether we use the ballistic (True) or\n        diffusive limit when calculating TFN power noise\n    squiddc : float\n        The frequency pole for the SQUID and downstream electronics noise, in Hz. The SQUID/electronics\n        noise should have been fit beforehand, using the following model:\n            (squiddc*(1.0+(squidpole/f)**squidn))**2.0\n    squidpole : float\n        The frequency pole for the SQUID and downstream electronics noise, in Hz. The SQUID/electronics\n        noise should have been fit beforehand, using the following model:\n            (squiddc*(1.0+(squidpole/f)**squidn))**2.0\n    squidn : float\n        The power of the SQUID and downstream electronics noise, in Hz. The SQUID/electronics\n        noise should have been fit beforehand, using the following model:\n            (squiddc*(1.0+(squidpole/f)**squidn))**2.0\n    f_tfn : float\n        Function that estimates the noise suppression of the thermal fluctuation noise due\n        to the difference in temperature between the bath and the TES. Supports the ballistic\n        and diffusive limits, which is chosen via lgcb\n        \n    '

    def __init__(self, freqs=None, rload=0.012, r0=0.15, rshunt=0.005, beta=1.0, loopgain=10.0, inductance=4e-07, tau0=0.0005, G=5e-10, qetbias=0.00016, tc=0.04, tload=0.9, tbath=0.02, n=5.0, lgcb=True, squiddc=2.5e-12, squidpole=0.0, squidn=1.0):
        """
        Initialization of the TES noise class.

        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation
        rload : float, optional
            The load resistance of the TES (sum of shunt and parasitic resistances) in Ohms
        r0 : float, optional
            The bias resistance of the TES in Ohms
        rshunt : float, optional
            The shunt resistance of the TES circuit in Ohms
        beta : float, optional
            The current sensitivity of the TES (dlogR/dlogI), unitless
        loopgain : float, optional
            The Irwin loop gain of the TES, unitless
        inductance : float, optional
            The inductance of the TES circuit in Henries
        tau0 : float, optional
            The thermal time constant (equals C/G) in s
        G : float, optional
            The thermal conductance of the TES in W/K
        qetbias : float, optional
            The QET bias in Amps
        tc : float, optional
            The critical temperature of the TES in K
        tload : float, optional
            The effective temperature of the load resistor in K
        tbath : float, optional
            The bath temperature in K
        n : float, optional
            The power-law dependence of the power flow to the heat bath
        lgcb : boolean, optional
            Boolean flag that determines whether we use the ballistic (True) or
            diffusive limit when calculating TFN power noise
        squiddc : float, optional
            The frequency pole for the SQUID and downstream electronics noise, in Hz. The SQUID/electronics
            noise should have been fit beforehand, using the following model:
                (squiddc*(1.0+(squidpole/f)**squidn))**2.0
        squidpole : float, optional
            The frequency pole for the SQUID and downstream electronics noise, in Hz. The SQUID/electronics
            noise should have been fit beforehand, using the following model:
                (squiddc*(1.0+(squidpole/f)**squidn))**2.0
        squidn : float, optional
            The power of the SQUID and downstream electronics noise, in Hz. The SQUID/electronics
            noise should have been fit beforehand, using the following model:
                (squiddc*(1.0+(squidpole/f)**squidn))**2.0

        """
        if freqs is None:
            self.freqs = np.logspace(0, 5.5, 10000)
        else:
            self.freqs = freqs
        self.rload = rload
        self.r0 = r0
        self.rshunt = rshunt
        self.beta = beta
        self.loopgain = loopgain
        self.inductance = inductance
        self.tau0 = tau0
        self.qetbias = qetbias
        self.i0 = self.qetbias * self.rshunt / (self.r0 + self.rload)
        self.tc = tc
        self.tload = tload
        self.G = G
        self.tbath = tbath
        self.n = n
        self.lgcb = lgcb
        self.squiddc = squiddc
        self.squidpole = squidpole
        self.squidn = squidn
        if self.lgcb:
            self.f_tfn = ((self.tbath / self.tc) ** (self.n + 1.0) + 1.0) / 2.0
        else:
            self.f_tfn = self.n / (2.0 * self.n + 1.0) * ((self.tbath / self.tc) ** (2.0 * self.n + 1.0) - 1.0) / ((self.tbath / self.tc) ** self.n - 1.0)

    def dIdV(self, freqs=None):
        """
        The two-pole dIdV function determined from the TES parameters.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        dIdV : float, ndarray
            The two-pole dIdV function
                
        """
        if freqs is None:
            freqs = self.freqs
        omega = 2.0 * np.pi * freqs
        dVdI = self.rload + self.r0 * (1.0 + self.beta) + complex(0.0, 1.0) * omega * self.inductance + self.r0 * self.loopgain / (1.0 - self.loopgain) * (2.0 + self.beta) / (1.0 + complex(0.0, 1.0) * omega * self.tau0 / (1.0 - self.loopgain))
        return 1.0 / dVdI

    def dIdP(self, freqs=None):
        """
        The two-pole dIdP function determined from the TES parameters.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        dIdP : float, ndarray
            The two-pole dIdP function
                
        """
        if freqs is None:
            freqs = self.freqs
        omega = 2.0 * np.pi * freqs
        return 1.0 / self.i0 * 1.0 / (1.0 - 1.0 / self.loopgain) * 1.0 / (1.0 + complex(0.0, 1.0) * omega * self.tau0 / (1.0 - self.loopgain)) * self.dIdV(freqs)

    def s_vload(self, freqs=None):
        """
        The Johnson load voltage noise determined from the TES parameters. This formula holds no
        matter where we are in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_vload : float, ndarray
            The Johnson load voltage noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return 4.0 * constants.k * self.tload * self.rload * np.ones_like(freqs)

    def s_iload(self, freqs=None):
        """
        The Johnson load current noise determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_iload : float, ndarray
            The Johnson load current noise at the specified frequencies
             
             
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_vload(freqs) * np.abs(self.dIdV(freqs)) ** 2.0

    def s_pload(self, freqs=None):
        """
        The Johnson load power noise determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_pload : float, ndarray
            The Johnson load power noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_iload(freqs) / np.abs(self.dIdP(freqs)) ** 2.0

    def s_vtes(self, freqs=None):
        """
        The Johnson TES voltage noise determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_vtes : float, ndarray
            The Johnson TES voltage noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return 4.0 * constants.k * self.tc * self.r0 * (1.0 + self.beta) ** 2.0 * np.ones_like(freqs)

    def s_ites(self, freqs=None):
        """
        The Johnson TES current noise determined from the TES parameters for in transition. 
        This noise has both an electronic and thermal component.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_ites : float, ndarray
            The Johnson TES current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_vtes(freqs) * np.abs(self.dIdV(freqs) - self.i0 * self.dIdP(freqs)) ** 2.0

    def s_ptes(self, freqs=None):
        """
        The Johnson TES power noise determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_ptes : float, ndarray
            The Johnson TES power noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_ites(freqs) / np.abs(self.dIdP(freqs)) ** 2.0

    def s_ptfn(self, freqs=None):
        """
        The thermal fluctuation noise in power determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_ptfn : float, ndarray
            The thermal fluctuation noise in power at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return 4.0 * constants.k * self.tc ** 2.0 * self.G * self.f_tfn * np.ones_like(freqs)

    def s_itfn(self, freqs=None):
        """
        The thermal fluctuation noise in current determined from the TES parameters for in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_itfn : float, ndarray
            The thermal fluctuation noise in current at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_ptfn(freqs) * np.abs(self.dIdP(freqs)) ** 2.0

    def s_isquid(self, freqs=None):
        """
        The SQUID and downstream electronics current noise, currently is using a 1/f model that
        must be specified when initializing the class.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_isquid : float, ndarray
            The SQUID and downstream electronics current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return (self.squiddc * (1.0 + (self.squidpole / freqs) ** self.squidn)) ** 2.0

    def s_psquid(self, freqs=None):
        """
        The SQUID and downstream electronics power noise, currently is using a 1/f model that
        must be specified when initializing the class. This is only used for when the TES is
        in transition.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_psquid : float, ndarray
            The SQUID and downstream electronics power noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_isquid(freqs) / np.abs(self.dIdP(freqs)) ** 2.0

    def s_itot(self, freqs=None):
        """
        The total current noise for the TES in transition. This is calculated by summing each of
        the current noise sources together. Units are [A^2/Hz].
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_itot : float, ndarray
            The total current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_iload(freqs) + self.s_ites(freqs) + self.s_itfn(freqs) + self.s_isquid(freqs)

    def s_ptot(self, freqs=None):
        """
        The total power noise for the TES in transition. This is calculated by summing each of
        the current noise sources together and using dIdP to convert to power noise. Units are [W^2/Hz].
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_ptot : float, ndarray
            The total power noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_itot(freqs) / np.abs(self.dIdP(freqs)) ** 2.0

    def dIdVnormal(self, freqs=None):
        """
        The one-pole dIdV function determined from the TES parameters for when the TES
        is normal.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        dIdVnormal : float, ndarray
            The one-pole dIdV function for when the TES is normal.
                
        """
        if freqs is None:
            freqs = self.freqs
        omega = 2.0 * np.pi * freqs
        return 1.0 / (self.rload + self.r0 + complex(0.0, 1.0) * omega * self.inductance)

    def s_iloadnormal(self, freqs=None):
        """
        The Johnson load current noise determined from the TES parameters for normal.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_iloadnormal : float, ndarray
            The Johnson load current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_vload(freqs) * np.abs(self.dIdVnormal(freqs)) ** 2.0

    def s_vtesnormal(self, freqs=None):
        """
        The Johnson TES voltage noise determined from the TES parameters for normal.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_vtesnormal : float, ndarray
            The Johnson TES voltage noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return 4.0 * constants.k * self.tc * self.r0 * np.ones_like(freqs)

    def s_itesnormal(self, freqs=None):
        """
        The Johnson TES current noise determined from the TES parameters for normal.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_itesnormal : float, ndarray
            The Johnson TES current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_vtesnormal(freqs) * np.abs(self.dIdVnormal(freqs)) ** 2.0

    def s_itotnormal(self, freqs=None):
        """
        The total current noise for the TES when normal. This is calculated by summing each of
        the current noise sources together. Units are [A^2/Hz].
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_itotnormal : float, ndarray
            The total current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_iloadnormal(freqs) + self.s_itesnormal(freqs) + self.s_isquid(freqs)

    def dIdVsc(self, freqs=None):
        """
        The one-pole dIdV function determined from the TES parameters for when the TES
        is superconducting.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        dIdVsc : float, ndarray
            The one-pole dIdV function for when the TES is superconducting.
                
        """
        if freqs is None:
            freqs = self.freqs
        omega = 2.0 * np.pi * freqs
        return 1.0 / (self.rload + complex(0.0, 1.0) * omega * self.inductance)

    def s_iloadsc(self, freqs=None):
        """
        The Johnson load current noise determined from the TES parameters for superconducting.
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_iloadsc : float, ndarray
            The Johnson load current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_vload(freqs) * np.abs(self.dIdVsc(freqs)) ** 2.0

    def s_itotsc(self, freqs=None):
        """
        The total current noise for the TES when superconducting. This is calculated by summing each of
        the current noise sources together. Units are [A^2/Hz].
        
        Parameters
        ----------
        freqs : float, ndarray, optional
            The frequencies for which we will calculate the noise simulation. If left as None, the 
            function will use the values from the initialization.
                
        Returns
        -------
        s_itotsc : float, ndarray
            The total current noise at the specified frequencies
                
        """
        if freqs is None:
            freqs = self.freqs
        return self.s_iloadsc(freqs) + self.s_isquid(freqs)