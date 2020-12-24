# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/AMAT/planet.py
# Compiled at: 2020-05-06 18:25:32
# Size of source mod 2**32: 26823 bytes
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import rcParams
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

class Planet:
    __doc__ = "\n\tThe Planet class is used to store planetary constants, \n\tload atmospheric data from look-up tables, and define\n\tnon-dimensional parameters used in the simulations.\n\t\n\tAttributes\n\t----------\n\tID : str\n\t\tString identifier of planet object\n\tRP : float\n\t\tMean equatorial radius of the target planet in meters\n\tOMEGA : float\n\t\tMean angular velocity of rotation of the planet about \n\t\tits axis of rotation in rad/s\n\tGM : float\n\t\tStandard gravitational parameter of the planet in m3/s2\n\trho0 : float\n\t\tReference atmospheric density at the surface of the target \n\t\tplanet in kg/m3\n\tCPCV : float\n\t\tSpecific heat ratio CP/CV at the surface of the planet\n\tJ2 : float\n\t\tzonal harmonic coefficient J2\n\tJ3 : float\n\t\tzonal harmonic coefficient J3\n\th_thres : float\n\t\tAtmospheric model cutoff altitude in meters, \n\t\tdensity is set to 0, if altitude exceeds h_thres\n\th_skip : float\n\t\tIf vehicle altitude exceeds this value, trajectory is cut off\n\t\tand vehicle is assumed to skip off the atmosphere\n\th_trap : float\n\t\tIf vehicle altitude falls below this value, trajectory is cut off\n\t\tand vehicle is assumed to hit the surface\n\th_low : float\n\t\tIf terminal altitude is below this value vehicle is assumed to\n\t\tbe trapped in the atmosphere. \n\tVref : float\n\t\tReference velocity for non-dimensionalization of entry equations\n\ttau : float\n\t\tReference timescale used to non-dimensionalize time, angular rates\n\tOMEGAbar : float\n\t\tReference non-dimensional angular rate of planet's rotation\n\tEARTHG : float\n\t\tReference value of acceleration due to Earth's gravity\n\tATM : numpy.ndarray\n\t\tArray containing the data loaded from atmospheric lookup file\n\tATM_height : numpy.ndarray\n\t\tArray containing height values from atm. look up dat file\n\tATM_temp : numpy.ndarray\n\t\tArray containing temperature values from atm. look up dat file\n\tATM_pressure : numpy.ndarray\n\t\tArray containing pressure values from atm. look up dat file\n\tATM_density : numpy.ndarray\n\t\tArray containing density values from atm. look up dat file\n\tATM_sonic : numpy.ndarray\n\t\tArray containing computed sonic speed values\n\ttemp_int : scipy.interpolate.interpolate.interp1d\n\t\tFunction which interpolates temperature as function of height\n\tpressure_int : scipy.interpolate.interpolate.interp1d\n\t\tFunction which interpolates pressure as function of height\n\tdensity_int : scipy.interpolate.interpolate.interp1d\n\t\tFunction which interpolates density as function of height\n\tsonic_int : scipy.interpolate.interpolate.interp1d\n\t\tFunction which interpolates sonic speed as function of height\n\t"

    def __init__(self, planetID):
        """
                Initializes the planet object with the planetary constants.
                
                Parameters
                ----------
                planetID : str
                        Name of the planetary body, must be all uppercase; 
                        Valid entries are: 'VENUS', 'EARTH', 'MARS',
                        'TITAN', 'URANUS', 'NEPTUNE'

                """
        if planetID == 'VENUS':
            self.ID = 'VENUS'
            self.RP = 6051800.0
            self.OMEGA = -2.99237e-07
            self.GM = 324859900000000.0
            self.rho0 = 64.79
            self.CPCV = 1.289
            self.J2 = 4.458e-06
            self.J3 = 0.0
            self.h_thres = 180000.0
            self.h_skip = 180000.0
            self.h_trap = 10000.0
            self.h_low = 60000.0
        else:
            if planetID == 'EARTH':
                self.ID = 'EARTH'
                self.RP = 6371000.0
                self.OMEGA = 7.272205e-05
                self.GM = 398600400000000.0
                self.rho0 = 1.225
                self.CPCV = 1.4
                self.J2 = 0.0010826
                self.J3 = -2.532e-06
                self.h_thres = 120000.0
                self.h_skip = 120000.0
                self.h_trap = 10000.0
                self.h_low = 50000.0
            else:
                if planetID == 'MARS':
                    self.ID = 'MARS'
                    self.RP = 3389500.0
                    self.OMEGA = 7.088253e-05
                    self.GM = 42828370000000.0
                    self.rho0 = 0.02
                    self.CPCV = 1.289
                    self.J2 = 0.00196045
                    self.J3 = 3.15e-05
                    self.h_thres = 120000.0
                    self.h_skip = 120000.0
                    self.h_trap = 10000.0
                    self.h_low = 50000.0
                else:
                    if planetID == 'TITAN':
                        self.ID = 'TITAN'
                        self.RP = 2575000.0
                        self.OMEGA = 4.545128e-06
                        self.GM = 8978000000000.0
                        self.rho0 = 5.435
                        self.CPCV = 1.4
                        self.J2 = 3.1808e-05
                        self.J3 = -1.88e-06
                        self.h_thres = 1000000.0
                        self.h_skip = 1000000.0
                        self.h_trap = 30000.0
                        self.h_low = 300000.0
                    else:
                        if planetID == 'URANUS':
                            self.ID = 'URANUS'
                            self.RP = 25559000.0
                            self.OMEGA = -0.000101237
                            self.GM = 5793939000000000.0
                            self.rho0 = 0.3788
                            self.CPCV = 1.45
                            self.J2 = 0.0033433
                            self.J3 = 0.0
                            self.h_thres = 1500000.0
                            self.h_skip = 1500000.0
                            self.h_trap = 50000.0
                            self.h_low = 100000.0
                        else:
                            if planetID == 'NEPTUNE':
                                self.ID = 'NEPTUNE'
                                self.RP = 24622000.0
                                self.OMEGA = 0.0001083385
                                self.GM = 6836529900000000.0
                                self.rho0 = 0.44021
                                self.CPCV = 1.45
                                self.J2 = 0.003411
                                self.J3 = 0.0
                                self.h_thres = 1000000.0
                                self.h_skip = 1000000.0
                                self.h_trap = 10000.0
                                self.h_low = 100000.0
                            else:
                                print(' >>> ERR : Invalid planet identifier provided.')
                                print('Valid entries are: VENUS, EARTH, MARS, \t\t\tTITAN, URANUS, NEPTUNE')
        self.Vref = np.sqrt(self.GM / self.RP)
        self.tau = self.RP / self.Vref
        self.OMEGAbar = self.OMEGA * self.tau
        self.EARTHG = 9.80665

    def loadAtmosphereModel(self, datfile, heightCol, tempCol, presCol, densCol, intType='cubic', heightInKmFlag=False):
        """
                Load atmospheric model from a look up table with 
                height, temperature, pressure, and density
                
                Parameters
                ----------
                datfile : str
                        file containing atmospheric lookup table
                heightCol : int
                        column number of height values, assumes unit = meters 
                        (first column = 0, second column = 1, etc.)
                presCol : int
                        column number of pressure values, assumes unit = Pascals 
                        (first column = 0, second column = 1, etc.)
                densCol : int
                        column number of density values, assumes unit = kg/m3 
                        (first column = 0, second column = 1, etc.)
                intType : str, optional
                        interpolation type: 'linear', 'quadratic' or 'cubic'
                        defaults to 'cubic'
                heightInKmFlag : bool, optional
                        optional, set this to True if heightCol has units of km, 
                        False by default
                """
        self.ATM = np.loadtxt(datfile)
        if heightInKmFlag == True:
            self.ATM_height = self.ATM[:, heightCol] * 1000.0
        else:
            self.ATM_height = self.ATM[:, heightCol]
        self.ATM_temp = self.ATM[:, tempCol]
        self.ATM_pressure = self.ATM[:, presCol]
        self.ATM_density = self.ATM[:, densCol]
        self.ATM_sonic = np.sqrt(self.CPCV * self.ATM_pressure / self.ATM_density)
        self.temp_int = interp1d((self.ATM_height), (self.ATM_temp), kind=intType,
          fill_value=0.0,
          bounds_error=False)
        self.pressure_int = interp1d((self.ATM_height), (self.ATM_pressure), kind=intType,
          fill_value=0.0,
          bounds_error=False)
        self.density_int = interp1d((self.ATM_height), (self.ATM_density), kind=intType,
          fill_value=0.0,
          bounds_error=False)
        self.sonic_int = interp1d((self.ATM_height), (self.ATM_sonic), kind=intType,
          fill_value=1e+20,
          bounds_error=False)

    def density(self, h):
        """
                Returns atmospheric density, scalar value, 
                at altitude h (in meters)

                
                Parameters
                ----------
                h : float
                        altitude in meters

                Returns
                ----------
                ans : float
                        atmospheric density at height h
                """
        if h >= 0:
            if h <= self.h_thres:
                return np.float(self.density_int(h))
        if h > self.h_thres:
            return 0
        if h < 0:
            return self.rho0

    def tempvectorized(self, h):
        """
                Returns atmospheric temperature, vector
                at altitudes array h[:] in meters

                
                Parameters
                ----------
                h : numpy.ndarray
                        altitude h[:] at which atmospheric temperature is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric temperature at altitudes h[:], K
                """
        ans = np.zeros(len(h))
        ans[:] = self.temp_int(h[:])
        return ans

    def presvectorized(self, h):
        """
                Returns atmospheric pressure, vector
                at altitudes array h[:] in meters

                Parameters
                ----------
                h : numpy.ndarray
                        altitude h[:] at which atmospheric pressure is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric pressure at altitudes h[:], K
                """
        ans = np.zeros(len(h))
        ans[:] = self.pressure_int(h[:])
        return ans

    def densityvectorized(self, h):
        """
                Returns atmospheric density, vector
                at altitudes array h[:] in meters

                Parameters
                ----------
                h : numpy.ndarray
                        altitude h[:] at which atmospheric density is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric density at altitudes h[:], K
                """
        ans = np.zeros(len(h))
        ans[:] = self.density_int(h[:])
        return ans

    def avectorized(self, h):
        """
                Returns atmospheric sonic speed, vector
                at altitudes array h[:] in meters

                Parameters
                ----------
                h : numpy.ndarray
                        altitude h[:] at which sonic speed is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the sonic speed at altitudes h[:], K
                """
        ans = np.zeros(len(h))
        ans[:] = self.sonic_int(h[:])
        return ans

    def rho(self, r, theta, phi):
        """
                Returns atmospheric density rho, scalar, as a function
                of radial distance from the target planet center r
                as well as longitude theta and latitude phi
                
                
                Parameters
                ----------
                r : float
                        radial distance r measured from the planet center
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                
                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric density at (r,theta,phi)
                """
        h = r - self.RP
        ans = self.density(h)
        return ans

    def rhovectorized(self, r):
        """
                Returns atmospheric density, vector
                at radial distance array r[:] in meters

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance r[:] at which density is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric density at radial distance r[:]
                """
        h = np.zeros(len(r))
        ans = np.zeros(len(r))
        RP_vec = np.ones(len(r)) * self.RP
        h[:] = r[:] - RP_vec[:]
        ans[:] = self.density_int(h[:])
        return ans

    def pressurevectorized(self, r):
        """
                Returns atmospheric pressure, vector
                at radial distance array r[:] in meters

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance r[:] at which pressure is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric pressure at radial distance r[:]
                """
        h = np.zeros(len(r))
        ans = np.zeros(len(r))
        RP_vec = np.ones(len(r)) * self.RP
        h[:] = r[:] - RP_vec[:]
        ans[:] = self.pressure_int(h[:])
        return ans

    def temperaturevectorized(self, r):
        """
                Returns atmospheric temperature, vector
                at radial distance array r[:] in meters

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance r[:] at which temperature is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric temperature at radial distance r[:]
                """
        h = np.zeros(len(r))
        ans = np.zeros(len(r))
        RP_vec = np.ones(len(r)) * self.RP
        h[:] = r[:] - RP_vec[:]
        ans[:] = self.temp_int(h[:])
        return ans

    def sonicvectorized(self, r):
        """
                Returns atmospheric sonic speed, vector
                at radial distance array r[:] in meters

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance r[:] at which sonic speed is desired

                Returns
                ----------
                ans : numpy.ndarray
                        returns the atmospheric speed at radial distance r[:]
                """
        h = np.zeros(len(r))
        ans = np.zeros(len(r))
        RP_vec = np.ones(len(r)) * self.RP
        h[:] = r[:] - RP_vec[:]
        ans[:] = self.sonic_int(h[:])
        return ans

    def rbar(self, r):
        """
                Returns non-dimensional rbar=r/RP
                
                Parameters
                ----------
                r : float
                        radial distance in meters

                Returns
                ----------
                ans : float
                        non-dimensional rbar
                """
        ans = r / self.RP
        return ans

    def rho2(self, rbar, theta, phi):
        """
                Returns atmospheric density rho, scalar, as a function
                of non-dimensional radial distance rbar, longitude theta, 
                and latitude phi
                
                Parameters
                ----------
                rbar : float
                        nondimensional radial distance rbar
                        measured from the planet center
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                
                Returns
                ----------
                ans : float
                        returns the atmospheric density at (rbar,theta,phi)
                """
        r = rbar * self.RP
        ans = self.rho(r, theta, phi)
        return ans

    def rhobar(self, rbar, theta, phi):
        """
                Returns non-dimensional density rhobar = rho / rho0
                as a function of non-dimensional radial distance rbar, 
                longitude theta, and latitude phi
                
                Parameters
                ----------
                rbar : float
                        nondimensional radial distance rbar
                        measured from the planet center
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                
                Returns
                ----------
                ans : float
                        non-dimensional density at (rbar,theta,phi)
                """
        ans = self.rho2(rbar, theta, phi) / self.rho0
        return ans

    def checkAtmProfiles(self, h0=0.0, dh=1000.0):
        """
                Function to check the loaded atmospheric profile data.
                Plots temperature, pressure, density and sonic speed
                as function of altitude.

                Parameters
                ----------
                h0 : float, optional
                        lower limit of altitude, defaults to 0.0
                dh : float, optional
                        height interval
                
                Returns
                ----------
                A plot showing the atmospheric profiles loaded
                from the lookup tables
                """
        h_array = np.linspace(h0, self.h_thres, int(self.h_thres / dh))
        T_array = self.tempvectorized(h_array)
        P_array = self.presvectorized(h_array)
        r_array = self.densityvectorized(h_array)
        a_array = self.avectorized(h_array)
        fig = plt.figure()
        fig.set_size_inches([6.5, 6.5])
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.subplot(2, 2, 1)
        plt.plot(T_array, (h_array * 0.001), 'r-', linewidth=2.0)
        plt.xlabel('Temperature, K', fontsize=12)
        plt.ylabel('Altitude, km', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid('on', linestyle='-', linewidth=0.2)
        plt.subplot(2, 2, 2)
        plt.plot((P_array * 0.001), (h_array * 0.001), 'r-', linewidth=2.0)
        plt.xlabel('Pressure, kPa', fontsize=12)
        plt.ylabel('Altitude, km', fontsize=12)
        plt.xscale('log')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid('on', linestyle='-', linewidth=0.2)
        plt.subplot(2, 2, 3)
        plt.plot(r_array, (h_array * 0.001), 'r-', linewidth=2.0)
        plt.xlabel('Density, kg/m3', fontsize=12)
        plt.ylabel('Altitude, km', fontsize=12)
        plt.xscale('log')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid('on', linestyle='-', linewidth=0.2)
        plt.subplot(2, 2, 4)
        plt.plot(a_array, (h_array * 0.001), 'r-', linewidth=2.0)
        plt.xlabel('Speed of Sound, m/s', fontsize=12)
        plt.ylabel('Altitude, km', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid('on', linestyle='-', linewidth=0.2)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        plt.tight_layout()
        plt.show()

    def computeR(self, h):
        """
                Returns radial distance r, as 
                a function of altitude h, METERS

                Parameters
                ----------
                h : float
                        altitude in meters

                Returns
                ----------
                r : float
                        radial distance r=RP+h
                """
        r = self.RP + h
        return r

    def computeH(self, r):
        """
                Returns altitude h, as 
                a function of radial distance r, METERS

                Parameters
                ----------
                r : float
                        radial distance in meters

                Returns
                ----------
                h : float
                        h = r - RP
                """
        h = r - self.RP
        return h

    def nonDimState(self, r, theta, phi, v, psi, gamma, drange):
        """
                Computes non-dimensional trajectory state variables from 
                dimensional trajectory state variables

                Parameters
                ----------
                r : float
                        radial distance in meters
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                v : float
                        planet-relative speed, m/s
                psi : float
                        heading angle, radians
                gamma : float
                        planet-relative flight-path angle, radians
                drange : float
                        downrange distance measured from entry-interface

                Returns
                ----------
                rbar : float
                        non-dimensional radial distance in meters
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, radians
                gamma : float
                        planet-relative flight-path angle, radians
                drangebar : float
                        non-dimensional downrange distance measured from 
                        entry-interface
                """
        rbar = r / self.RP
        vbar = v / self.Vref
        drangebar = drange / self.RP
        return (
         rbar, theta, phi, vbar, psi, gamma, drangebar)

    def dimensionalize(self, tbar, rbar, theta, phi, vbar, psi, gamma, drangebar):
        """
                Computes dimensional trajectory state variables from 
                non-dimensional trajectory state variables

                Parameters
                ----------
                rbar : float
                        non-dimensional radial distance in meters
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, radians
                gamma : float
                        planet-relative flight-path angle, radians
                drangebar : float
                        non-dimensional downrange distance measured from 
                        entry-interface

                Returns
                ----------
                r : float
                        radial distance in meters
                theta : float
                        longitude theta(RADIANS), theta in [-PI,PI]     
                phi : float     
                        latitude phi (RADIANS), phi in (-PI/2, PI/2)
                v : float
                        planet-relative speed, m/s
                psi : float
                        heading angle, radians
                gamma : float
                        planet-relative flight-path angle, radians
                drange : float
                        downrange distance measured from entry-interface

                """
        t = self.tau * tbar
        r = rbar * self.RP
        v = vbar * self.Vref
        drange = drangebar * self.RP
        return (
         t, r, theta, phi, v, psi, gamma, drange)

    def scaleHeight(self, h, density_int):
        """
                Returns the scale height as a function of altitude 
                for given density profile 
                
                Parameters
                ----------
                h : float
                        altitude at which scale height is desired
                density_int  : scipy.interpolate.interpolate.interp1d
                        density interpolation function
                --
                Returns
                --
                ans : float
                        scale height, meters
                """
        h_array = np.linspace(0, self.h_skip, int(self.h_skip / 1000.0))
        d_array = self.densityvectorized(h_array)
        integ = cumtrapz((d_array[int(h / 1000.0):]), (h_array[int(h / 1000.0):]),
          initial=0)[(-1)]
        ans = integ / (self.density(h) - self.density(self.h_skip))
        return ans

    def loadMonteCarloDensityFile2(self, atmfile, heightCol, densLowCol, densAvgCol, densHighCol, densTotalCol, heightInKmFlag=False):
        """
                Loads a Monte Carlo density look up table from GRAM-Model output

                Parameters
                ----------
                atmfile : str
                        filename, contains mean density profile data
                heightCol : int
                        column number of height values, assumes unit = meters 
                        (first column = 0, second column = 1, etc.)
                densLowCol : int
                        column number of the low mean density 
                densAvgCol : int
                        column number of the average mean density
                densHigCol : int
                        column number of the high mean desnity
                densTotalCol : int
                        column number of the total (=mean + perturb.) density
                heightinKmFlag : bool, optional
                        optional, set this to True if heightCol has units of km, 
                        False by default

                Returns
                ----------
                ATM_height : numpy.ndarray
                        height array, m
                ATM_density_low : numpy.ndarray
                        low density array, kg/m3
                ATM_density_avg : numpy.ndarray
                        avg. density array, kg/m3
                ATM_density_high : numpy.ndarray
                        high density array, kg/m3
                ATM_density_pert : numpy.ndarray
                        1 sigma mean deviation from avg

                """
        ATM = np.loadtxt(atmfile)
        if heightInKmFlag == True:
            ATM_height = ATM[:, heightCol] * 1000.0
        else:
            ATM_height = ATM[:, heightCol]
        ATM_density_low = ATM[:, densLowCol]
        ATM_density_avg = ATM[:, densAvgCol]
        ATM_density_high = ATM[:, densHighCol]
        ATM_density_pert = ATM[:, densTotalCol] - ATM[:, densAvgCol]
        return (
         ATM_height, ATM_density_low, ATM_density_avg,
         ATM_density_high, ATM_density_pert)

    def pSigmaFunc(self, x):
        """
                Utility function. Returns 1 if x>=0, 0.0 otherwise
                
                Parameters
                ----------
                x : float
                        input x

                Returns
                ----------
                ans : float
                        1 if x>=0, 0.0 otherwise 

                """
        if x >= 0:
            return 1.0
        return 0.0

    def nSigmaFunc(self, x):
        """
                Utility function. Returns 1 if x<0, 0.0 otherwise
                
                Parameters
                ----------
                x : float
                        input x

                Returns
                ----------
                ans : float
                        1 if x<0, 0.0 otherwise 

                """
        if x < 0:
            return 1.0
        return 0.0

    def loadAtmosphereModel5(self, ATM_height, ATM_density_low, ATM_density_avg, ATM_density_high, ATM_density_pert, sigmaValue, NPOS, i):
        """
                Read and create density_int for a single entry from a list 
                of perturbed monte carlo density profiles.
                
                Parameters
                ----------
                ATM_height : numpy.ndarray
                        height array, m
                ATM_density_low : numpy.ndarray
                        low density array, kg/m3
                ATM_density_avg : numpy.ndarray
                        avg. density array, kg/m3
                ATM_density_high : numpy.ndarray
                        high density array, kg/m3
                ATM_density_pert : numpy.ndarray
                        1 sigma mean deviation from avg
                sigmaValue : float
                        mean desnity profile sigma deviation value
                        (intended as input from a normal distribution
                        with mean=0, sigma=1)
                NPOS : int
                        NPOS value from GRAM model
                        equals the number of positions (altitude) for which
                        density value is available in look up table.

                Returns
                ----------
                density_int : scipy.interpolate.interpolate.interp1d
                        density interpolation function

                """
        nSigma = ATM_density_avg[int((i - 1) * NPOS):int(i * NPOS)] - ATM_density_low[int((i - 1) * NPOS):int(i * NPOS)]
        pSigma = ATM_density_high[int((i - 1) * NPOS):int(i * NPOS)] - ATM_density_avg[int((i - 1) * NPOS):int(i * NPOS)]
        h_array = ATM_height[int((i - 1) * NPOS):int(i * NPOS)]
        d_array = ATM_density_avg[int((i - 1) * NPOS):int(i * NPOS)] + pSigma * self.pSigmaFunc(sigmaValue) * sigmaValue + nSigma * self.nSigmaFunc(sigmaValue) * sigmaValue + ATM_density_pert[int((i - 1) * NPOS):int(i * NPOS)]
        density_int = interp1d(h_array, d_array, kind='linear', fill_value=0.0,
          bounds_error=False)
        return density_int