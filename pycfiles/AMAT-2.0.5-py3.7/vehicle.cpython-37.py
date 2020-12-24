# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/AMAT/vehicle.py
# Compiled at: 2020-03-04 20:59:53
# Size of source mod 2**32: 143352 bytes
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import cumtrapz
import copy, random as rd, os

class Vehicle:
    __doc__ = '\n\tThe Vehicle class is used to define vehicle parameters, \n\tsuch as mass, aerodynamics, and aeroheating relations.\n\n\tAttributes\n\t----------\n\tvehicleID : str\n\t\tidentifier string for vehicle object\n\tmass : float\n\t\tvehicle mass, kg\n\tbeta : float\n\t\tvehicle ballistic coefficient, kg/m2\n\tLD : float\n\t\tvehicle lift-to-drag ratio\n\tA : float\n\t\tvehicle reference aerodynamic area, m2\n\talpha : float\n\t\tvehicle angle-of-attack, currently not implemented, rad\n\tRN : float\n\t\tvehicle nose-radius, m\n\tplanetObj : planet.Planet\n\t\tplanet object associated with the vehicle, indicates\n\t\tthe planetary atmosphere in which the vehicle will\n\t\toperate in\n\tAbar : float\n\t\tvehicle non-dimensional reference area\n\tmbar : float\n\t\tvehicle non-dimensional mass\n\tCD : float\n\t\tvehicle drag coefficient\n\tCL : float\n\t\tvehicle lift coefficient\n\th0_km : float\n\t\tinitial vehicle altitude at atmospheric interface / other \n\t\tstart point, meters\n\ttheta0_deg : float\n\t\tinitial vehicle longitude at atmospheric interface / other \n\t\tstart point, degrees\n\tphi0_deg : float\n\t\tinitial vehicle latitude at atmospheric interface / other \n\t\tstart point, degrees\n\tv0_kms : float\n\t\tinitial vehicle speed (planet-relative) at atmospheric\n\t    interface / other  start point, km/s\n\tpsi0_deg : float\n\t\tinitial vehicle heading at atmospheric interface / other \n\t\tstart point, degrees\n\tgamma0_deg : float\n\t\tinitial vehicle flight-path angle at atmospheric interface\n\t\t/ other start point, degrees\n\tdrange0_km : float\n\t\tinitial vehicle downrange at atmospheric interface\n\t\t/ other start point, km\n\theatLoad0 : float\n\t\tinitial vehicle heatload at atmospheric interface\n\t\t/ other start point, J/cm2\n\ttol : float\n\t\tsolver tolerance, currently both abstol and reltol\n\t\tare set to this value\n\tindex : int\n\t\tarray index of the event location if one was detected, \n\t\tterminal index otherwise\n\texitflag : int\n\t\tflag to indicate and classify event occurence \n\t\tor lack of it\t\t\t\n\ttc : numpy.ndarray\n\t\ttruncated time array, sec\n\trc : numpy.ndarray\n\t\ttruncated radial distance array, m\n\tthetac : numpy.ndarray\n\t\ttruncated longitude solution array, rad\n\tphic : numpy.ndarray\n\t\ttruncated latitude solution, rad\n\tvc : numpy.ndarray\n\t\ttruncated speed solution array, m/s\n\tpsic : numpy.ndarray\n\t\ttruncated heading angle solution, rad\n\tgammac : numpy.ndarray\n\t\ttruncated flight-path angle solution, rad\n\tdrangec : numpy.ndarray\n\t\ttruncated downrange solution array, m\n\tt_minc : numpy.ndarray\n\t\ttruncated time array, minutes\n\th_kmc : numpy.ndarray\n\t\ttruncated altitude array, km\n\tv_kmsc : numpy.ndarray\n\t\ttruncated speed array, km/s\n\tphi_degc : numpy.ndarray\n\t\ttruncated latitude array, deg\n\tpsi_degc : numpy.ndarray\n\t\ttruncated heading angle, deg\n\ttheta_degc : numpy.ndarray\n\t\ttruncated longitude array, deg\n\tgamma_degc : numpy.ndarray\n\t\ttruncared flight-path angle array, deg\n\tdrange_kmc : numpy.ndarray\n\t\ttruncated downrange array, km\n\tacc_net_g  : numpy.ndarray\n\t\tacceleration load solution, Earth G      \n\tacc_drag_g  : numpy.ndarray\n\t\tdrag acceleration solution, Earth G      \n\tdyn_pres_atm : numpy.ndarray\n\t\tdynamic pressure solution, Pa\n\tstag_pres_atm : numpy.ndarray\n\t\tstagnation pressure solution, Pa\n\tq_stag_con : numpy.ndarray\n\t\tstagnation-point convective heat rate, W/cm2\n\tq_stag_rad : numpy.ndarray\n\t\tstagnation-point radiative heat rate, W/cm2\n\tq_stag_total : numpy.ndarray\n\t\tstagnation-point radiative tottal heat rate, W/cm2\n\theatload : numpy.ndarray\n\t\tstagnation point heat load, J/cm2 \n\tmaxRollRate : float\n\t\tmaximum allowed roll rate, degrees per second\n\tbeta1: float\n\t\tbeta1 (smaller ballistic coeff.) for drag modulation, kg/m2\n\tbetaRatio : float\n\t\tballistic coefficient ratio for drag modulation \n\ttarget_peri_km : float\n\t\tvehicle target periapsis altitude, km\n\ttarget_apo_km : float\n\t\tvehicle target apoapsis altitude, km\n\ttarget_apo_km_tol : float\n\t\tvehicle target apoapsis altitude error tolerance, km\n\t\tused by guidance algorithm\n\tGhdot : float\n\t\tGhdot term for vehicle equilibrium glide phase\n\tGq : float\n\t\tGq term for vehicle equilibrium glide phase guidance\n\tv_switch_kms : float\n\t\tspeed below which eq. glide phase is terminated\n\tt_step_array : numpy.ndarray\n\t\ttime step array for guided aerocapture trajectory, min\n\tdelta_deg_array : numpy.ndarray\n\t\tbank angle array for guided aerocapture trajectory, deg\n\thdot_array : numpy.ndarray\n\t\taltitude rate array for guided aerocapture trajectory, m/s\n\thddot_array : numpy.ndarray\n\t\taltitude acceleration array for guided aerocapture, m/s2\n\tqref_array : numpy.ndarray\n\t\treference dynamic pressure array for guided aerocapture, Pa\n\tq_array : numpy.ndarray\n\t\tactual dynamic pressure array for guided aerocapture, Pa\n\th_step_array : numpy.ndarray\n\t\taltitude array for guided aerocapture, meters\n\tacc_step_array : numpy.ndarray\n\t\tacceleration array for guided aerocapture, Earth G\n\tacc_drag_array : numpy.ndarray\n\t\tacceleration due to drag for guided aerocapture, Earth G \n\tdensity_mes_array : numpy.ndarray\n\t\tmeasured density array during descending leg, kg/m3\n\tdensity_mes_int : scipy.interpolate.interpolate.interp1d\n\t\tmeasured density interpolation function\n\tminAlt : float\n\t\tminimum altitude at which density measurement is available, km\n\tlowAlt_km : float\n\t\tlower altitude to which density model is to be extrapolated\n\t\tbased on available measurements, km\n\tnumPoints_lowAlt : int\n\t\tnumber of points to evaluate extrapolation at below the \n\t\taltitude where measurements are available\n\thdot_threshold : float\n\t\tthreshold altitude rate (m/s) above which density measurement\n\t\tis terminated and apoapsis prediction is initiated\n\tt_min_eg : numpy.ndarray\n\t\ttime solution of equilibrium glide phase, min\n\th_km_eg : numpy.ndarray\n\t\taltitude array of equilibrium glide phase, km\n\tv_kms_eg : numpy.ndarray\n\t\tspeed solution of equilibrium glide phase, km/s\n\ttheta_deg_eg : numpy.ndarray\n\t\tlongitude solution of equilibrium glide phase, deg\n\tphi_deg_eg : numpy.ndarray\n\t\tlatitude solution of equilibrium glide phase, deg\n\tpsi_deg_eg : numpy.ndarray\n\t\theading angle solution of equilibrium glide phase, deg\n\tgamma_deg_eg : numpy.ndarray\n\t\tflight-path angle solution of eq. glide phase, deg\n\tdrange_km_eg : numpy.ndarray\n\t\tdownrange solution of eq. glide phase, km\n\tacc_net_g_eg : numpy.ndarray\n\t\tacceleration solution of eq. glide phase, Earth G\n\tdyn_pres_atm_eg : numpy.ndarray\n\t\tdynamic pressure solution of eq. glide phase, atm\n\tstag_pres_atm_eg : numpy.ndarray\n\t\tstagnation pressure solution of eq. glide phase, atm\n\tq_stag_total_eg : numpy.ndarray\n\t\tstag. point total heat rate of eq. glide phase, W/cm2\n\theatload_eg : numpy.ndarray\n\t\tstag. point heatload solution of eq. glide phase, J/cm2\n\tt_switch : float\n\t\tswtich time from eq. glide to exit phase, min\n\th_switch : float\n\t\taltitude at which guidance switched to exit phase, km\n\tv_switch : float\n\t\tspeed at which guidance switched to exit phase, km/s\n\tp_switch : float\n\t\tbank angle at which guidance switched to exit phase, deg\n\tt_min_full : numpy.ndarray\n\t\ttime solution of full \n\t\t(eq. gllide + exit phase), min\n\th_km_full : numpy.ndarray\n\t\taltitude array of full \n\t\t(eq. gllide + exit phase), km\n\tv_kms_full : numpy.ndarray\n\t\tspeed solution of full \n\t\t(eq. gllide + exit phase), km/s\n\ttheta_deg_full : numpy.ndarray\n\t\tlongitude solution of full \n\t\t(eq. gllide + exit phase), deg\n\tphi_deg_full : numpy.ndarray\n\t\tlatitude solution of full \n\t\t(eq. gllide + exit phase), deg\n\tpsi_deg_full : numpy.ndarray\n\t\theading angle solution of full \n\t\t(eq. gllide + exit phase), deg\n\tgamma_deg_full : numpy.ndarray\n\t\tflight-path angle solution of full (eq. gllide + exit phase), deg\n\tdrange_km_full : numpy.ndarray\n\t\tdownrange solution of full \n\t\t(eq. gllide + exit phase), km\n\tacc_net_g_full : numpy.ndarray\n\t\tacceleration solution of full \n\t\t(eq. gllide + exit phase), Earth G\n\tdyn_pres_atm_full : numpy.ndarray\n\t\tdynamic pressure solution of full \n\t\t(eq. gllide + exit phase), atm\n\tstag_pres_atm_full : numpy.ndarray\n\t\tstagnation pressure solution of full \n\t\t(eq. gllide + exit phase), atm\n\tq_stag_total_full : numpy.ndarray\n\t\tstag. point total heat rate of full \n\t\t(eq. gllide + exit phase), W/cm2\n\theatload_full : numpy.ndarray\n\t\tstag. point heatload solution of full \n\t\t(eq. gllide + exit phase), J/cm2\n\tNPOS : int\n\t\tNPOS value from GRAM model output \n\t\tis the number of data points (altitude) in each atm. profile\n\tNMONTE : int\n\t\tNMONTE is the number of Monte Carlo atm profiles\n\t\tfrom GRAM model output\n\theightCol : int\n\t\tcolumn number of altitude values in Monte Carlo density file\n\tdensLowCol : int\n\t\tcolumn number of low density value in Monte Carlo density file\n\tdensAvgCol : int\n\t\tcolumn number of avg. density value in Monte Carlo density file\n\tdensHighCol : int\n\t\tcolumn number of high density value in Monte Carlo density file\n\tdensTotalCol : int\n\t\tcolumn number of total density value in Monte Carlo density file\n\theightInKmFlag : bool\n\t\tset to True if height values are in km\n\tnominalEFPA : float\n\t\tnominal entry-flight-path angle\n\tEFPA_1sigma_value : float\n\t\t1-sigma error for EFPA\n\tnominalLD : float\n\t\tnominal vehicle lift-to-drag ratio\n\tLD_1sigma_value : float\n\t\t1-sigma error for vehicle lift-to-drag ratio\n\tvehicleCopy : Vehicle.vehicle\n\t\tcopy of the original vehicle object\n\ttimeStep : float\n\t\tguidance cycle time, sec\n\tdt : float\n\t\tmax. solver timestep, sec\n\tmaxTimeSecs : float\n\t\tmaximum propogation time used by guidance algorithm, sec\n\n\n\t\n\t\t\n\n\t'

    def __init__(self, vehicleID, mass, beta, LD, A, alpha, RN, planetObj):
        """
                Initializes vehicle object with properties such as mass, 
                aerodynamics etc.

                Parameters
                ----------
                vehicleID : str
                        name of the vehicle
                mass : float
                        mass of the vehicle, kg
                beta : float
                        vehicle ballistic coefficient, kg/m2
                LD : float
                        vehicle lift-to-drag ratio
                A : float
                        vehicle reference aerodynamic area, m2
                alpha : float
                        vehicle angle-of-attack
                RN : float
                        vehicle nose-radius
                planetObj : planet.Planet
                        planet object associated with the vehicle
                """
        self.vehicleID = vehicleID
        self.mass = mass
        self.beta = beta
        self.A = A
        self.LD = LD
        self.alpha = alpha
        self.RN = RN
        self.planetObj = planetObj
        self.Abar = self.A / (self.mass / (self.planetObj.rho0 * self.planetObj.RP))
        self.mbar = self.mass / self.mass
        self.CD = self.mass / (self.beta * self.A)
        self.CL = self.LD * self.CD

    def setInitialState(self, h0_km, theta0_deg, phi0_deg, v0_kms, psi0_deg, gamma0_deg, drange0_km, heatLoad0):
        """
                Set initial vehicle state at atmospheric entry interface

                Parameters
                ----------
                h0_km : float
                        initial vehicle altitude at atmospheric interface / other 
                        start point, meters
                theta0_deg : float
                        initial vehicle longitude at atmospheric interface / other 
                        start point, degrees
                phi0_deg : float
                        initial vehicle latitude at atmospheric interface / other 
                        start point, degrees
                v0_kms : float
                        initial vehicle speed (planet-relative) at atmospheric
                    interface / other  start point, km/s
                psi0_deg : float
                        initial vehicle heading at atmospheric interface / other 
                        start point, degrees
                gamma0_deg : float
                        initial vehicle flight-path angle at atmospheric interface
                        / other start point, degrees
                drange0_km : float
                        initial vehicle downrange at atmospheric interface
                        / other start point, km
                heatLoad0 : float
                        initial vehicle heatload at atmospheric interface
                        / other start point, J/cm2

                """
        self.h0_km = h0_km
        self.theta0_deg = theta0_deg
        self.phi0_deg = phi0_deg
        self.v0_kms = v0_kms
        self.psi0_deg = psi0_deg
        self.gamma0_deg = gamma0_deg
        self.drange0_km = drange0_km
        self.heatLoad0 = heatLoad0
        self.h0_km_ref = copy.deepcopy(h0_km)
        self.theta0_deg_ref = copy.deepcopy(theta0_deg)
        self.phi0_deg_ref = copy.deepcopy(phi0_deg)
        self.v0_kms_ref = copy.deepcopy(v0_kms)
        self.psi0_deg_ref = copy.deepcopy(psi0_deg)
        self.gamma0_deg_ref = copy.deepcopy(gamma0_deg)
        self.drange0_km_ref = copy.deepcopy(drange0_km)
        self.heatLoad0_ref = copy.deepcopy(heatLoad0)

    def setSolverParams(self, tol):
        """
                Set the solver parameters.

                Parameters
                ----------
                tol : float
                        solver tolerance, currently both abstol and reltol
                        are set to this value
                """
        self.tol = tol

    def qStagConvective(self, r, v):
        """
                This function defines the convective stagnation-point 
                heating relationships. Edit the parameters in the
                source-code if you wish to modify these values.

                Sources : Sutton-Graves relationships, NASA Neptune Orbiter 
                with Probes Vision Report, Bienstock et al.

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance solution array of trajectory, m
                v : numpy.ndarray
                        planet-relative speed array of trajectory, m/s

                Returns
                ----------
                ans : numpy.ndarray
                        convective stagnation-point heating rate array, W/cm2
                """
        if self.planetObj.ID == 'VENUS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 1.896e-08 * (rho_vec[:] / self.RN) ** 0.5 * v[:] ** 3.0
            return ans
        if self.planetObj.ID == 'EARTH':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 1.7623e-08 * (rho_vec[:] / self.RN) ** 0.5 * v[:] ** 3.0
            return ans
        if self.planetObj.ID == 'MARS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 1.898e-08 * (rho_vec[:] / self.RN) ** 0.5 * v[:] ** 3.0
            return ans
        if self.planetObj.ID == 'TITAN':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 1.7407e-08 * (rho_vec[:] / self.RN) ** 0.5 * v[:] ** 3.0
            return ans
        if self.planetObj.ID == 'URANUS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 2.24008e-07 * rho_vec[:] ** 0.45213 * v[:] ** 2.6918 * np.sqrt(0.291 / self.RN)
            return ans
        if self.planetObj.ID == 'NEPTUNE':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 2.24008e-07 * rho_vec[:] ** 0.45213 * v[:] ** 2.6918 * np.sqrt(0.291 / self.RN)
            return ans
        print(' >>> ERR : Invalid planet identifier provided.')

    def qStagRadiative(self, r, v):
        """
                This function defines the radiative stagnation-point 
                heating relationships. Edit the parameters in the
                source-code if you wish to modify these values.

                Radiative heating is currently set to 0 for Mars 
                and Titan, though these may not be negligible
                under certain conditions.

                Sources : 
                        Craig and Lyne, 2005; 
                        Brandis and Johnston, 2014;
                        NASA Vision Neptune orbiter with probes, 
                        Contract No. NNH04CC41C

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance solution array of trajectory, m
                v : numpy.ndarray
                        planet-relative speed array of trajectory, m/s

                Returns
                ----------
                ans : numpy.ndarray
                        radiative stagnation-point heating rate array, W/cm2
                """
        if self.planetObj.ID == 'VENUS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            for i in range(0, len(r)):
                if v[i] < 8000.0:
                    ans[i] = 3.33e-34 * v[i] ** 10.0 * rho_vec[i] ** 1.2 * self.RN ** 0.49
                elif v[i] >= 8000.0 and v[i] < 10000.0:
                    ans[i] = 1.22e-16 * v[i] ** 5.5 * rho_vec[i] ** 1.2 * self.RN ** 0.49
                else:
                    ans[i] = 3.07e-48 * v[i] ** 13.4 * rho_vec[i] ** 1.2 * self.RN ** 0.49

            return ans
        if self.planetObj.ID == 'EARTH':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            C = 34160.0
            if self.RN <= 0.5:
                amax = 0.61
            else:
                if self.RN > 0.5 and self.RN < 2.0:
                    amax = 1.23
                else:
                    amax = 0.49
            for i in range(0, len(r)):
                a = np.min(3175000.0 * V ** (-1.8) * rho_vec[i] ** (-0.1575), amax)
                b = 1.261
                fV = -53.26 + 6555.0 / (1 + (16000.0 / V) ** 8.25)
                ans[i] = C * self.RN ** a * rho_vec[i] ** b * fV

            return ans
        if self.planetObj.ID == 'MARS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            return ans
        if self.planetObj.ID == 'TITAN':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            return ans
        if self.planetObj.ID == 'URANUS':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 0.008125812 * rho_vec[:] ** 0.49814 * (v[:] / 10000) ** 15.113 * (self.RN / 0.291)
            return ans
        if self.planetObj.ID == 'NEPTUNE':
            ans = np.zeros(len(r))
            rho_vec = self.planetObj.rhovectorized(r)
            ans[:] = 0.008125812 * rho_vec[:] ** 0.49814 * (v[:] / 10000) ** 15.113 * (self.RN / 0.291)
            return ans
        print(' >>> ERR : Invalid planet identifier provided.')

    def qStagTotal(self, r, v):
        """
                Computes the total heat rate which is the sum of the
                convective and radiative heating rates.
                
                Parameters
                ----------
                r : numpy.ndarray
                        radial distance solution array of trajectory, m
                v : numpy.ndarray
                        planet-relative speed array of trajectory, m/s

                Returns
                ----------
                ans : numpy.ndarray
                        total stagnation-point heating rate array, W/cm2
                """
        ans = np.zeros(len(r))
        qStagCon = self.qStagConvective(r, v)
        qStagRad = self.qStagRadiative(r, v)
        ans = qStagCon + qStagRad
        return ans

    def L(self, r, theta, phi, v):
        """
                Computes the vehicle aerodynamic lift, as a function of the
                vehicle location(r,theta, phi), and velocity. 

                Parameters
                ----------
                r : float
                        radial position value, scalar, m
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                v : float
                        planet-relative speed, m/s

                Returns
                ----------
                ans : float
                        aerodynamic lift force, N

                """
        ans = 0.5 * self.planetObj.rho(r, theta, phi) * v ** 2.0 * self.A * self.CL
        return ans

    def Lvectorized(self, r, theta, phi, v):
        """
                Vectorized version of the L() function

                Computesthe vehicle aerodynamic lift array
                over the provided trajectory array, as a function of the
                vehicle location array (r[:],theta[:], phi[:]), and velocity. 

                Parameters
                ----------
                r : numpy.ndarray
                        radial position array, m
                theta : numpy.ndarray
                        longitude array, radians
                phi : float
                        latitude array, radians
                v : float
                        planet-relative speed array, m/s

                Returns
                ----------
                ans : numpy.ndarray
                        aerodynamic lift force array, N

                """
        ans = np.zeros(len(r))
        rho_vec = self.planetObj.rhovectorized(r)
        ans[:] = 0.5 * rho_vec[:] * v[:] ** 2.0 * self.A * self.CL
        return ans

    def D(self, r, theta, phi, v):
        """
                Computes the vehicle aerodynamic drag, as a function of the
                vehicle location(r,theta, phi), and velocity. 

                Parameters
                ----------
                r : float
                        radial position value, scalar, m
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                v : float
                        planet-relative speed, m/s

                Returns
                ----------
                ans : float
                        aerodynamic drag force, N

                """
        ans = 0.5 * self.planetObj.rho(r, theta, phi) * v ** 2.0 * self.A * self.CD
        return ans

    def Dvectorized(self, r, theta, phi, v):
        """
                Vectorized version of the D() function

                Computesthe vehicle aerodynamic drag array
                over the provided trajectory array, as a function of the
                vehicle location array (r[:],theta[:], phi[:]), and velocity. 

                Parameters
                ----------
                r : numpy.ndarray
                        radial position array, m
                theta : numpy.ndarray
                        longitude array, radians
                phi : numpy.ndarray
                        latitude array, radians
                v : numpy.ndarray
                        planet-relative speed array, m/s

                Returns
                ----------
                ans : numpy.ndarray
                        aerodynamic drag force array, N

                """
        ans = np.zeros(len(r))
        rho_vec = self.planetObj.rhovectorized(r)
        ans[:] = 0.5 * rho_vec[:] * v[:] ** 2.0 * self.A * self.CD
        return ans

    def Lbar(self, rbar, theta, phi, vbar):
        """
                Computes the non-dimensional vehicle aerodynamic lift, 
                as a function of the vehicle location(r,theta, phi), 
                and velocity. 

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s

                Returns
                ----------
                ans : float
                        non-dimensional aerodynamic lift force

                """
        ans = 0.5 * self.planetObj.rhobar(rbar, theta, phi) * vbar ** 2.0 * self.Abar * self.CL
        return ans

    def Dbar(self, rbar, theta, phi, vbar):
        """
                Computes the non-dimensional vehicle aerodynamic drag, 
                as a function of the vehicle location(r,theta, phi), 
                and velocity. 

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s

                Returns
                ----------
                ans : float
                        non-dimensional aerodynamic drag force

                """
        ans = 0.5 * self.planetObj.rhobar(rbar, theta, phi) * vbar ** 2.0 * self.Abar * self.CD
        return ans

    def a_s(self, r, theta, phi, v, delta):
        """
                Function to return tangential acceleration term a_s;
                
                a_s is the tangential acceleration term along the direction of 
                the velocity vector.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                r : float
                        radial position value, scalar, m
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                v : float
                        planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        tangential acceleration term a_s

                """
        ans = 0.0 * np.cos(self.alpha) - self.D(r, theta, phi, v) / self.mass
        return ans

    def a_svectorized(self, r, theta, phi, v, delta):
        """
                Vectorized version of the a_s() function

                Parameters
                ----------
                r : numpy.ndarray
                        radial position array, m
                theta : numpy.ndarray
                        longitude array, radians
                phi : numpy.ndarray
                        latitude array, radians
                v : numpy.ndarray
                        planet-relative speed array, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : numpy.ndarray
                        tangential acceleration array, m/s2

                """
        ans = np.zeros(len(r))
        T = np.zeros(len(r))
        D_vec = self.Dvectorized(r, theta, phi, v)
        ans[:] = T[:] * np.cos(self.alpha) - D_vec[:] / self.mass
        return ans

    def a_n(self, r, theta, phi, v, delta):
        """
                Function to return normal acceleration term a_n;
                
                a_n is the normal acceleration term along perpendicular 
                to the velocity vector, in the plane of the trajectory.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                r : float
                        radial position value, scalar, m
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                v : float
                        planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        normal acceleration term a_n

                """
        ans = (self.L(r, theta, phi, v) + 0.0 * np.sin(self.alpha)) * np.cos(delta) / self.mass
        return ans

    def a_nvectorized(self, r, theta, phi, v, delta):
        """
                Vectorized version of the a_n() function

                Parameters
                ----------
                r : numpy.ndarray
                        radial position array, m
                theta : numpy.ndarray
                        longitude array, radians
                phi : numpy.ndarray
                        latitude array, radians
                v : numpy.ndarray
                        planet-relative speed array, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : numpy.ndarray
                        normal acceleration array, m/s2

                """
        ans = np.zeros(len(r))
        T = np.zeros(len(r))
        L_vec = self.Lvectorized(r, theta, phi, v)
        ans[:] = (L_vec[:] + T[:] * np.sin(self.alpha)) * np.cos(delta) / self.mass
        return ans

    def a_w(self, r, theta, phi, v, delta):
        """
                Function to return binormal acceleration term a_w;
                
                a_n is the binormal acceleration term along perpendicular 
                to the velocity vector, perpendicular to 
                the plane of the trajectory.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                r : float
                        radial position value, scalar, m
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                v : float
                        planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        binormal acceleration term a_n

                """
        ans = (self.L(r, theta, phi, v) + 0.0 * np.sin(self.alpha)) * np.sin(delta) / self.mass
        return ans

    def a_wvectorized(self, r, theta, phi, v, delta):
        """
                Vectorized version of the a_w() function

                Parameters
                ----------
                r : numpy.ndarray
                        radial position array, m
                theta : numpy.ndarray
                        longitude array, radians
                phi : numpy.ndarray
                        latitude array, radians
                v : numpy.ndarray
                        planet-relative speed array, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : numpy.ndarray
                        binormal acceleration array, m/s2

                """
        ans = np.zeros(len(r))
        T = np.zeros(len(r))
        L_vec = self.Lvectorized(r, theta, phi, v)
        ans[:] = (L_vec[:] + T[:] * np.sin(self.alpha)) * np.sin(delta) / self.mass
        return ans

    def a_sbar(self, rbar, theta, phi, vbar, delta):
        """
                Function to return non-dimensional 
                tangential acceleration term a_sbar;
                
                a_sbar is the tangential acceleration term along 
                the direction of the velocity vector.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        non-dimensional tangential acceleration term a_sbar

                """
        ans = (0.0 * np.cos(self.alpha) - self.Dbar(rbar, theta, phi, vbar)) / self.mbar
        return ans

    def a_nbar(self, rbar, theta, phi, vbar, delta):
        """
                Function to return non-dimensional 
                normall acceleration term a_nbar;
                
                a_nbar is the tangential acceleration term along 
                the direction of the velocity vector.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        non-dimensional tangential acceleration term a_nbar

                """
        ans = (self.Lbar(rbar, theta, phi, vbar) + 0.0 * np.sin(self.alpha)) * np.cos(delta) / self.mbar
        return ans

    def a_wbar(self, rbar, theta, phi, vbar, delta):
        """
                Function to return non-dimensional 
                normal acceleration term a_wbar;
                
                a_wbar is the tangential acceleration term along 
                the direction of the velocity vector.

                Current formulation does not include thrust, can be added here 
                later in place of 0.0

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                theta : float
                        longitude, radians
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                delta : float
                        bank angle, rad

                Returns
                ----------
                ans : float
                        non-dimensional tangential acceleration term a_wbar

                """
        ans = (self.Lbar(rbar, theta, phi, vbar) + 0.0 * np.sin(self.alpha)) * np.sin(delta) / self.mbar
        return ans

    def cfvbar(self, rbar, phi, vbar, psi, gamma):
        """
                Function to return non dimensional centrifugal 
                acceleration term cfvbar
                
                cfvbar is the non dimensional centrifugal acceleration 
                term cfvbar in the EOM

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, rad
                gamma : float
                        flight-path angle, rad

                Returns
                ----------
                ans : float
                        non dimensional centrifugal acceleration cfvbar

                """
        ans = self.planetObj.OMEGAbar ** 2.0 * rbar * np.cos(phi) * (np.sin(gamma) * np.cos(phi) - np.cos(gamma) * np.sin(phi) * np.sin(psi))
        return ans

    def cfpsibar(self, rbar, phi, vbar, psi, gamma):
        """
                Function to return non dimensional centrifugal 
                acceleration term cfpsibar
                
                cfpsibar is the non dimensional centrifugal acceleration 
                term  in the EOM

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, rad
                gamma : float
                        flight-path angle, rad

                Returns
                ----------
                ans : float
                        non dimensional centrifugal acceleration cfpsibar

                """
        ans = -1.0 * self.planetObj.OMEGAbar ** 2.0 * rbar / (vbar * np.cos(gamma)) * np.sin(phi) * np.cos(phi) * np.cos(psi)
        return ans

    def cfgammabar(self, rbar, phi, vbar, psi, gamma):
        """
                Function to return non dimensional centrifugal 
                acceleration term cfgammabar
                
                cfgammabar is the non dimensional centrifugal acceleration 
                term  in the EOM

                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, rad
                gamma : float
                        flight-path angle, rad

                Returns
                ----------
                ans : float
                        non dimensional centrifugal acceleration cfpsibar

                """
        ans = self.planetObj.OMEGAbar ** 2.0 * rbar / vbar * np.cos(phi) * (np.cos(gamma) * np.cos(phi) + np.sin(gamma) * np.sin(phi) * np.sin(psi))
        return ans

    def copsibar(self, rbar, phi, vbar, psi, gamma):
        """
                Function to return non dimensional Coriolis 
                acceleration term copsibar
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, rad
                gamma : float
                        flight-path angle, rad

                Returns
                ----------
                ans : float
                        non dimensional Coriolis acceleration copsibar

                """
        ans = 2.0 * self.planetObj.OMEGAbar * (np.tan(gamma) * np.cos(phi) * np.sin(psi) - np.sin(phi))
        return ans

    def cogammabar(self, rbar, phi, vbar, psi, gamma):
        """
                Function to return non dimensional Coriolis 
                acceleration term cogammabar
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                vbar : float
                        non-dimensional planet-relative speed, m/s
                psi : float
                        heading angle, rad
                gamma : float
                        flight-path angle, rad

                Returns
                ----------
                ans : float
                        non dimensional Coriolis acceleration cogammabar

                """
        ans = 2.0 * self.planetObj.OMEGAbar * np.cos(phi) * np.cos(psi)
        return ans

    def grbar(self, rbar, phi):
        """
                Returns the non-dimensional gravity radial acceleration term grbar.
                
                grbar is the non dimensional gravity  
                radial acceleration term grbar in the EOM
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                
                Returns
                ----------
                ans : float
                        non-dimensional radial acceleration term grbar

                """
        term1 = -1.0 / rbar ** 2.0
        term2 = 1.5 * self.planetObj.J2 / rbar ** 4.0 * (3.0 * np.sin(phi) * np.sin(phi) - 1.0)
        term3 = 2.0 * self.planetObj.J3 / rbar ** 5.0 * (5.0 * np.sin(phi) ** 3.0 - 3.0 * np.sin(phi))
        ans = term1 + term2 + term3
        return ans

    def gthetabar(self, rbar, phi):
        """
                Returns the non-dimensional gravity longitudinal acceleration term.
                
                gthetabar is the non dimensional longitudinal
                gravity  acceleration term grbar in the EOM
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                
                Returns
                ----------
                ans : float
                        non-dimensional longitudinal gravity 
                        acceleration term gthetabar

                """
        return 0.0

    def gphibar(self, rbar, phi):
        """
                Returns the non-dimensional gravity 
                latitudinal acceleration term gphibar.
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                
                Returns
                ----------
                ans : float
                        non-dimensional gravity 
                        latitudinal acceleration term gphibar

                """
        term1 = -3.0 * self.planetObj.J2 / rbar ** 4.0 * np.sin(phi) * np.cos(phi)
        term2 = 1.5 * self.planetObj.J3 / rbar ** 5.0 * np.cos(phi) * (1.0 - 5.0 * np.sin(phi) * np.sin(phi))
        ans = term1 + term2
        return ans

    def gnbar(self, rbar, phi, gamma, psi):
        """
                Returns the non-dimensional gravity normal acceleration term gnbar.
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                gamma : float
                        flight-path angle, rad
                psi : float
                        heading angle, rad
                
                Returns
                ----------
                ans : float
                        non-dimensional gravity normal acceleration term gnbar

                """
        term1 = np.cos(gamma) * self.grbar(rbar, phi)
        term2 = -1.0 * np.sin(gamma) * np.cos(psi) * self.gthetabar(rbar, phi)
        term3 = -1.0 * np.sin(gamma) * np.sin(psi) * self.gphibar(rbar, phi)
        ans = term1 + term2 + term3
        return ans

    def gsbar(self, rbar, phi, gamma, psi):
        """
                Returns the non-dimensional gravity tangential
                acceleration term gsbar.
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                gamma : float
                        flight-path angle, rad
                psi : float
                        heading angle, rad
                
                Returns
                ----------
                ans : float
                        non-dimensional gravity tangential acceleration term gsbar

                """
        term1 = np.sin(gamma) * self.grbar(rbar, phi)
        term2 = np.cos(gamma) * np.cos(psi) * self.gthetabar(rbar, phi)
        term3 = np.cos(gamma) * np.sin(psi) * self.gphibar(rbar, phi)
        ans = term1 + term2 + term3
        return ans

    def gwbar(self, rbar, phi, gamma, psi):
        """
                Returns the non-dimensional gravity binormal
                acceleration term gwbar.
                
                Parameters
                ----------
                rbar : float
                        non-dimensional radial position
                phi : float
                        latitude, radians
                gamma : float
                        flight-path angle, rad
                psi : float
                        heading angle, rad
                
                Returns
                ----------
                ans : float
                        non-dimensional gravity binormal acceleration term gwbar

                """
        term1 = -1.0 * np.sin(psi) * self.gthetabar(rbar, phi)
        term2 = np.cos(psi) * self.gphibar(rbar, phi)
        ans = term1 + term2
        return ans

    def EOM(self, y, t, delta):
        """
                Define the EoMs to propogate the 3DoF trajectory inside the 
                atmosphere of a an oblate rotating planet.

                Reference 1: Vinh, Chapter 3.
                Reference 2: Lescynzki, MS Thesis, NPS.

                Parameters
                ----------
                y : numpy.ndarray
                        trajectory state vector
                t : numpy.ndarray
                        trajectory time vector
                delta : float
                        bank angle, rad
                
                Returns
                ----------
                ans : dydt
                        derivate vector of state, process equations

                """
        rbar, theta, phi, vbar, psi, gamma, drangebar = y
        dydt = [
         vbar * np.sin(gamma),
         vbar * np.cos(gamma) * np.cos(psi) / (rbar * np.cos(phi)),
         vbar * np.cos(gamma) * np.sin(psi) / rbar,
         self.a_sbar(rbar, theta, phi, vbar, delta) + self.gsbar(rbar, phi, gamma, psi) + self.cfvbar(rbar, phi, vbar, psi, gamma),
         (self.a_wbar(rbar, theta, phi, vbar, delta) + self.gwbar(rbar, phi, gamma, psi)) / (vbar * np.cos(gamma)) - 1.0 * vbar / rbar * np.cos(gamma) * np.cos(psi) * np.tan(phi) + self.cfpsibar(rbar, phi, vbar, psi, gamma) + self.copsibar(rbar, phi, vbar, psi, gamma),
         (self.a_nbar(rbar, theta, phi, vbar, delta) + self.gnbar(rbar, phi, gamma, psi)) / vbar + vbar / rbar * np.cos(gamma) + self.cfgammabar(rbar, phi, vbar, psi, gamma) + self.cogammabar(rbar, phi, vbar, psi, gamma),
         vbar * np.cos(gamma)]
        return dydt

    def solveTrajectory(self, rbar0, theta0, phi0, vbar0, psi0, gamma0, drangebar0, t_sec, dt, delta):
        """
                Function to propogate a single atmospheric entry trajectory 
                given entry interface / other initial conditions and
                bank angle delta.

                Reference 1: Vinh, Chapter 3.
                Reference 2: Lescynzki, MS Thesis, NPS.

                Parameters
                ----------
                rbar0 : float
                        non-dimensional radial distance initial condition
                theta0 : float
                        longitude initial condition, rad
                phi0 : float
                        latatitude initial condition, rad
                vbar0 : float
                        non-dimensional planet-relative speed initial condition
                psi0 : float
                        heading angle initial condition, rad
                gamma0 : float
                        entry flight-path angle initial condition, rad
                drangebar0 : float
                        non-dimensional downrange initial condition
                t_sec : float
                        time in seconds for which propogation is done
                dt : float
                        max. time step size in seconds
                delta : float
                        bank angle command, rad

                Returns
                ----------
                tbar : numpy.ndarray
                        nondimensional time at which solution is computed
                rbar : numpy.ndarray
                        nondimensional radial distance solution
                theta : numpy.ndarray
                        longitude solution, rad
                phi : numpy.ndarray
                        latitude array, rad
                vbar : numpy.ndarray
                        nondimensional velocity solution
                psi : numpy.ndarray, rad
                        heading angle solution, rad
                gamma : numpy.ndarray
                        flight-path angle, rad
                drangebar : numpy.ndarray
                        downrange solution, meters
                """
        xbar_0 = [
         rbar0, theta0, phi0, vbar0,
         psi0, gamma0, drangebar0]
        tbar = np.arange(0, (t_sec + dt) / self.planetObj.tau, dt / self.planetObj.tau)
        xbar = odeint((self.EOM), xbar_0, tbar, rtol=(self.tol),
          atol=(self.tol),
          args=(delta,))
        rbar = xbar[:, 0]
        theta = xbar[:, 1]
        phi = xbar[:, 2]
        vbar = xbar[:, 3]
        psi = xbar[:, 4]
        gamma = xbar[:, 5]
        drangebar = xbar[:, 6]
        return (
         tbar, rbar, theta, phi, vbar, psi, gamma, drangebar)

    def convertToPlotUnits(self, t, r, v, phi, psi, theta, gamma, drange):
        """
                Convert state vector components to units appropriate 
                for evolution plots.

                Parameters
                ----------
                t : numpy.ndarray
                        time array, sec
                r : numpy.ndarray
                        radial distance array, m
                v : numpy.ndarray
                        speed array, m
                phi : numpy.ndarray
                        latitude array, rad
                psi : numpy.ndarray
                        heading angle array, rad
                theta : numpy.ndarray
                        longitude array, rad
                gamma : numpy.ndarray
                        flight path angle array, rad
                drange : numpy.ndarray
                        downrange array, meters

                Returns
                ----------
                t_min : numpy.ndarray
                        time array, minutes
                h_km : numpy.ndarray
                        altitude array, km
                v_kms : numpy.ndarray
                        speed array, km/s
                phi_deg : numpy.ndarray
                        latitude array, deg
                psi_deg : numpy.ndarray
                        heading angle array, deg
                theta_deg : numpy.ndarray
                        longitude array, deg
                gamma_deg : numpy.ndarray
                        flight path angle array, deg
                drange_km : numpy.ndarray
                        downrange array, km
                """
        t_min = t / 60.0
        h_km = (r - self.planetObj.RP) * 0.001
        v_kms = v * 0.001
        phi_deg = phi * 180 / np.pi
        psi_deg = psi * 180 / np.pi
        theta_deg = theta * 180 / np.pi
        gamma_deg = gamma * 180 / np.pi
        drange_km = drange * 0.001
        return (
         t_min, h_km, v_kms, phi_deg, psi_deg, theta_deg,
         gamma_deg, drange_km)

    def convertToKPa(self, pres):
        """
                Convert a pressure solution array from Pa to kPa. 

                Parameters
                ----------
                pres : numpy.ndarray
                        pressure (static/dynamic/total), Pascal (Pa)
                
                Returns
                ----------
                ans : numpy.ndarray
                        pressure (static/dynamic/total), kiloPascal (kPa)

                """
        return pres / 1000.0

    def convertToPerCm2(self, heatrate):
        """
                Convert a heat rate from W/m2 to W/cm2. 

                Parameters
                ----------
                heatrate : numpy.ndarray
                        stagnation-point heat rate, W/m2
                
                Returns
                ----------
                ans : numpy.ndarray
                        stagnation-point heat rate, W/cm2

                """
        return heatrate / 10000.0

    def classifyTrajectory(self, r):
        """
                This function checks the trajectory for "events" which are 
                used to truncate the trajectory
                
                A "skip out event" is said to occur as when the vehicle 
                altitude did not hit the surface and exceeds the prescribed 
                skip out altitude.
                
                A "time out event" is said to occur if the vehicle did not 
                exceed the skip out altitude, and did not reach the trap in 
                altitude.
                
                A "trap in" event is said to occur when the vehicle altitude 
                falls below the prescribed trap in altitude.
                
                This function checks for these events and returns the array 
                index of the "event" location and an exitflag
                
                exitflag to indicate if an event was detected or not.
                exitflag = 1.0 indicates "skip out event" has occured.
                exitflag = 0.0 indicates no "event" was detected in the trajectory, 
                consider increasing simulation time.
                exitflag = -1.0 indicates "trap in event" has occured.

                Parameters
                ----------
                r : numpy.ndarray
                        dimensional radial distance solution, meters

                Returns
                ----------
                index : int
                        array index of the event location if one was detected, 
                        terminal index otherwise
                exitflag : int
                        flag to indicate and classify event occurence or lack of it                     

                
                """
        h = self.planetObj.computeH(r)
        h_max = max(h)
        h_min = min(h)
        if h_min >= 0 and h_max > self.planetObj.h_skip:
            index = np.argmax(h > self.planetObj.h_skip)
            exitflag = 1.0
        else:
            if h_min >= self.planetObj.h_trap and h_max < self.planetObj.h_skip:
                index = len(h)
                exitflag = 0.0
            else:
                if h_min <= self.planetObj.h_trap:
                    index = np.argmax(h < self.planetObj.h_trap)
                    exitflag = -1.0
                else:
                    index = len(h)
                    exitflag = 0.0
        return (
         index, exitflag)

    def truncateTrajectory(self, t, r, theta, phi, v, psi, gamma, drange, index):
        """
                This function truncates the full trajectory returned by the solver 
                to the first event location.
                
                The full trajectory returned by the solver could have skipped out 
                exceeding the skip out altitude, or could have descended below the 
                trap in altitude or even below the surface.
                
                This function helps ensure that we truncate the trajectory to what 
                we actually need, i.e. till a skip out / trap in event.

                Parameters
                ----------
                t : numpy.ndarray
                        time array, sec
                r : numpy.ndarray
                        radial distance array, m
                v : numpy.ndarray
                        speed array, m
                phi : numpy.ndarray
                        latitude array, rad
                psi : numpy.ndarray
                        heading angle array, rad
                theta : numpy.ndarray
                        longitude array, rad
                gamma : numpy.ndarray
                        flight path angle array, rad
                drange : numpy.ndarray
                        downrange array, meters
                index : int
                        array index of detected event location / 
                        max index if no event detected

                Returns
                ----------
                t : numpy.ndarray
                        truncated time array, sec
                r : numpy.ndarray
                        truncated radial distance array, m
                v : numpy.ndarray
                        truncated speed array, m
                phi : numpy.ndarray
                        truncated latitude array, rad
                psi : numpy.ndarray
                        truncated heading angle array, rad
                theta : numpy.ndarray
                        truncated longitude array, rad
                gamma : numpy.ndarray
                        truncated flight path angle array, rad
                drange : numpy.ndarray
                        truncated downrange array, meters
                
                """
        return (
         t[0:index], r[0:index], theta[0:index], phi[0:index],
         v[0:index], psi[0:index], gamma[0:index], drange[0:index])

    def computeAccelerationLoad(self, tc, rc, thetac, phic, vc, index, delta):
        """
                This function computes the acceleration load (Earth G's) over 
                the entire trajectory from trajectory data returned by the solver.

                Parameters
                ----------
                tc : numpy.ndarray
                        truncated time array, sec
                rc : numpy.ndarray
                        truncated radial distance array, m
                thetac : numpy.ndarray
                        truncated longitude array, rad
                phic : numpy.ndarray
                        trucnated latitude array, rad
                vc : numpy.ndarray
                        truncated speed array, m
                index : int
                        array index of detected event location / 
                        max index if no event detected
                delta : float
                        bank angle, rad

                Returns
                ----------
                acc_net_g : numpy.ndarray
                        acceleration load (Earth G's) over the entire trajectory
                """
        acc_s = np.zeros(index)
        acc_n = np.zeros(index)
        acc_w = np.zeros(index)
        acc_s = self.a_svectorized(rc, thetac, phic, vc, delta)
        acc_n = self.a_nvectorized(rc, thetac, phic, vc, delta)
        acc_w = self.a_wvectorized(rc, thetac, phic, vc, delta)
        acc_net = np.zeros(index)
        acc_net[:] = np.sqrt(acc_s[:] ** 2.0 + acc_n[:] ** 2.0 + acc_w[:] * 2.0)
        acc_net_g = acc_net / self.planetObj.EARTHG
        return acc_net_g

    def computeAccelerationDrag(self, tc, rc, thetac, phic, vc, index, delta):
        """
                This function computes the drag acceleration load (Earth G's) over 
                the entire trajectory from trajectory data returned by the solver.

                Parameters
                ----------
                tc : numpy.ndarray
                        truncated time array, sec
                rc : numpy.ndarray
                        truncated radial distance array, m
                thetac : numpy.ndarray
                        truncated longitude array, rad
                phic : numpy.ndarray
                        trucnated latitude array, rad
                vc : numpy.ndarray
                        truncated speed array, m
                index : int
                        array index of detected event location / 
                        max index if no event detected
                delta : float
                        bank angle, rad

                Returns
                ----------
                acc_drag_g : numpy.ndarray
                        drag acceleration load (Earth G's) over the entire trajectory
                """
        acc_s = np.zeros(index)
        acc_n = np.zeros(index)
        acc_w = np.zeros(index)
        acc_s = self.a_svectorized(rc, thetac, phic, vc, delta)
        acc_n = self.a_nvectorized(rc, thetac, phic, vc, delta)
        acc_w = self.a_wvectorized(rc, thetac, phic, vc, delta)
        acc_drag = np.zeros(index)
        acc_drag[:] = np.sqrt(acc_s[:] ** 2.0 + 0.0 * acc_n[:] ** 2.0 + 0.0 * acc_w[:] * 2.0)
        acc_drag_g = acc_drag / self.planetObj.EARTHG
        return acc_drag_g

    def computeDynPres(self, r, v):
        """
                This function computes the dynamic pressure over the 
                entire trajectory.

                Parameters
                ----------
                r : numpy.ndarray
                        radial distance array, m
                v : numpy.ndarray
                        speed array, m/s
                
                Returns
                ----------
                ans : numpy.ndarray
                        dynamic pressure, Pa
                
                """
        ans = np.zeros(len(r))
        rho_vec = self.planetObj.rhovectorized(r)
        ans[:] = 0.5 * rho_vec[:] * v[:] ** 2
        return ans

    def computeStagPres(self, rc, vc):
        """
                This function computes the stag. pressure over the 
                entire trajectory.

                Parameters
                ----------
                rc : numpy.ndarray
                        radial distance array, m
                vc : numpy.ndarray
                        speed array, m/s
                
                Returns
                ----------
                ans : numpy.ndarray
                        stag. pressure, Pa
                
                """
        stat_pres = self.planetObj.pressurevectorized(rc)
        stag_pres = np.zeros(len(rc))
        dyn_pres = self.computeDynPres(rc, vc)
        stag_pres = stat_pres + dyn_pres
        return stag_pres

    def computeMach(self, rc, vc):
        """
                This function computes the Mach. no over the 
                entire trajectory.

                Parameters
                ----------
                rc : numpy.ndarray
                        radial distance array, m
                vc : numpy.ndarray
                        speed array, m/s
                
                Returns
                ----------
                ans : numpy.ndarray
                        Mach no.
                
                """
        stat_pres = self.planetObj.pressurevectorized(rc)
        stat_temp = self.planetObj.temperaturevectorized(rc)
        mach = np.zeros(len(rc))
        sonic_spd = self.planetObj.sonicvectorized(rc)
        mach[:] = vc[:] / sonic_spd[:]
        return mach

    def computeStagTemp(self, rc, vc):
        """
                This function computes the stag. temperature over the 
                entire trajectory.

                Parameters
                ----------
                rc : numpy.ndarray
                        radial distance array, m
                vc : numpy.ndarray
                        speed array, m/s
                
                Returns
                ----------
                ans : numpy.ndarray
                        stag. temperature, K
                
                """
        stat_temp = self.planetObj.temperaturevectorized(rc)
        mach = np.zeros(len(rc))
        sonic_spd = self.planetObj.sonicvectorized(rc)
        mach[:] = vc[:] / sonic_spd[:]
        stag_temp = np.zeros(len(rc))
        stag_temp[:] = stat_temp[:] * (1 + 0.5 * (self.CPCV - 1) * mach[:] ** 2.0)
        return stag_temp

    def computeHeatingForMultipleRN(self, tc, rc, vc, rn_array):
        """
                This function computes the max. stag. pont heating rate 
                and heat load for an array of nose radii.

                Parameters
                ----------
                tc : numpy.ndarray
                        truncated time array, sec
                rc : numpy.ndarray
                        truncated radial distance array, m
                vc : numpy.ndarray
                        speed array, m/s
                rn_array : numpy.ndarray
                        nose radius array, m
                
                Returns
                ----------
                q_stag_max : numpy.ndarray
                        max. heat rate, W/cm2
                heatload : numpy.ndarray
                        max. heatload, J/cm2
                
                """
        temp_var = self.RN
        q_stag_max = np.zeros(len(rn_array))
        heatload = np.zeros(len(rn_array))
        count = 0
        for RN in rn_array:
            self.RN = RN
            q_stag = self.qStagTotal(rc, vc)
            q_stag_max[count] = max(q_stag)
            heatload[count] = cumtrapz(q_stag, tc, initial=0)[(-1)]
            count = count + 1

        self.RN = temp_var
        return (
         q_stag_max, heatload)

    def computeEnergy(self, rc, vc):
        """
                This function computes the total specific mechanical energy 
                of the vehicle over the entire trajectory.

                Parameters
                ----------
                rc : numpy.ndarray
                        radial distance array, m
                vc : numpy.ndarray
                        speed array, m/s
                
                Returns
                ----------
                ans : numpy.ndarray
                        specific energy, J/kg
                
                """
        energy = np.zeros(len(rc))
        energy[:] = -1.0 * self.planetObj.GM / rc[:] + 0.5 * vc[:] ** 2.0
        return energy

    def computeEnergyScalar(self, r, v):
        """
                This function computes the total specific mechanical energy 
                of the vehicle at an instance.

                Parameters
                ----------
                r : float
                        radial distance, m
                v : float
                        speed array, m/s
                
                Returns
                ----------
                ans : float
                        specific energy, J/kg
                
                """
        energy = -1.0 * self.planetObj.GM / r + 0.5 * v ** 2.0
        return energy

    def computeSemiMajorAxisScalar(self, E):
        """
                This function computes the semi-major axis of the orbit given 
                its total specific mechanical energy.
                
                Parameters
                ----------
                E : float
                        specific energy, J/kg
                
                Returns
                ----------
                ans : float
                        semi major axis, km
                """
        a = -1.0 * self.planetObj.GM / (2 * E)
        return a

    def computeAngMomScalar(self, terminal_r, terminal_v, terminal_g):
        """
                This function computes the specific angular momentum (orbital) 
                of the vehicle at an instance given its current radial distance,
                speed, and flight-path angle.

                Parameters
                ----------
                terminal_r : float
                        radial distance, meters
                terminal_v : float
                        speed, meters/sec
                terminal_g : float
                        flight-path angle, rad
                
                
                Returns
                ----------
                ans : float
                        specific angular momentum, SI units
                """
        angMom = terminal_r * terminal_v * np.cos(terminal_g)
        return angMom

    def computeEccScalar(self, h, E):
        """
                This function computes the eccentricity of the orbit given its 
                specific angular momentum, and total specific mechanical energy.
                
                Parameters
                ----------
                h : float
                        specific angular momentum, SI units
                E : float
                        specifice energy, J/kg
                
                Returns
                ----------
                ans : float
                        eccentricity value
                
                """
        ecc = np.sqrt(1.0 + 2 * E * h ** 2.0 / self.planetObj.GM ** 2.0)
        return ecc

    def propogateEntry(self, t_sec, dt, delta_deg):
        """
                Propogates the vehicle state for a specified time using 
                initial conditions, vehicle properties, and 
                atmospheric profile data.
                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                delta_deg : float
                        bank angle command, deg
                
                """
        h0 = self.h0_km * 1000.0
        theta0 = self.theta0_deg * np.pi / 180.0
        phi0 = self.phi0_deg * np.pi / 180.0
        v0 = self.v0_kms * 1000.0
        psi0 = self.psi0_deg * np.pi / 180.0
        gamma0 = self.gamma0_deg * np.pi / 180.0
        drange0 = self.drange0_km * 1000.0
        delta = delta_deg * np.pi / 180.0
        r0 = self.planetObj.computeR(h0)
        rbar0, theta0, phi0, vbar0, psi0, gamma0, drangebar0 = self.planetObj.nonDimState(r0, theta0, phi0, v0, psi0, gamma0, drange0)
        tbar, rbar, theta, phi, vbar, psi, gamma, drangebar = self.solveTrajectory(rbar0, theta0, phi0, vbar0, psi0, gamma0, drangebar0, t_sec, dt, delta)
        t, r, theta, phi, v, psi, gamma, drange = self.planetObj.dimensionalize(tbar, rbar, theta, phi, vbar, psi, gamma, drangebar)
        t_min, h_km, v_kms, phi_deg, psi_deg, theta_deg, gamma_deg, drange_km = self.convertToPlotUnits(t, r, v, phi, psi, theta, gamma, drange)
        self.index, self.exitflag = self.classifyTrajectory(r)
        self.tc, self.rc, self.thetac, self.phic, self.vc, self.psic, self.gammac, self.drangec = self.truncateTrajectory(t, r, theta, phi, v, psi, gamma, drange, self.index)
        self.t_minc, self.h_kmc, self.v_kmsc, self.phi_degc, self.psi_degc, self.theta_degc, self.gamma_degc, self.drange_kmc = self.truncateTrajectory(t_min, h_km, v_kms, phi_deg, psi_deg, theta_deg, gamma_deg, drange_km, self.index)
        self.acc_net_g = self.computeAccelerationLoad(self.tc, self.rc, self.thetac, self.phic, self.vc, self.index, delta)
        self.acc_drag_g = self.computeAccelerationDrag(self.tc, self.rc, self.thetac, self.phic, self.vc, self.index, delta)
        self.dyn_pres_atm = self.computeDynPres(self.rc, self.vc) / 101325.0
        self.stag_pres_atm = self.computeStagPres(self.rc, self.vc) / 101325.0
        self.q_stag_con = self.qStagConvective(self.rc, self.vc)
        self.q_stag_rad = self.qStagRadiative(self.rc, self.vc)
        self.q_stag_total = self.q_stag_con + self.q_stag_rad
        self.heatload = cumtrapz((self.q_stag_total), (self.tc), initial=(self.heatLoad0))

    def dummyVehicle(self, density_mes_int):
        """
                Create a copy of the vehicle object which uses a 
                measured density profile for propogation.

                Parameters
                -----------
                density_mes_int : scipy.interpolate.interpolate.interp1d
                        density interpolation function

                Returns
                -----------
                vehicleCopy : vehicle object
                        dummy vehicle object

                """
        planetCopy = copy.deepcopy(self.planetObj)
        planetCopy.density_int = density_mes_int
        vehicleCopy = copy.deepcopy(self)
        vehicleCopy.planetObj = planetCopy
        return vehicleCopy

    def propogateEntry2(self, h0_km, theta0_deg, phi0_deg, v0_kms, gamma0_deg, psi0_deg, drange0_km, heatLoad0, t_sec, dt, delta_deg, density_mes_int):
        """
                Utility propogator routine for prediction of atmospheric exit
                conditions which is then supplied to the apoapis prediction 
                module.

                Propogates the vehicle state for using the "measured 
                atmospheric profile" during the descending leg.
                
                Parameters
                ----------
                h0_km : float
                        current altitude, km
                theta0_deg : float
                        current longitude, deg
                phi0_deg : float
                        current latitude, deg
                v0_kms : float
                        current speed, km/s
                gamma0_deg : float
                        current FPA, deg
                psi0_deg : float
                        current heading angle, deg
                drange0_km : float
                        current downrange, km
                heatLoad0 : float
                        current heatload, J/cm2
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                delta_deg : float
                        bank angle command, deg

                Returns
                ----------
                t_minc : numpy.ndarray
                        time solution array, min 
                h_kmc : numpy.ndarray
                        altitude solution array, km
                v_kmsc : numpy.ndarray
                        speed solution array, km/s
                phi_degc : numpy.ndarray
                        latitude solution array, deg
                psi_degc : numpy.ndarray
                        heading angle solution array, deg
                theta_degc : numpy.ndarray
                        longitude solution array, deg
                gamma_degc : numpy.ndarray
                        FPA solution array, deg
                drange_kmc : numpy.ndarray
                        downrange solution array, km
                exitflag : int
                        exitflag
                acc_net_g : numpy.ndarray
                        acceleration solution array, Earth g
                dyn_pres_atm : numpy.ndarray
                        dynamic pressure solution array, atm
            stag_pres_atm : numpy.ndarray
                stagnation pressure array, atm
            q_stag_total : numpy.ndarray
                stagnation point heat rate array
            heatload : numpy.ndarray
                stagnation point heat load
            acc_drag_g : numpy.ndarray
                acceleration due to drag, Earth g
                
                """
        planetCopy = copy.deepcopy(self.planetObj)
        planetCopy.density_int = density_mes_int
        vehicleCopy = copy.deepcopy(self)
        vehicleCopy.planetObj = planetCopy
        h0 = h0_km * 1000.0
        theta0 = theta0_deg * np.pi / 180.0
        phi0 = phi0_deg * np.pi / 180.0
        v0 = v0_kms * 1000.0
        psi0 = psi0_deg * np.pi / 180.0
        gamma0 = gamma0_deg * np.pi / 180.0
        drange0 = drange0_km * 1000.0
        delta = delta_deg * np.pi / 180.0
        r0 = vehicleCopy.planetObj.computeR(h0)
        rbar0, theta0, phi0, vbar0, psi0, gamma0, drangebar0 = vehicleCopy.planetObj.nonDimState(r0, theta0, phi0, v0, psi0, gamma0, drange0)
        tbar, rbar, theta, phi, vbar, psi, gamma, drangebar = vehicleCopy.solveTrajectory(rbar0, theta0, phi0, vbar0, psi0, gamma0, drangebar0, t_sec, dt, delta)
        t, r, theta, phi, v, psi, gamma, drange = vehicleCopy.planetObj.dimensionalize(tbar, rbar, theta, phi, vbar, psi, gamma, drangebar)
        t_min, h_km, v_kms, phi_deg, psi_deg, theta_deg, gamma_deg, drange_km = vehicleCopy.convertToPlotUnits(t, r, v, phi, psi, theta, gamma, drange)
        index, exitflag = vehicleCopy.classifyTrajectory(r)
        tc, rc, thetac, phic, vc, psic, gammac, drangec = vehicleCopy.truncateTrajectory(t, r, theta, phi, v, psi, gamma, drange, index)
        t_minc, h_kmc, v_kmsc, phi_degc, psi_degc, theta_degc, gamma_degc, drange_kmc = vehicleCopy.truncateTrajectory(t_min, h_km, v_kms, phi_deg, psi_deg, theta_deg, gamma_deg, drange_km, index)
        acc_net_g = vehicleCopy.computeAccelerationLoad(tc, rc, thetac, phic, vc, index, delta)
        acc_drag_g = vehicleCopy.computeAccelerationDrag(tc, rc, thetac, phic, vc, index, delta)
        dyn_pres_atm = vehicleCopy.computeDynPres(rc, vc) / 101325.0
        stag_pres_atm = vehicleCopy.computeStagPres(rc, vc) / 101325.0
        q_stag_con = vehicleCopy.qStagConvective(rc, vc)
        q_stag_rad = vehicleCopy.qStagRadiative(rc, vc)
        q_stag_total = q_stag_con + q_stag_rad
        heatload = cumtrapz(q_stag_total, tc, initial=heatLoad0)
        return (
         t_minc, h_kmc, v_kmsc, phi_degc, psi_degc, theta_degc,
         gamma_degc, drange_kmc, exitflag, acc_net_g, dyn_pres_atm,
         stag_pres_atm, q_stag_total, heatload, acc_drag_g)

    def makeBasicEntryPlots(self):
        """
                This function creates the evolution plots of the 
                altitude, speed, deceleration, and heat rate

                Parameters
                ----------
                None.
                
                Returns
                ----------
                1 image with 4 subplots

                """
        fig = plt.figure()
        fig.set_size_inches([6.5, 6.5])
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.subplot(2, 2, 1)
        plt.plot((self.t_minc), (self.h_kmc), 'r-', linewidth=2.0)
        plt.xlabel('Time, min', fontsize=10)
        plt.ylabel('Altitude, km', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        plt.subplot(2, 2, 2)
        plt.plot((self.t_minc), (self.v_kmsc), 'g-', linewidth=2.0)
        plt.xlabel('Time, min', fontsize=10)
        plt.ylabel('Velocity (km/s)', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        plt.subplot(2, 2, 3)
        plt.plot((self.t_minc), (self.acc_net_g), 'b-', linewidth=2.0)
        plt.xlabel('Time, min', fontsize=10)
        plt.ylabel('Deceleration (Earth g)', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        plt.subplot(2, 2, 4)
        plt.plot((self.t_minc), (self.q_stag_total), 'm-', linewidth=2.0)
        plt.xlabel('Time, min')
        plt.ylabel('Stag. point heat-rate (W/cm2)')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        plt.show()

    def isCaptured(self, t_sec, dt, delta_deg):
        """
                This function determines if the vehicle is captured.
                Returns -1 if the vehicle is captured, +1 otherwise.

                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                delta_deg : float
                        bank angle command, deg
                
                Returns
                ----------
                ans : int

                """
        self.propogateEntry(t_sec, dt, delta_deg)
        energy = self.computeEnergy(self.rc, self.vc)
        if energy[(self.index - 1)] < 0:
            ans = -1.0
        else:
            ans = 1.0
        return ans

    def hitsTargetApoapsis(self, t_sec, dt, delta_deg, targetApopasisAltitude_km):
        """
                This function is used to check if the vehicle undershoots 
                or overshoots. Does not include effect of planet rotation
                to compute inertial speed.

                Returns +1 if the vehicle is captured into an orbit with the 
                required target apoapsis alt, -1 otherwise.

                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                delta_deg : float
                        bank angle command, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                ans : int
                        -1 indicates overshoot, +1 indicates undershoot
                
                """
        self.propogateEntry(t_sec, dt, delta_deg)
        energy = self.computeEnergy(self.rc, self.vc)
        self.terminal_r = self.rc[(self.index - 1)]
        self.terminal_v = self.vc[(self.index - 1)]
        self.terminal_g = self.gammac[(self.index - 1)]
        self.terminal_E = self.computeEnergyScalar(self.terminal_r, self.terminal_v)
        self.terminal_h = self.computeAngMomScalar(self.terminal_r, self.terminal_v, self.terminal_g)
        self.terminal_a = self.computeSemiMajorAxisScalar(self.terminal_E)
        self.terminal_e = self.computeEccScalar(self.terminal_h, self.terminal_E)
        self.rp = self.terminal_a * (1.0 + self.terminal_e)
        self.hp = self.rp - self.planetObj.RP
        self.hp_km = self.hp / 1000.0
        terminal_alt = (self.terminal_r - self.planetObj.RP) / 1000.0
        if self.hp_km >= targetApopasisAltitude_km or self.terminal_a < 0:
            ans = -1.0
        else:
            ans = 1.0
        if terminal_alt < self.planetObj.h_low / 1000.0:
            ans = 1.0
        return ans

    def hitsTargetApoapsis2(self, t_sec, dt, delta_deg, targetApopasisAltitude_km):
        """
                This function is used to check if the vehicle undershoots 
                or overshoots. Includes effect of planet rotation to 
                calculate inertial speed.

                Returns +1 if the vehicle is captured into an orbit with the 
                required target apoapsis alt, -1 otherwise.

                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                delta_deg : float
                        bank angle command, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                ans : int
                        -1 indicates overshoot, +1 indicates undershoot
                
                """
        self.propogateEntry(t_sec, dt, delta_deg)
        energy = self.computeEnergy(self.rc, self.vc)
        terminal_r = self.rc[(self.index - 1)]
        terminal_v = self.vc[(self.index - 1)]
        terminal_g = self.gammac[(self.index - 1)]
        terminal_theta = self.thetac[(self.index - 1)]
        terminal_phi = self.phic[(self.index - 1)]
        terminal_psi = self.psic[(self.index - 1)]
        v_pr_x = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * (-1 * np.sin(terminal_theta)) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.cos(terminal_theta))
        v_pr_y = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.sin(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.sin(terminal_theta))
        v_pr_z = terminal_v * np.sin(terminal_g) * np.sin(terminal_phi) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * np.cos(terminal_phi)
        v_ie_x = v_pr_x + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.sin(terminal_theta) * -1.0
        v_ie_y = v_pr_y + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.cos(terminal_theta)
        v_ie_z = v_pr_z
        terminal_r_vec = terminal_r * np.array([np.cos(terminal_phi) * np.cos(terminal_theta),
         np.cos(terminal_phi) * np.sin(terminal_theta), np.sin(terminal_phi)])
        terminal_r_hat_vec = terminal_r_vec / np.linalg.norm(terminal_r_vec)
        terminal_v_ie_vec = np.array([v_ie_x, v_ie_y, v_ie_z])
        terminal_v_ie_hat_vec = terminal_v_ie_vec / np.linalg.norm(terminal_v_ie_vec)
        terminal_fpa_ie_deg = 90.0 - 180 / np.pi * np.arccos(np.dot(terminal_r_hat_vec, terminal_v_ie_hat_vec))
        terminal_fpa_ie_rad = terminal_fpa_ie_deg * np.pi / 180.0
        v_ie_mag = np.sqrt(v_ie_x ** 2 + v_ie_y ** 2 + v_ie_z ** 2)
        terminal_E = self.computeEnergyScalar(terminal_r, v_ie_mag)
        terminal_h = self.computeAngMomScalar(terminal_r, v_ie_mag, terminal_fpa_ie_rad)
        terminal_a = self.computeSemiMajorAxisScalar(terminal_E)
        terminal_e = self.computeEccScalar(terminal_h, terminal_E)
        rp = terminal_a * (1.0 + terminal_e)
        hp = rp - self.planetObj.RP
        hp_km = hp / 1000.0
        terminal_alt = (terminal_r - self.planetObj.RP) / 1000.0
        if hp_km >= targetApopasisAltitude_km or terminal_a < 0:
            ans = -1.0
        else:
            ans = 1.0
        if terminal_alt < self.planetObj.h_low / 1000.0:
            ans = 1.0
        return ans

    def findOverShootLimit(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                Computes the overshoot limit entry flight-path angle
                for aerocapture vehicle using bisection algorithm.

                This is shallowest entry flight path angle for which a full lift down
                trajectory gets the vehicle captured into a post atmospheric exit orbit 
                with the desired target apoapsis altitude.

                Note: the overshoot limit entry flight path angle should be computed 
                with an accuracy of at least 10 decimal places to ensure the correct 
                atmospheric trajectory is simulated. 

                A bisection algorithm is used to compute the overshoot limit.

                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the overshoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                overShootLimit : float
                        overshoot limit EFPA, deg
                exitflag_os : float
                        flag to indicate if a solution could not be found for the 
                        overshoot limit

                exitflag_os = 1.0 indicates over shoot limit was found.
                exitflag_os = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                """
        delta_deg = 180.0
        temp_var = self.gamma0_deg
        self.gamma0_deg = gamma0_deg_guess_low
        ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        self.gamma0_deg = gamma0_deg_guess_high
        ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        if ans1 * ans2 < 0:
            while abs(gamma0_deg_guess_high - gamma0_deg_guess_low) > gamma_deg_tol:
                gamma0_deg_guess_mid = 0.5 * (gamma0_deg_guess_low + gamma0_deg_guess_high)
                self.gamma0_deg = gamma0_deg_guess_low
                ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_mid
                ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_high
                ans3 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                if ans1 * ans2 < 0:
                    gamma0_deg_guess_high = gamma0_deg_guess_mid
                else:
                    if ans2 * ans3 < 0:
                        gamma0_deg_guess_low = gamma0_deg_guess_mid
                overShootLimit = gamma0_deg_guess_high
                exitflag_os = 1.0

        else:
            print('Overshoot limit is outside user specified bounds.')
            overShootLimit = 0.0
            exitflag_os = 0.0
        self.gamma0_deg = temp_var
        return (
         overShootLimit, exitflag_os)

    def findOverShootLimit2(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                Computes the overshoot limit entry flight-path angle
                for aerocapture vehicle using bisection algorithm.
                Includes effect of planet rotation on inertial speed.

                This is shallowest entry flight path angle for which a full lift down
                trajectory gets the vehicle captured into a post atmospheric exit orbit 
                with the desired target apoapsis altitude.

                Note: the overshoot limit entry flight path angle should be computed 
                with an accuracy of at least 10 decimal places to ensure the correct 
                atmospheric trajectory is simulated. 

                A bisection algorithm is used to compute the overshoot limit.

                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the overshoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                overShootLimit : float
                        overshoot limit EFPA, deg
                exitflag_os : float
                        flag to indicate if a solution could not be found for the 
                        overshoot limit

                exitflag_os = 1.0 indicates over shoot limit was found.
                exitflag_os = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                """
        delta_deg = 180.0
        temp_var = self.gamma0_deg
        self.gamma0_deg = gamma0_deg_guess_low
        ans1 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        self.gamma0_deg = gamma0_deg_guess_high
        ans2 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        if ans1 * ans2 < 0:
            while abs(gamma0_deg_guess_high - gamma0_deg_guess_low) > gamma_deg_tol:
                gamma0_deg_guess_mid = 0.5 * (gamma0_deg_guess_low + gamma0_deg_guess_high)
                self.gamma0_deg = gamma0_deg_guess_low
                ans1 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_mid
                ans2 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_high
                ans3 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                if ans1 * ans2 < 0:
                    gamma0_deg_guess_high = gamma0_deg_guess_mid
                else:
                    if ans2 * ans3 < 0:
                        gamma0_deg_guess_low = gamma0_deg_guess_mid
                overShootLimit = gamma0_deg_guess_high
                exitflag_os = 1.0

        else:
            print('Overshoot limit is outside user specified bounds.')
            overShootLimit = 0.0
            exitflag_os = 0.0
        self.gamma0_deg = temp_var
        return (
         overShootLimit, exitflag_os)

    def findUnderShootLimit(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                Computes the undershoot limit entry flight-path angle
                for aerocapture vehicle using bisection algorithm.

                This is steepest entry flight path angle for which a full lift up
                trajectory gets the vehicle captured into a post atmospheric exit orbit 
                with the desired target apoapsis altitude.

                Note: the undershoor limit entry flight path angle should be computed 
                with an accuracy of at least 6 decimal places to ensure the correct 
                atmospheric trajectory is simulated. 

                A bisection algorithm is used to compute the undershoot limit.

                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the overshoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                underShootLimit : float
                        overshoot limit EFPA, deg
                exitflag_us : float
                        flag to indicate if a solution could not be found for the 
                        undershoot limit

                exitflag_us = 1.0 indicates undershoot limit was found.
                exitflag_us = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                """
        delta_deg = 0.0
        temp_var = self.gamma0_deg
        self.gamma0_deg = gamma0_deg_guess_low
        ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        self.gamma0_deg = gamma0_deg_guess_high
        ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        if ans1 * ans2 < 0:
            while abs(gamma0_deg_guess_high - gamma0_deg_guess_low) > gamma_deg_tol:
                gamma0_deg_guess_mid = 0.5 * (gamma0_deg_guess_low + gamma0_deg_guess_high)
                self.gamma0_deg = gamma0_deg_guess_low
                ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_mid
                ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_high
                ans3 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                if ans1 * ans2 < 0:
                    gamma0_deg_guess_high = gamma0_deg_guess_mid
                else:
                    if ans2 * ans3 < 0:
                        gamma0_deg_guess_low = gamma0_deg_guess_mid
                underShootLimit = gamma0_deg_guess_high
                exitflag_us = 1.0

        else:
            print('Undershoot limit is outside user specified bounds.')
            underShootLimit = 0.0
            exitflag_os = 0.0
        self.gamma0_deg = temp_var
        return (
         underShootLimit, exitflag_us)

    def findUnderShootLimit2(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                Computes the undershoot limit entry flight-path angle
                for aerocapture vehicle using bisection algorithm.
                Includes effect of planet rotation on inertial speed.

                This is steepest entry flight path angle for which a full lift up
                trajectory gets the vehicle captured into a post atmospheric exit orbit 
                with the desired target apoapsis altitude.

                Note: the undershoor limit entry flight path angle should be computed 
                with an accuracy of at least 6 decimal places to ensure the correct 
                atmospheric trajectory is simulated. 

                A bisection algorithm is used to compute the undershoot limit.

                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the overshoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                underShootLimit : float
                        overshoot limit EFPA, deg
                exitflag_us : float
                        flag to indicate if a solution could not be found for the 
                        undershoot limit

                exitflag_us = 1.0 indicates undershoot limit was found.
                exitflag_us = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                """
        delta_deg = 0.0
        temp_var = self.gamma0_deg
        self.gamma0_deg = gamma0_deg_guess_low
        ans1 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        self.gamma0_deg = gamma0_deg_guess_high
        ans2 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        if ans1 * ans2 < 0:
            while abs(gamma0_deg_guess_high - gamma0_deg_guess_low) > gamma_deg_tol:
                gamma0_deg_guess_mid = 0.5 * (gamma0_deg_guess_low + gamma0_deg_guess_high)
                self.gamma0_deg = gamma0_deg_guess_low
                ans1 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_mid
                ans2 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_high
                ans3 = self.hitsTargetApoapsis2(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                if ans1 * ans2 < 0:
                    gamma0_deg_guess_high = gamma0_deg_guess_mid
                else:
                    if ans2 * ans3 < 0:
                        gamma0_deg_guess_low = gamma0_deg_guess_mid
                underShootLimit = gamma0_deg_guess_high
                exitflag_us = 1.0

        else:
            print('Undershoot limit is outside user specified bounds.')
            underShootLimit = 0.0
            exitflag_os = 0.0
        self.gamma0_deg = temp_var
        return (
         underShootLimit, exitflag_us)

    def computeTCW(self, t_sec, dt, gamma0_deg_guess_low_os, gamma0_deg_guess_high_os, gamma0_deg_guess_low_us, gamma0_deg_guess_high_us, gamma_deg_tol_os, gamma_deg_tol_us, targetApopasisAltitude_km):
        """
                Computes the theoretical corridor width (TCW) for 
                lift modulation aerocapture.

                TCW = overShootLimit - underShootLimit
                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low_os : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high_os : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_low_us : float
                        lower bound for the guess of undershoot limit FPA, deg
                gamma0_deg_guess_high_us : float
                        upper bound for the guess of undershoot limit FPA, deg
                gamma_deg_tol_os : float
                        desired accuracy for computation of the overshoot limit, deg
                gamma_deg_tol_us : float
                        desired accuracy for computation of the undershoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                TCW : float
                        Theoretical Corridor Width, deg
                """
        overShootLimit, exitflag_os = self.findOverShootLimit(t_sec, dt, gamma0_deg_guess_low_os, gamma0_deg_guess_high_os, gamma_deg_tol_os, targetApopasisAltitude_km)
        underShootLimit, exitflag_us = self.findUnderShootLimit(t_sec, dt, gamma0_deg_guess_low_us, gamma0_deg_guess_high_us, gamma_deg_tol_us, targetApopasisAltitude_km)
        print('Overshoot Limit  : ' + str(overShootLimit) + ' deg.')
        print('Undershoot Limit : ' + str(underShootLimit) + ' deg.')
        TCW = overShootLimit - underShootLimit
        print('Corridor Width   : ' + str(TCW) + ' deg.')
        return TCW

    def computeTCW2(self, t_sec, dt, gamma0_deg_guess_low_os, gamma0_deg_guess_high_os, gamma0_deg_guess_low_us, gamma0_deg_guess_high_us, gamma_deg_tol_os, gamma_deg_tol_us, targetApopasisAltitude_km):
        """
                Computes the theoretical corridor width (TCW) for 
                lift modulation aerocapture. Includes effect of planet rotation.

                TCW = overShootLimit - underShootLimit
                
                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low_os : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high_os : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_low_us : float
                        lower bound for the guess of undershoot limit FPA, deg
                gamma0_deg_guess_high_us : float
                        upper bound for the guess of undershoot limit FPA, deg
                gamma_deg_tol_os : float
                        desired accuracy for computation of the overshoot limit, deg
                gamma_deg_tol_us : float
                        desired accuracy for computation of the undershoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                TCW : float
                        Theoretical Corridor Width, deg
                """
        overShootLimit, exitflag_os = self.findOverShootLimit2(t_sec, dt, gamma0_deg_guess_low_os, gamma0_deg_guess_high_os, gamma_deg_tol_os, targetApopasisAltitude_km)
        underShootLimit, exitflag_us = self.findUnderShootLimit2(t_sec, dt, gamma0_deg_guess_low_us, gamma0_deg_guess_high_us, gamma_deg_tol_us, targetApopasisAltitude_km)
        print('Overshoot Limit  : ' + str(overShootLimit) + ' deg.')
        print('Undershoot Limit : ' + str(underShootLimit) + ' deg.')
        TCW = overShootLimit - underShootLimit
        print('Corridor Width   : ' + str(TCW) + ' deg.')
        return TCW

    def setDragModulationVehicleParams(self, beta1, betaRatio):
        """
                Set the beta1 and betaRatio params for a drag modulation vehicle.

                Parameters
                ----------
                beta1 : float
                        small value of ballistic coefficient, kg/m2
                betaRatio : float
                        ballistic coefficient ratio
                """
        self.beta1 = beta1
        self.betaRatio = betaRatio

    def findEFPALimitD(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                This function computes the limiting EFPA for drag modulation
                aerocapture.

                A bisection algorithm is used to compute the limit.

                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                EFPALimit : float
                        limit EFPA, deg
                exitflag : float
                        flag to indicate if a solution could not be found for the 
                        limit EFPA

                exitflag = 1.0 indicates over shoot limit was found.
                exitflag = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                
                """
        temp_var_1 = self.gamma0_deg
        temp_var_2 = self.LD
        delta_deg = 0.0
        self.LD = 0.0
        self.gamma0_deg = gamma0_deg_guess_low
        ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        self.gamma0_deg = gamma0_deg_guess_high
        ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
        if ans1 * ans2 < 0:
            while abs(gamma0_deg_guess_high - gamma0_deg_guess_low) > gamma_deg_tol:
                gamma0_deg_guess_mid = 0.5 * (gamma0_deg_guess_low + gamma0_deg_guess_high)
                self.gamma0_deg = gamma0_deg_guess_low
                ans1 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_mid
                ans2 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                self.gamma0_deg = gamma0_deg_guess_high
                ans3 = self.hitsTargetApoapsis(t_sec, dt, delta_deg, targetApopasisAltitude_km)
                if ans1 * ans2 < 0:
                    gamma0_deg_guess_high = gamma0_deg_guess_mid
                else:
                    if ans2 * ans3 < 0:
                        gamma0_deg_guess_low = gamma0_deg_guess_mid
                EFPALimit = gamma0_deg_guess_high
                exitflag = 1.0

        else:
            print('EFPA limit is outside user specified bounds.')
            EFPALimit = 0.0
            exitflag = 0.0
        self.gamma0_deg = temp_var_1
        self.LD = temp_var_2
        return (
         EFPALimit, exitflag)

    def findUnderShootLimitD(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                This function computes the limiting undershoot 
                EFPA for drag modulation aerocapture.

                Parameters:
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                underShootLimitD : float
                        undershoot limit EFPA, deg
                exitflagD_us : float
                        flag to indicate if a solution could not be found for the 
                        undershoot limit EFPA

                exitflagD_us = 1.0 indicates undershoot limit was found.
                exitflagD_us = 0.0 indicates undershoot limit was not found 
                within user specified bounds.
                
                """
        self.beta = self.beta1 * self.betaRatio
        self.CD = self.mass / (self.beta * self.A)
        underShootLimitD, exitflagD_us = self.findEFPALimitD(t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km)
        return (
         underShootLimitD, exitflagD_us)

    def findOverShootLimitD(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                This function computes the limiting overshoot 
                EFPA for drag modulation aerocapture.

                Parameters:
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low : float
                        lower bound for the guess of limit FPA, deg
                gamma0_deg_guess_high : float
                        upper bound for the guess of limit FPA, deg
                gamma_deg_tol : float
                        desired accuracy for computation of the limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                overShootLimitD : float
                        overshoot limit EFPA, deg
                exitflagD_os : float
                        flag to indicate if a solution could not be found for the 
                        overshoot limit EFPA

                exitflagD_os = 1.0 indicates over shoot limit was found.
                exitflagD_os = 0.0 indicates overshoot limit was not found 
                within user specified bounds.
                
                """
        self.beta = self.beta1
        self.CD = self.mass / (self.beta * self.A)
        overShootLimitD, exitflagD_os = self.findEFPALimitD(t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km)
        return (
         overShootLimitD, exitflagD_os)

    def computeTCWD(self, t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km):
        """
                Computes the theoretical corridor width (TCWD) for 
                drag modulation aerocapture.

                TCWD = overShootLimit - underShootLimit
                
                Parameters:
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. time step, seconds
                gamma0_deg_guess_low_os : float
                        lower bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_high_os : float
                        upper bound for the guess of overshoot limit FPA, deg
                gamma0_deg_guess_low_us : float
                        lower bound for the guess of undershoot limit FPA, deg
                gamma0_deg_guess_high_us : float
                        upper bound for the guess of undershoot limit FPA, deg
                gamma_deg_tol_os : float
                        desired accuracy for computation of the overshoot limit, deg
                gamma_deg_tol_us : float
                        desired accuracy for computation of the undershoot limit, deg
                targetApopasisAltitude_km : float
                        target apoapsis altitude , km
                
                Returns
                ----------
                TCWD : float
                        Theoretical Corridor Width (Drag Modulation), deg
                """
        underShootLimitD, exitflagD_us = self.findUnderShootLimitD(t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km)
        overshootLimitD, exitflagD_os = self.findOverShootLimitD(t_sec, dt, gamma0_deg_guess_low, gamma0_deg_guess_high, gamma_deg_tol, targetApopasisAltitude_km)
        TCWD = overshootLimitD - underShootLimitD
        return TCWD

    def createQPlot(self, t_sec, dt, delta_deg):
        """
                Creates q-plots as described by Cerimele and Gamble, 1985.

                Parameters
                ----------
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. solver time step
                delta_deg : float
                        commanded bank angle, degrees

                Returns
                ---------
                plt.plot object

                """
        self.propogateEntry(t_sec, dt, delta_deg)
        a = -0.1685655880914111
        b = 50777.96070410234
        x_arr = np.linspace(100000.0, 298000.0, 101)
        y_arr = a * x_arr + b
        fig = plt.figure()
        fig.set_size_inches([3.25, 3.25])
        plt.rc('font', family='Times New Roman')
        params = {'mathtext.default': 'regular'}
        plt.rcParams.update(params)
        plt.plot((self.h_kmc * 1000.0), (self.dyn_pres_atm * 101325.0), 'r-', linewidth=3.0)
        plt.xlim(100000.0, 700000.0)
        plt.ylim(0.0, 12500.0)
        plt.plot(x_arr, y_arr, 'k-', linewidth=2.0, linestyle='dashed')
        plt.xlabel('Altitude, m', fontsize=10)
        plt.ylabel('Dynamic pressure, Pa ', fontsize=10)
        plt.xticks((np.array([200000.0, 400000.0, 600000.0])), fontsize=10)
        ax = plt.gca()
        ax.tick_params(direction='in')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(direction='in')
        ax.annotate('$\\bar{q} = -0.1686h + 50778$', xy=(248586, 9103.4),
          xytext=(331181, 9103.4),
          arrowprops=dict(arrowstyle='<-'),
          va='center',
          ha='left',
          fontsize=9)
        plt.show()

    def compute_ApoapsisAltitudeKm(self, terminal_r, terminal_v, terminal_g, terminal_theta, terminal_phi, terminal_psi):
        """
                Compute the apoapsis altitude given conditions at 
                atmospheric exit interface. Note this function includes
                correction to account for rotation of planet.

                Terminal values refer to those at atmospheric exit.

                Parameters
                ---------
                terminal_r : float
                        radial distance, m
                terminal_v : float
                        terminal speed, m/s
                terminal_g : float
                        terminal FPA, rad
                terminal_theta : float
                        terminal longitude, rad
                terminal_phi : float
                        terminal latitude, rad
                terminal_psi : float
                        terminal heading angle

                Returns
                --------
                hp_km : float
                        apoapsis altitude, km

                """
        v_pr_x = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * (-1 * np.sin(terminal_theta)) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.cos(terminal_theta))
        v_pr_y = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.sin(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.sin(terminal_theta))
        v_pr_z = terminal_v * np.sin(terminal_g) * np.sin(terminal_phi) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * np.cos(terminal_phi)
        v_ie_x = v_pr_x + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.sin(terminal_theta) * -1.0
        v_ie_y = v_pr_y + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.cos(terminal_theta)
        v_ie_z = v_pr_z
        terminal_r_vec = terminal_r * np.array([np.cos(terminal_phi) * np.cos(terminal_theta),
         np.cos(terminal_phi) * np.sin(terminal_theta), np.sin(terminal_phi)])
        terminal_r_hat_vec = terminal_r_vec / np.linalg.norm(terminal_r_vec)
        terminal_v_ie_vec = np.array([v_ie_x, v_ie_y, v_ie_z])
        terminal_v_ie_hat_vec = terminal_v_ie_vec / np.linalg.norm(terminal_v_ie_vec)
        terminal_fpa_ie_deg = 90.0 - 180 / np.pi * np.arccos(np.dot(terminal_r_hat_vec, terminal_v_ie_hat_vec))
        terminal_fpa_ie_rad = terminal_fpa_ie_deg * np.pi / 180.0
        v_ie_mag = np.sqrt(v_ie_x ** 2 + v_ie_y ** 2 + v_ie_z ** 2)
        terminal_E = self.computeEnergyScalar(terminal_r, v_ie_mag)
        terminal_h = self.computeAngMomScalar(terminal_r, v_ie_mag, terminal_fpa_ie_rad)
        terminal_a = self.computeSemiMajorAxisScalar(terminal_E)
        terminal_e = self.computeEccScalar(terminal_h, terminal_E)
        rp = terminal_a * (1.0 + terminal_e)
        hp = rp - self.planetObj.RP
        hp_km = hp / 1000.0
        return hp_km

    def compute_PeriapsisAltitudeKm(self, terminal_r, terminal_v, terminal_g, terminal_theta, terminal_phi, terminal_psi):
        """
                Compute the periapsis altitude given conditions at 
                atmospheric exit interface. Note this function includes
                correction to account for rotation of planet.

                Terminal values refer to those at atmospheric exit.

                Parameters
                ---------
                terminal_r : float
                        radial distance, m
                terminal_v : float
                        terminal speed, m/s
                terminal_g : float
                        terminal FPA, rad
                terminal_theta : float
                        terminal longitude, rad
                terminal_phi : float
                        terminal latitude, rad
                terminal_psi : float
                        terminal heading angle

                Returns
                --------
                hp_km : float
                        periapsis altitude, km

                """
        v_pr_x = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * (-1 * np.sin(terminal_theta)) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.cos(terminal_theta))
        v_pr_y = terminal_v * np.sin(terminal_g) * np.cos(terminal_phi) * np.sin(terminal_theta) + terminal_v * np.cos(terminal_g) * np.cos(terminal_psi) * np.cos(terminal_theta) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * (-1 * np.sin(terminal_phi) * np.sin(terminal_theta))
        v_pr_z = terminal_v * np.sin(terminal_g) * np.sin(terminal_phi) + terminal_v * np.cos(terminal_g) * np.sin(terminal_psi) * np.cos(terminal_phi)
        v_ie_x = v_pr_x + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.sin(terminal_theta) * -1.0
        v_ie_y = v_pr_y + terminal_r * self.planetObj.OMEGA * np.cos(terminal_phi) * np.cos(terminal_theta)
        v_ie_z = v_pr_z
        terminal_r_vec = terminal_r * np.array([np.cos(terminal_phi) * np.cos(terminal_theta),
         np.cos(terminal_phi) * np.sin(terminal_theta), np.sin(terminal_phi)])
        terminal_r_hat_vec = terminal_r_vec / np.linalg.norm(terminal_r_vec)
        terminal_v_ie_vec = np.array([v_ie_x, v_ie_y, v_ie_z])
        terminal_v_ie_hat_vec = terminal_v_ie_vec / np.linalg.norm(terminal_v_ie_vec)
        terminal_fpa_ie_deg = 90.0 - 180 / np.pi * np.arccos(np.dot(terminal_r_hat_vec, terminal_v_ie_hat_vec))
        terminal_fpa_ie_rad = terminal_fpa_ie_deg * np.pi / 180.0
        v_ie_mag = np.sqrt(v_ie_x ** 2 + v_ie_y ** 2 + v_ie_z ** 2)
        terminal_E = self.computeEnergyScalar(terminal_r, v_ie_mag)
        terminal_h = self.computeAngMomScalar(terminal_r, v_ie_mag, terminal_fpa_ie_rad)
        terminal_a = self.computeSemiMajorAxisScalar(terminal_E)
        terminal_e = self.computeEccScalar(terminal_h, terminal_E)
        rp = terminal_a * (1.0 - terminal_e)
        hp = rp - self.planetObj.RP
        hp_km = hp / 1000.0
        return hp_km

    def createDensityMeasuredFunction(self, h_step_array, density_mes_array, lowAlt_km, numPoints_lowAlt):
        """
                Computes a density function based on measurements made during the 
                descending leg of the aerocapture maneuver.

                Parameters
                ----------
                h_step_array : numpy.ndarray
                        height array at which density is measured, km
                density_mes_array : float
                        density array corresponding to h_step_array, kg/m3
                lowAlt_km : float
                        lower altitude to which density model is to be extrapolated
                        based on available measurements, km
                numPoints_lowAlt : int
                        number of points to evaluate extrapolation at below the 
                        altitude where measurements are available.

                Returns
                ----------
                density_mes_int : scipy.interpolate.interpolate.interp1d
                        interpolated measured density lookup function 
                minAlt : float       
                        minimum altitude at which density measurements were available
                
                """
        h_step_array = np.delete(h_step_array, 0)
        density_mes_array = np.delete(density_mes_array, 0)
        minAltIndex = np.argmin(h_step_array)
        minAlt = h_step_array[minAltIndex] * 1000.0
        density_mes_int_upper = interp1d((h_step_array * 1000.0), density_mes_array,
          kind='linear', fill_value=(
         max(density_mes_array),
         min(density_mes_array)),
          bounds_error=False)
        scaleHeightminAlt = self.planetObj.scaleHeight(minAlt, density_mes_int_upper)
        h_low_array = np.linspace(minAlt - 1000.0, lowAlt_km * 1000.0, numPoints_lowAlt)
        d_low_array = density_mes_int_upper(minAlt) * np.exp((minAlt - h_low_array) / scaleHeightminAlt)
        h_array = np.concatenate((h_step_array * 1000.0, h_low_array), axis=0)
        d_array = np.concatenate((density_mes_array, d_low_array), axis=0)
        density_mes_int = interp1d(h_array, d_array, kind='linear', fill_value=(
         max(d_array), min(d_array)),
          bounds_error=False)
        return (
         density_mes_int, minAlt)

    def setMaxRollRate(self, maxRollRate):
        """
                Set the maximum allowed vehicle roll rate (deg/s)
                
                Parameters
                ----------
                maxRollRate : float
                        maximum roll rate, degrees per second
                """
        self.maxRollRate = maxRollRate

    def psuedoController(self, DeltaCMD_deg_command, Delta_deg_ini, timestep):
        """
                Pseudo controller implenetation for maximum roll rate 
                constraint.
                
                Parameters
                ----------
                DeltaCMD_deg_command : float
                        commanded bank angle from guidance algorithm, deg
                Delta_deg_ini : float      
                        current vehicle bank angle, deg
                maxBankRate : float
                        maximum allowed roll rate, deg/s
                timestep : float
                        guidance cycle timestep
                
                Returns
                ----------
                DeltaCMD_deg : float   
                        actual bank angle response using pseudocontroller, deg
                Delta_deg_ini : float
                        current bank angle, same as actual bank angle 
                        (is redundant)
                
                """
        if np.abs(DeltaCMD_deg_command - Delta_deg_ini) > self.maxRollRate * timestep:
            DeltaCMD_deg = Delta_deg_ini + np.sign(DeltaCMD_deg_command - Delta_deg_ini) * self.maxRollRate * timestep
            Delta_deg_ini = DeltaCMD_deg
        else:
            bankRate = np.abs(DeltaCMD_deg_command - Delta_deg_ini) / timestep
            DeltaCMD_deg = Delta_deg_ini + np.sign(DeltaCMD_deg_command - Delta_deg_ini) * self.maxRollRate * timestep
            Delta_deg_ini = DeltaCMD_deg
        return (DeltaCMD_deg, Delta_deg_ini)

    def predictApoapsisAltitudeKm_withLiftUp(self, h0_km, theta0_deg, phi0_deg, v0_kms, gamma0_deg, psi0_deg, drange0_km, heatLoad0, t_sec, dt, delta_deg, density_mes_int):
        """
                Compute apoapsis altitude using full lift up bank 
                command from current vehicle state till atmospheric exit.

                Parameters
                ----------
                h0_km : float
                        current vehicle altitude, km
                theta0_deg : float
                        current vehicle longitude, deg
                phi0_deg : float
                        current vehicle latitude, deg
                v0_kms : float
                        current vehicle speed, km/s
                gamma0_deg : float
                        current FPA, deg
                psi0_deg : float
                        current heading angle, deg
                drange0_km : float
                        current downrange, km
                heatLoad0 : float
                        current heatload, J/cm2
                t_sec : float
                        propogation time, seconds
                dt : float
                        max. solver timestep
                delta_deg : float
                        commanded bank angle, deg
                density_mes_int : scipy.interpolate.interpolate.interp1d
                        measured density interpolation function

                """
        t_minc, h_kmc, v_kmsc, phi_degc, psi_degc, theta_degc, gamma_degc, drange_kmc, exitflag, acc_net_g, dyn_pres_atm, stag_pres_atm, q_stag_total, heatload, acc_drag_g = self.propogateEntry2(h0_km, theta0_deg, phi0_deg, v0_kms, gamma0_deg, psi0_deg, drange0_km, heatLoad0, t_sec, dt, delta_deg, density_mes_int)
        terminal_apoapsis_km = self.compute_ApoapsisAltitudeKm(self.planetObj.RP + h_kmc[(-1)] * 1000.0, v_kmsc[(-1)] * 1000.0, gamma_degc[(-1)] * np.pi / 180.0, theta_degc[(-1)] * np.pi / 180.0, phi_degc[(-1)] * np.pi / 180.0, psi_degc[(-1)] * np.pi / 180.0)
        return terminal_apoapsis_km

    def setTargetOrbitParams(self, target_peri_km, target_apo_km, target_apo_km_tol):
        """
                Set the target capture orbit parameters.

                Parameters
                ----------
                target_peri_km : float
                        target periapsis altitude, km
                target_apo_km : float
                        target apoapsis altitude, km
                target_apo_km_tol : float
                        target apoapsis altitude error tolerance, km
                        used by guidance algorithm
                """
        self.target_peri_km = target_peri_km
        self.target_apo_km = target_apo_km
        self.target_apo_km_tol = target_apo_km_tol

    def compute_periapsis_raise_DV(self, current_peri_km, current_apo_km, target_peri_km):
        """
                Compute the propulsive DV to raise the orbit periapsis to 
                the target value.

                Parameters
                ----------
                current_peri_km : float
                        current periapsis altitude, km
                current_apo_km  : float
                        current apoapsis altitude, km
                target_peri_km  : float
                        target periapsis altitude, km
                
                Returns
                ----------
                dV :float
                        periapse raise DV, m/s
                
                """
        E_current = -self.planetObj.GM / (self.planetObj.RP + current_apo_km * 1000.0 + current_peri_km * 1000.0 + self.planetObj.RP)
        v_apo_current = np.sqrt(2 * E_current + 2 * self.planetObj.GM / (self.planetObj.RP + current_apo_km * 1000.0))
        E_target = -self.planetObj.GM / (self.planetObj.RP + current_apo_km * 1000.0 + target_peri_km * 1000.0 + self.planetObj.RP)
        v_apo_target = np.sqrt(2 * E_target + 2 * self.planetObj.GM / (self.planetObj.RP + current_apo_km * 1000.0))
        dV = v_apo_target - v_apo_current
        return dV

    def compute_apoapsis_raise_DV(self, peri_km_current, apo_km_current, apo_km_target):
        """
                Compute the propulsive DV to raise the orbit apoapsis to 
                the target value.

                Parameters
                ----------
                peri_km_current : float
                        current periapsis altitude, km
                apo_km_current  : float
                        current apoapsis altitude, km
                apo_km_target  : float
                        target apoapsis altitude, km
                
                Returns
                ----------
                dV :float
                        apoapsis raise DV, m/s
                
                """
        E_current = -self.planetObj.GM / (self.planetObj.RP + apo_km_current * 1000.0 + peri_km_current * 1000.0 + self.planetObj.RP)
        v_peri_current = np.sqrt(2 * E_current + 2 * self.planetObj.GM / (peri_km_current * 1000.0 + self.planetObj.RP))
        E_target = -self.planetObj.GM / (apo_km_target * 1000.0 + self.planetObj.RP + peri_km_current * 1000.0 + self.planetObj.RP)
        v_peri_target = np.sqrt(2 * E_target + 2 * self.planetObj.GM / (peri_km_current * 1000.0 + self.planetObj.RP))
        dV = v_peri_target - v_peri_current
        return dV

    def setEquilibriumGlideParams(self, Ghdot, Gq, v_switch_kms, lowAlt_km, numPoints_lowAlt, hdot_threshold):
        """
                Set equilibrium glide phase guidance parameters

                Parameters
                -----------
                Ghdot : float
                        Ghdot term
                Gq : float
                        Gq term
                v_switch_kms : float
                        speed below which eq. glide phase is terminated
                lowAlt_km : float
                        lower altitude to which density model is to be extrapolated
                        based on available measurements, km
                numPoints_lowAlt : int
                        number of points to evaluate extrapolation at below the 
                        altitude where measurements are available
                hdot_threshold : float
                        threshold altitude rate (m/s) above which density measurement
                        is terminated and apoapsis prediction is initiated

                """
        self.Ghdot = Ghdot
        self.Gq = Gq
        self.v_switch_kms = v_switch_kms
        self.lowAlt_km = lowAlt_km
        self.numPoints_lowAlt = numPoints_lowAlt
        self.hdot_threshold = hdot_threshold

    def propogateEquilibriumGlide(self, timeStep, dt, maxTimeSecs):
        """
                Implements the equilibrium glide phase of the guidance scheme.

                Parameters
                --------
                timeStep : float
                        Guidance cycle time, seconds
                dt : float
                        Solver max. time step, seconds
                maxTimeSecs : float
                        max. time for propogation, seconds

                """
        counter = 0
        g0 = self.planetObj.GM / self.planetObj.RP ** 2
        h_skip_km = self.planetObj.h_skip / 1000.0
        self.t_step_array = np.array([0.0])
        self.delta_deg_array = np.array([0.0])
        self.hdot_array = np.array([0.0])
        self.hddot_array = np.array([0.0])
        self.qref_array = np.array([0.0])
        self.q_array = np.array([0.0])
        self.h_step_array = np.array([0.0])
        self.acc_step_array = np.array([0.0])
        self.acc_drag_array = np.array([0.0])
        self.density_mes_array = np.array([0.0])
        self.propogateEntry(1.0, dt, 0.0)
        t_min = self.t_minc
        h_km = self.h_kmc
        v_kms = self.v_kmsc
        phi_deg = self.phi_degc
        psi_deg = self.psi_degc
        theta_deg = self.theta_degc
        gamma_deg = self.gamma_degc
        drange_km = self.drange_kmc
        acc_net_g = self.acc_net_g
        dyn_pres_atm = self.dyn_pres_atm
        stag_pres_atm = self.stag_pres_atm
        q_stag_total = self.q_stag_total
        heatload = self.heatload
        acc_drag_g = self.acc_drag_g
        self.h_current_km = h_km[(-1)]
        self.v_current_kms = v_kms[(-1)]
        customFlag = 0.0
        Delta_deg_ini = 0.0
        while self.v_current_kms > self.v_switch_kms:
            h0_km = h_km[(-1)]
            theta0_deg = theta_deg[(-1)]
            phi0_deg = phi_deg[(-1)]
            v0_kms = v_kms[(-1)]
            psi0_deg = psi_deg[(-1)]
            gamma0_deg = gamma_deg[(-1)]
            drange0_km = drange_km[(-1)]
            h0 = h0_km * 1000.0
            theta0 = theta0_deg * np.pi / 180.0
            phi0 = phi0_deg * np.pi / 180.0
            v0 = v0_kms * 1000.0
            psi0 = psi0_deg * np.pi / 180.0
            gamma0 = gamma0_deg * np.pi / 180.0
            hi = h0
            ri = h0 + self.planetObj.RP
            vi = v0
            qi = 0.5 * self.planetObj.density(hi) * vi ** 2.0
            gammai = gamma0
            hdoti = vi * np.sin(gammai)
            qrefi = -1.0 * self.mass * g0 / (0.75 * self.CL * self.A) * (1 - vi ** 2.0 / (g0 * ri))
            Ji = self.heatload[(-1)]
            cosDeltaEQGL = self.mass * g0 / (self.CL * qi * self.A) * (1.0 - vi ** 2.0 / (g0 * ri))
            cosDeltaCMD = cosDeltaEQGL - self.Ghdot * hdoti / qi + self.Gq * ((qi - qrefi) / qi)
            if cosDeltaCMD > 1.0:
                DeltaCMD = 0.0
            else:
                if cosDeltaCMD < -1.0:
                    DeltaCMD = np.pi
                else:
                    DeltaCMD = np.arccos(cosDeltaCMD)
            DeltaCMD_deg_command = DeltaCMD * 180.0 / np.pi
            DeltaCMD_deg, Delta_deg_ini = self.psuedoController(DeltaCMD_deg_command, Delta_deg_ini, timeStep)
            self.setInitialState(h0_km, theta0_deg, phi0_deg, v0_kms, psi0_deg, gamma0_deg, drange0_km, Ji)
            self.propogateEntry(timeStep, dt, DeltaCMD_deg)
            t_min_c = self.t_minc
            h_km_c = self.h_kmc
            v_kms_c = self.v_kmsc
            phi_deg_c = self.phi_degc
            psi_deg_c = self.psi_degc
            theta_deg_c = self.theta_degc
            gamma_deg_c = self.gamma_degc
            drange_km_c = self.drange_kmc
            acc_net_g_c = self.acc_net_g
            dyn_pres_atm_c = self.dyn_pres_atm
            stag_pres_atm_c = self.stag_pres_atm
            q_stag_total_c = self.q_stag_total
            heatload_c = self.heatload
            acc_drag_g_c = self.acc_drag_g
            t_min_c = t_min_c + t_min[(-1)]
            self.t_step_array = np.append(self.t_step_array, t_min[(-1)])
            self.delta_deg_array = np.append(self.delta_deg_array, DeltaCMD_deg)
            self.hdot_array = np.append(self.hdot_array, hdoti)
            self.qref_array = np.append(self.qref_array, qrefi)
            self.q_array = np.append(self.q_array, qi)
            self.h_step_array = np.append(self.h_step_array, h0_km)
            self.hdotref_array = np.zeros(len(self.t_step_array))
            self.hddoti = (self.hdot_array[(-1)] - self.hdot_array[(-2)]) / (self.t_step_array[(-1)] * 60.0 - self.t_step_array[(-2)] * 60.0)
            self.hddot_array = np.append(self.hddot_array, self.hddoti)
            self.acc_step_array = np.append(self.acc_step_array, self.acc_net_g[(-1)])
            self.acc_drag_array = np.append(self.acc_drag_array, self.acc_drag_g[(-1)])
            t_min = np.concatenate((t_min, t_min_c), axis=0)
            h_km = np.concatenate((h_km, h_km_c), axis=0)
            v_kms = np.concatenate((v_kms, v_kms_c), axis=0)
            phi_deg = np.concatenate((phi_deg, phi_deg_c), axis=0)
            psi_deg = np.concatenate((psi_deg, psi_deg_c), axis=0)
            theta_deg = np.concatenate((theta_deg, theta_deg_c), axis=0)
            gamma_deg = np.concatenate((gamma_deg, gamma_deg_c), axis=0)
            drange_km = np.concatenate((drange_km, drange_km_c), axis=0)
            acc_net_g = np.concatenate((acc_net_g, acc_net_g_c), axis=0)
            acc_drag_g = np.concatenate((acc_drag_g, acc_drag_g_c), axis=0)
            dyn_pres_atm = np.concatenate((dyn_pres_atm, dyn_pres_atm_c), axis=0)
            stag_pres_atm = np.concatenate((stag_pres_atm, stag_pres_atm_c), axis=0)
            q_stag_total = np.concatenate((q_stag_total, q_stag_total_c), axis=0)
            heatload = np.concatenate((heatload, heatload_c), axis=0)
            self.acc_step_array = np.append(self.acc_step_array, acc_net_g[(-1)])
            density_mes = 2 * self.mass * acc_drag_g[(-1)] * self.planetObj.EARTHG / (self.CD * self.A * (0.5 * (vi + v_kms[(-1)] * 1000.0)) ** 2.0)
            self.density_mes_array = np.append(self.density_mes_array, density_mes)
            if hdoti > self.hdot_threshold:
                if customFlag == 0:
                    self.density_mes_int, self.minAlt = self.createDensityMeasuredFunction(self.h_step_array, self.density_mes_array, self.lowAlt_km, self.numPoints_lowAlt)
                    customFlag = 1.0
            elif hdoti > self.hdot_threshold:
                terminal_apoapsis_km = self.predictApoapsisAltitudeKm_withLiftUp(h_km[(-1)], theta_deg[(-1)], phi_deg[(-1)], v_kms[(-1)], gamma_deg[(-1)], psi_deg[(-1)], drange_km[(-1)], heatload[(-1)], maxTimeSecs, dt, 0.0, self.density_mes_int)
            else:
                terminal_apoapsis_km = 0.0
            counter += 1
            h_current_km = h_km[(-1)]
            v_current_kms = v_kms[(-1)]
            if terminal_apoapsis_km > 0:
                if terminal_apoapsis_km < self.target_apo_km:
                    break
            if abs(terminal_apoapsis_km - self.target_apo_km) < self.target_apo_km_tol:
                break
            if h_current_km > self.planetObj.h_skip / 1000 - 2.0:
                break

        self.t_min_eg = t_min
        self.h_km_eg = h_km
        self.v_kms_eg = v_kms
        self.theta_deg_eg = theta_deg
        self.phi_deg_eg = phi_deg
        self.psi_deg_eg = psi_deg
        self.gamma_deg_eg = gamma_deg
        self.drange_km_eg = drange_km
        self.acc_net_g_eg = acc_net_g
        self.dyn_pres_atm_eg = dyn_pres_atm
        self.stag_pres_atm_eg = stag_pres_atm
        self.q_stag_total_eg = q_stag_total
        self.heatload_eg = heatload

    def propogateExitPhase(self, timeStep, dt, maxTimeSecs):
        """
                Implements the exit phase of the guidance scheme (full lift-up).

                Parameters
                --------
                timeStep : float
                        Guidance cycle time, seconds
                dt : float
                        Solver max. time step, seconds
                maxTimeSecs : float
                        max. time for propogation, seconds

                """
        self.t_switch = self.t_min_eg[(-1)]
        self.h_switch = self.h_km_eg[(-1)]
        self.v_switch = self.v_kms_eg[(-1)]
        self.p_switch = self.delta_deg_array[(-1)]
        t_min = self.t_min_eg
        h_km = self.h_km_eg
        v_kms = self.v_kms_eg
        theta_deg = self.theta_deg_eg
        phi_deg = self.phi_deg_eg
        psi_deg = self.psi_deg_eg
        gamma_deg = self.gamma_deg_eg
        drange_km = self.drange_km_eg
        acc_net_g = self.acc_net_g_eg
        dyn_pres_atm = self.dyn_pres_atm_eg
        stag_pres_atm = self.stag_pres_atm_eg
        q_stag_total = self.q_stag_total_eg
        heatload = self.heatload_eg
        h_current_km = h_km[(-1)]
        t_current_min = t_min[(-1)]
        h_skip_km = self.planetObj.h_skip / 1000.0
        hdot_refi = self.hdot_array[(-1)]
        Ji = self.heatload_eg[(-1)]
        Delta_deg_ini = self.p_switch
        while h_current_km < h_skip_km:
            h0_km = h_km[(-1)]
            theta0_deg = theta_deg[(-1)]
            phi0_deg = phi_deg[(-1)]
            v0_kms = v_kms[(-1)]
            psi0_deg = psi_deg[(-1)]
            gamma0_deg = gamma_deg[(-1)]
            drange0_km = drange_km[(-1)]
            h0 = h0_km * 1000.0
            theta0 = theta0_deg * np.pi / 180.0
            phi0 = phi0_deg * np.pi / 180.0
            v0 = v0_kms * 1000.0
            psi0 = psi0_deg * np.pi / 180.0
            gamma0 = gamma0_deg * np.pi / 180.0
            hi = h0
            ri = h0 + self.planetObj.RP
            vi = v0
            qi = 0.5 * self.planetObj.density(hi) * vi ** 2.0
            gammai = gamma0
            hdoti = vi * np.sin(gammai)
            DeltaCMD_deg_command = 0.0
            DeltaCMD_deg, Delta_deg_ini = self.psuedoController(DeltaCMD_deg_command, Delta_deg_ini, timeStep)
            self.setInitialState(h0_km, theta0_deg, phi0_deg, v0_kms, psi0_deg, gamma0_deg, drange0_km, Ji)
            self.propogateEntry(timeStep, dt, DeltaCMD_deg)
            t_min_c = self.t_minc
            h_km_c = self.h_kmc
            v_kms_c = self.v_kmsc
            phi_deg_c = self.phi_degc
            psi_deg_c = self.psi_degc
            theta_deg_c = self.theta_degc
            gamma_deg_c = self.gamma_degc
            drange_km_c = self.drange_kmc
            acc_net_g_c = self.acc_net_g
            dyn_pres_atm_c = self.dyn_pres_atm
            stag_pres_atm_c = self.stag_pres_atm
            q_stag_total_c = self.q_stag_total
            heatload_c = self.heatload
            acc_drag_g_c = self.acc_drag_g
            t_min_c = t_min_c + t_min[(-1)]
            self.t_step_array = np.append(self.t_step_array, t_min[(-1)])
            self.delta_deg_array = np.append(self.delta_deg_array, DeltaCMD_deg)
            self.hdot_array = np.append(self.hdot_array, hdoti)
            self.hdotref_array = np.append(self.hdotref_array, hdot_refi)
            self.hddoti = (self.hdot_array[(-1)] - self.hdot_array[(-2)]) / (self.t_step_array[(-1)] * 60.0 - self.t_step_array[(-2)] * 60.0)
            self.hddot_array = np.append(self.hddot_array, self.hddoti)
            t_min = np.concatenate((t_min, t_min_c), axis=0)
            h_km = np.concatenate((h_km, h_km_c), axis=0)
            v_kms = np.concatenate((v_kms, v_kms_c), axis=0)
            phi_deg = np.concatenate((phi_deg, phi_deg_c), axis=0)
            psi_deg = np.concatenate((psi_deg, psi_deg_c), axis=0)
            theta_deg = np.concatenate((theta_deg, theta_deg_c), axis=0)
            gamma_deg = np.concatenate((gamma_deg, gamma_deg_c), axis=0)
            drange_km = np.concatenate((drange_km, drange_km_c), axis=0)
            acc_net_g = np.concatenate((acc_net_g, acc_net_g_c), axis=0)
            dyn_pres_atm = np.concatenate((dyn_pres_atm, dyn_pres_atm_c), axis=0)
            stag_pres_atm = np.concatenate((stag_pres_atm, stag_pres_atm_c), axis=0)
            q_stag_total = np.concatenate((q_stag_total, q_stag_total_c), axis=0)
            heatload = np.concatenate((heatload, heatload_c), axis=0)
            terminal_apoapsis_km = self.compute_ApoapsisAltitudeKm(self.planetObj.RP + h_km[(-1)] * 1000.0, v_kms[(-1)] * 1000.0, gamma_deg[(-1)] * np.pi / 180.0, theta_deg[(-1)] * np.pi / 180.0, phi_deg[(-1)] * np.pi / 180.0, psi_deg[(-1)] * np.pi / 180.0)
            if hi > self.planetObj.h_skip - 10000.0:
                break
            h_current_km = h_km[(-1)]
            t_current_min = t_min[(-1)]

        self.t_min_full = t_min
        self.h_km_full = h_km
        self.v_kms_full = v_kms
        self.theta_deg_full = theta_deg
        self.phi_deg_full = phi_deg
        self.psi_deg_full = psi_deg
        self.gamma_deg_full = gamma_deg
        self.drange_km_full = drange_km
        self.acc_net_g_full = acc_net_g
        self.dyn_pres_atm_full = dyn_pres_atm
        self.stag_pres_atm_full = stag_pres_atm
        self.q_stag_total_full = q_stag_total
        self.heatload_full = heatload
        self.terminal_apoapsis = self.compute_ApoapsisAltitudeKm(self.planetObj.RP + h_km[(-1)] * 1000.0, v_kms[(-1)] * 1000.0, gamma_deg[(-1)] * np.pi / 180.0, theta_deg[(-1)] * np.pi / 180.0, phi_deg[(-1)] * np.pi / 180.0, psi_deg[(-1)] * np.pi / 180.0)
        self.terminal_periapsis = self.compute_PeriapsisAltitudeKm(self.planetObj.RP + h_km[(-1)] * 1000.0, v_kms[(-1)] * 1000.0, gamma_deg[(-1)] * np.pi / 180.0, theta_deg[(-1)] * np.pi / 180.0, phi_deg[(-1)] * np.pi / 180.0, psi_deg[(-1)] * np.pi / 180.0)
        self.apoapsis_perc_error = (self.terminal_apoapsis - self.target_apo_km) * 100.0 / self.target_apo_km
        self.periapsis_raise_DV = self.compute_periapsis_raise_DV(self.terminal_periapsis, self.terminal_apoapsis, self.target_peri_km)
        self.apoapsis_raise_DV = self.compute_apoapsis_raise_DV(self.target_peri_km, self.terminal_apoapsis, self.target_apo_km)

    def propogateGuidedEntry(self, timeStep, dt, maxTimeSecs):
        """
                Implements the full guidance scheme (eq. glide + exit phase)

                Parameters
                --------
                timeStep : float
                        Guidance cycle time, seconds
                dt : float
                        Solver max. time step, seconds
                maxTimeSecs : float
                        max. time for propogation, seconds

                """
        self.propogateEquilibriumGlide(timeStep, dt, maxTimeSecs)
        self.propogateExitPhase(timeStep, dt, maxTimeSecs)

    def setupMonteCarloSimulation(self, NPOS, NMONTE, atmfiles, heightCol, densLowCol, densAvgCol, densHighCol, densTotalCol, heightInKmFlag, nominalEFPA, EFPA_1sigma_value, nominalLD, LD_1sigma_value, timeStep, dt, maxTimeSecs):
        """
                Set the Monte Carlo simulation parameters.

                Parameters
                --------
                NPOS : int
                        NPOS value from GRAM model output 
                        is the number of data points (altitude) in each atm. profile
                NMONTE : int
                        NMONTE is the number of Monte Carlo atm profiles
                        from GRAM model output
                atmfiles : str
                        location of atmospheric files used in Monte Carlo simulation

                """
        self.NPOS = NPOS
        self.NMONTE = NMONTE
        self.atmfiles = atmfiles
        self.heightCol = heightCol
        self.densLowCol = densLowCol
        self.densAvgCol = densAvgCol
        self.densHighCol = densHighCol
        self.densTotalCol = densTotalCol
        self.heightInKmFlag = heightInKmFlag
        self.nominalEFPA = nominalEFPA
        self.EFPA_1sigma_value = EFPA_1sigma_value
        self.nominalLD = nominalLD
        self.LD_1sigma_value = LD_1sigma_value
        self.vehicleCopy = copy.deepcopy(self)
        self.timeStep = timeStep
        self.dt = dt
        self.maxTimeSecs = maxTimeSecs

    def runMonteCarlo(self, N, mainFolder):
        terminal_apoapsis_arr = np.zeros(N)
        terminal_periapsis_arr = np.zeros(N)
        periapsis_raise_DV_arr = np.zeros(N)
        apoapsis_raise_DV_arr = np.zeros(N)
        acc_net_g_max_arr = np.zeros(N)
        q_stag_max_arr = np.zeros(N)
        heatload_max_arr = np.zeros(N)
        h0_km = self.vehicleCopy.h0_km_ref
        theta0_deg = self.vehicleCopy.theta0_deg_ref
        phi0_deg = self.vehicleCopy.phi0_deg_ref
        v0_kms = self.vehicleCopy.v0_kms_ref
        psi0_deg = self.vehicleCopy.psi0_deg_ref
        drange0_km = self.vehicleCopy.drange0_km_ref
        heatLoad0 = self.vehicleCopy.heatLoad0_ref
        os.makedirs(mainFolder)
        for i in range(N):
            selected_atmfile = rd.choice(self.atmfiles)
            selected_profile = rd.randint(1, self.NMONTE)
            selected_efpa = np.random.normal(self.nominalEFPA, self.EFPA_1sigma_value)
            selected_atmSigma = np.random.normal(0, 1)
            selected_LD = np.random.normal(self.nominalLD, self.LD_1sigma_value)
            ATM_height, ATM_density_low, ATM_density_avg, ATM_density_high, ATM_density_pert = self.planetObj.loadMonteCarloDensityFile2(selected_atmfile, self.heightCol, self.densLowCol, self.densAvgCol, self.densHighCol, self.densTotalCol, self.heightInKmFlag)
            self.planetObj.density_int = self.planetObj.loadAtmosphereModel5(ATM_height, ATM_density_low, ATM_density_avg, ATM_density_high, ATM_density_pert, selected_atmSigma, self.NPOS, selected_profile)
            self.setInitialState(h0_km, theta0_deg, phi0_deg, v0_kms, psi0_deg, selected_efpa, drange0_km, heatLoad0)
            self.propogateGuidedEntry(self.timeStep, self.dt, self.maxTimeSecs)
            terminal_apoapsis = self.terminal_apoapsis
            apoapsis_error = self.apoapsis_perc_error
            terminal_periapsis = self.terminal_periapsis
            periapsis_raise_DV = self.periapsis_raise_DV
            apoapsis_raise_DV = self.apoapsis_raise_DV
            terminal_apoapsis_arr[i] = self.terminal_apoapsis
            terminal_periapsis_arr[i] = self.terminal_periapsis
            periapsis_raise_DV_arr[i] = self.periapsis_raise_DV
            apoapsis_raise_DV_arr[i] = self.apoapsis_raise_DV
            acc_net_g_max_arr[i] = max(self.acc_net_g_full)
            q_stag_max_arr[i] = max(self.q_stag_total_full)
            heatload_max_arr[i] = max(self.heatload_full)
            print('BATCH :' + str(mainFolder) + ', RUN #: ' + str(i + 1) + ', PROF: ' + str(selected_atmfile) + ', SAMPLE #: ' + str(selected_profile) + ', EFPA: ' + str('{:.2f}'.format(selected_efpa, 2)) + ', SIGMA: ' + str('{:.2f}'.format(selected_atmSigma, 2)) + ', LD: ' + str('{:.2f}'.format(selected_LD, 2)) + ', APO : ' + str('{:.2f}'.format(terminal_apoapsis, 2)))
            os.makedirs(mainFolder + '/' + '#' + str(i + 1))
            np.savetxt((mainFolder + '/' + '#' + str(i + 1) + '/' + 'atmfile.txt'), (np.array([selected_atmfile])), fmt='%s')
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'profile.txt', np.array([selected_profile]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'efpa.txt', np.array([selected_efpa]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'atmSigma.txt', np.array([selected_atmSigma]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'LD.txt', np.array([selected_LD]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'terminal_apoapsis.txt', np.array([terminal_apoapsis]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'apoapsis_error.txt', np.array([apoapsis_error]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'terminal_periapsis.txt', np.array([terminal_periapsis]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'periapsis_raise_DV.txt', np.array([periapsis_raise_DV]))
            np.savetxt(mainFolder + '/' + '#' + str(i + 1) + '/' + 'apoapsis_raise_DV.txt', np.array([apoapsis_raise_DV]))
            np.savetxt(mainFolder + '/' + 'terminal_apoapsis_arr.txt', terminal_apoapsis_arr)
            np.savetxt(mainFolder + '/' + 'terminal_periapsis_arr.txt', terminal_periapsis_arr)
            np.savetxt(mainFolder + '/' + 'periapsis_raise_DV_arr.txt', periapsis_raise_DV_arr)
            np.savetxt(mainFolder + '/' + 'apoapsis_raise_DV_arr.txt', apoapsis_raise_DV_arr)
            np.savetxt(mainFolder + '/' + 'acc_net_g_max_arr.txt', acc_net_g_max_arr)
            np.savetxt(mainFolder + '/' + 'q_stag_max_arr.txt', q_stag_max_arr)
            np.savetxt(mainFolder + '/' + 'heatload_max_arr.txt', heatload_max_arr)