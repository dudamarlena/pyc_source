# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kgulliks/.PythonModules/TelluricFitter/src/MakeModel.py
# Compiled at: 2015-06-08 17:49:39
"""

    This file provides the MakeModel class. It is what directly interfaces
      with LBLRTM to make the telluric model. You can call this function 
      from the bash shell using the command 'python MakeModel.py' to generate
      a model transmission spectrum. The input settings for the model can be
      adjusted at the bottom of this file (after the line that reads
      'if __name__ == "__main__":')

    This file is part of the TelFit program.

    TelFit is free software: you can redistribute it and/or modify
    it under the terms of the MIT license.

    TelFit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    You should have received a copy of the MIT license
    along with TelFit.  If not, see <http://opensource.org/licenses/MIT>.

"""
import sys, subprocess, os
from collections import defaultdict
import struct, warnings, time, FittingUtilities, copy, scipy.interpolate, lockfile, numpy as np
from astropy import units
import DataStructures, MakeTape5
DEFAULT_TELLURICMODELING = ('{}/.TelFit/').format(os.environ['HOME'])
MoleculeNumbers = {1: 'H2O', 2: 'CO2', 
   3: 'O3', 
   4: 'N2O', 
   5: 'CO', 
   6: 'CH4', 
   7: 'O2', 
   8: 'NO', 
   9: 'SO2', 
   10: 'NO2', 
   11: 'NH3', 
   12: 'HNO3', 
   13: 'OH', 
   14: 'HF', 
   15: 'HCl', 
   16: 'HBr', 
   17: 'HI', 
   18: 'ClO', 
   19: 'OCS', 
   20: 'H2CO', 
   21: 'HOCl', 
   22: 'N2', 
   23: 'HCN', 
   24: 'CH3Cl', 
   25: 'H2O2', 
   26: 'C2H2', 
   27: 'C2H6', 
   28: 'PH3', 
   29: 'COF2', 
   30: 'SF6', 
   31: 'H2S', 
   32: 'HCOOH', 
   33: 'HO2', 
   34: 'O', 
   35: 'ClONO2', 
   36: 'NO+', 
   37: 'HOBr', 
   38: 'C2H4', 
   39: 'CH3OH'}

class ModelerException(Exception):
    pass


class Modeler():

    def __init__(self, debug=False, TelluricModelingDirRoot=DEFAULT_TELLURICMODELING, nmolecules=12):
        """
        Initialize a modeler instance

        :param debug: If True, it will print some extra information to the screen when making telluric models.
        :param TelluricModelingDirRoot: Root directory to do the actual telluric modeling. The default
                                        installation puts this in ~/.TelFit/
        :param nmolecules: The number of molecules to include in the telluric model. Probably don't change
                           this, and definitely don't increase it!
        :return: None
        """
        Atmosphere = defaultdict(list)
        indices = {}
        self.debug = debug
        if not TelluricModelingDirRoot.endswith('/'):
            TelluricModelingDirRoot = TelluricModelingDirRoot + '/'
        if 'rundir1' not in os.listdir(TelluricModelingDirRoot):
            try:
                TelluricModelingDirRoot = os.environ['TELLURICMODELING']
            except KeyError:
                raise ModelerException(('Directory {} is not configured correctly or does not exist, and the environment variable TELLURICMODELING is not set!').format(TelluricModelingDirRoot))

        self.TelluricModelingDirRoot = TelluricModelingDirRoot
        self.FindWorkingDirectory()
        TelluricModelingDir = self.TelluricModelingDir
        ModelDir = self.ModelDir
        if debug:
            print 'Generating new atmosphere profile'
        filename = TelluricModelingDir + 'MIPAS_atmosphere_profile'
        infile = open(filename)
        lines = infile.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('*') and 'END' not in line:
                if line.find('HGT') > 0 and line.find('[') > 0:
                    numlevels = int(lines[(i - 1)].split()[0])
                    indices['Z'] = i
                elif line.find('PRE') > 0 and line.find('[') > 0:
                    indices['P'] = i
                elif line.find('TEM') > 0 and line.find('[') > 0:
                    indices['T'] = i
                else:
                    molecule = line.split('*')[(-1)].split()[0]
                    indices[molecule] = i

        infile.close()
        levelsperline = 5.0
        linespersection = int(numlevels / levelsperline + 0.9)
        layers = []
        for j in range(indices['Z'] + 1, indices['Z'] + 1 + linespersection):
            line = lines[j]
            levels = line.split()
            [ layers.append(float(level)) for level in levels ]

        for j in range(linespersection):
            line = lines[(j + indices['P'] + 1)]
            levels = line.split()
            for i, level in enumerate(levels):
                Atmosphere[layers[int(j * levelsperline + i)]].append(float(level))

        for j in range(linespersection):
            line = lines[(j + indices['T'] + 1)]
            levels = line.split()
            for i, level in enumerate(levels):
                Atmosphere[layers[int(j * levelsperline + i)]].append(float(level))
                Atmosphere[layers[int(j * levelsperline + i)]].append([])

        for k in range(1, nmolecules + 1):
            for j in range(linespersection):
                line = lines[(j + indices[MoleculeNumbers[k]] + 1)]
                levels = line.split()
                for i, level in enumerate(levels):
                    Atmosphere[layers[int(j * levelsperline + i)]][2].append(float(level))

        self.Atmosphere = Atmosphere
        self.layers = layers
        self.nmolecules = nmolecules
        self.Cleanup()

    def EditProfile(self, profilename, profile_height, profile_value):
        """
        This function will take a np array as a profile, and stitch it into the
          MIPAS atmosphere profile read in in __init__

        :param profilename: A string with the name of the profile to edit.
                       Should be either 'pressure', 'temperature', or
                       one of the molecules given in the MakeModel.MoleculeNumbers
                       dictionary
        :param profile_height: A np array with the height in the atmosphere (in km)
        :param profile_value: A np array with the value of the profile parameter at
                              each height given in profile_height.
        :return: None

        """
        profilenum = -1
        if profilename.lower() == 'pressure':
            profilenum = 0
        else:
            if profilename.lower() == 'temperature':
                profilenum = 1
            else:
                profilenum = 2
                molnum = -1
                for n in MoleculeNumbers:
                    if MoleculeNumbers[n] == profilename:
                        molnum = n - 1

                if molnum < 0:
                    print 'Error! Profilename given in Modeler.EditProfile is invalid!'
                    print 'You gave: ', profilename
                    print 'Valid options are: '
                    for n in MoleculeNumbers:
                        print MoleculeNumbers[n]

                    raise ValueError
                if profilenum < 0:
                    print 'Error! Profilename given in Modeler.EditProfile is invalid!'
                    print 'You gave: ', profilename
                    print "Valid options are either a molecule name, 'pressure', or 'temperature'"
                    raise ValueError
                Atmosphere = self.Atmosphere
                layers = np.array(self.layers)
                mipas = []
                for layer in layers:
                    if profilenum < 2:
                        mipas.append(Atmosphere[layer][profilenum])
                    else:
                        mipas.append(Atmosphere[layer][profilenum][molnum])

                while abs(profile_value[(-1)]) < 1:
                    profile_height = profile_height[:-1]
                    profile_value = profile_value[:-1]

            profile_fcn = scipy.interpolate.interp1d(profile_height, profile_value, kind='linear')
            left = np.searchsorted(layers, profile_height[0])
            right = np.searchsorted(layers, profile_height[(-1)]) - 1
            newprofile = list(mipas)
            newprofile[:left] -= (mipas[left] - profile_fcn(layers[left])) * np.exp(-(layers[left] - layers[:left]))
            newprofile[right:] -= (mipas[right] - profile_fcn(layers[right])) * np.exp(-(layers[right:] - layers[right]))
            newprofile[left:right] = profile_fcn(layers[left:right])
            for i, layer in enumerate(layers):
                if profilenum < 2:
                    Atmosphere[layer][profilenum] = newprofile[i]
                else:
                    Atmosphere[layer][profilenum][molnum] = newprofile[i]

        self.Atmosphere = Atmosphere

    def Cleanup(self):
        """
          Release the lock on the directory. This can be called on its own, but
          should never need to be.
        """
        lock = self.lock
        try:
            lock.release()
        except lockfile.NotLocked:
            warnings.warn('The model directory was somehow unlocked prematurely!')

    def FindWorkingDirectory(self):
        """
        Find a run directory to work in. This is necessary so that you
          can run several instances of MakeModel (or TelFit) at once.
          Should not need to be called on directly by the user.
        """
        TelluricModelingDirRoot = self.TelluricModelingDirRoot
        found = False
        possible_rundirs = [ d for d in os.listdir(self.TelluricModelingDirRoot) if d.startswith('rundir') and '.' not in d
                           ]
        while not found:
            for test in possible_rundirs:
                test = '%s%s' % (TelluricModelingDirRoot, test)
                if not test.endswith('/'):
                    test = test + '/'
                lock = lockfile.FileLock(test)
                if not lock.is_locked():
                    TelluricModelingDir = test
                    ModelDir = '%sOutputModels/' % TelluricModelingDir
                    lock.acquire()
                    found = True
                    break

            if not found:
                print 'Un-locked directory not found! Waiting 10 seconds...'
                time.sleep(10)

        if self.debug:
            print 'Telluric Modeling Directory: %s' % TelluricModelingDir
            print 'Model Directory: %s' % ModelDir
        self.TelluricModelingDir = TelluricModelingDir
        self.ModelDir = ModelDir
        self.lock = lock

    def MakeModel(self, pressure=795.0, temperature=283.0, lowfreq=4000, highfreq=4600, angle=45.0, humidity=50.0, co2=368.5, o3=0.039, n2o=0.32, co=0.14, ch4=1.8, o2=210000.0, no=1.1e-19, so2=0.0001, no2=0.0001, nh3=0.0001, hno3=0.00056, lat=30.6, alt=2.1, wavegrid=None, resolution=None, save=False, libfile=None, vac2air=True):
        """
        Here is the important function! All of the variables have default values,
          which you will want to override for any realistic use.

        :param pressure:       Pressure at telescope altitude (hPa)
        :param temperature:    Temperature at telescope altitude (Kelvin)
        :param lowfreq:        The starting wavenumber (cm^-1)
        :param highfreq:       The ending wavenumber (cm^-1)
        :param angle:          The zenith distance of the telescope (degrees). This is related to
                               the airmass (z) through z = sec(angle)
        :param humidity:       Percent relative humidity at the telescope altitude.
        :param co2:            Mixing ratio of this molecule (parts per million by volumne)
        :param o3:             Mixing ratio of this molecule (parts per million by volumne)
        :param n2o:            Mixing ratio of this molecule (parts per million by volumne)
        :param co:             Mixing ratio of this molecule (parts per million by volumne)
        :param ch4:            Mixing ratio of this molecule (parts per million by volumne)
        :param o2:             Mixing ratio of this molecule (parts per million by volumne)
        :param no:             Mixing ratio of this molecule (parts per million by volumne)
        :param so2:            Mixing ratio of this molecule (parts per million by volumne)
        :param no2:            Mixing ratio of this molecule (parts per million by volumne)
        :param nh3:            Mixing ratio of this molecule (parts per million by volumne)
        :param hno3:           Mixing ratio of this molecule (parts per million by volumne)
        :param lat:            The latitude of the observatory (degrees)
        :param alt:            The altitude of the observatory above sea level (km)
        :param wavegrid:       If given, the model will be resampled to this grid.
                               Should be a 1D np array
        :param resolution:     If given, it will reduce the resolution by convolving
                               with a gaussian of appropriate width. Should be a float
                               with R=lam/dlam
        :param save:           If true, the generated model is saved. The filename will be
                               printed to the screen.
        :param libfile:        Useful if generating a telluric library. The filename of the
                               saved file will be written to this filename. Should be a string
                               variable. Ignored if save==False
        :param vac2air:        If True (default), it converts the wavelengths from vacuum to air
        :return:               DataStructures.xypoint instance with the telluric model. The x-axis
                               is in nanometers and the y-axis is in fractional transmission.
        """
        self.FindWorkingDirectory()
        TelluricModelingDir = self.TelluricModelingDir
        debug = self.debug
        lock = self.lock
        layers = np.array(self.layers)
        ModelDir = self.ModelDir
        Atmosphere = copy.deepcopy(self.Atmosphere)
        h2o = humidity_to_ppmv(humidity, temperature, pressure)
        keys = sorted(Atmosphere.keys())
        lower = max(0, np.searchsorted(keys, alt) - 1)
        upper = min(lower + 1, len(keys) - 1)
        if lower == upper:
            raise ZeroDivisionError('Observatory altitude of %g results in the surrounding layers being the same!' % alt)
        scale_values = list(Atmosphere[lower])
        scale_values[2] = list(Atmosphere[lower][2])
        scale_values[0] = (Atmosphere[upper][0] - Atmosphere[lower][0]) / (keys[upper] - keys[lower]) * (alt - keys[lower]) + Atmosphere[lower][0]
        scale_values[1] = (Atmosphere[upper][1] - Atmosphere[lower][1]) / (keys[upper] - keys[lower]) * (alt - keys[lower]) + Atmosphere[lower][1]
        for mol in range(len(scale_values[2])):
            scale_values[2][mol] = (Atmosphere[upper][2][mol] - Atmosphere[lower][2][mol]) / (keys[upper] - keys[lower]) * (alt - keys[lower]) + Atmosphere[lower][2][mol]

        pressure_scalefactor = (scale_values[0] - pressure) * np.exp(-(layers - alt) ** 2 / (2.0 * 100.0))
        temperature_scalefactor = (scale_values[1] - temperature) * np.exp(-(layers - alt) ** 2 / (2.0 * 100.0))
        for i, layer in enumerate(layers):
            Atmosphere[layer][0] *= pressure / scale_values[0]
            Atmosphere[layer][1] -= temperature_scalefactor[i]
            Atmosphere[layer][2][0] *= h2o / scale_values[2][0]
            Atmosphere[layer][2][1] *= co2 / scale_values[2][1]
            Atmosphere[layer][2][2] *= o3 / scale_values[2][2]
            Atmosphere[layer][2][3] *= n2o / scale_values[2][3]
            Atmosphere[layer][2][4] *= co / scale_values[2][4]
            Atmosphere[layer][2][5] *= ch4 / scale_values[2][5]
            Atmosphere[layer][2][6] *= o2 / scale_values[2][6]
            Atmosphere[layer][2][7] *= no / scale_values[2][7]
            Atmosphere[layer][2][8] *= so2 / scale_values[2][8]
            Atmosphere[layer][2][9] *= no2 / scale_values[2][9]
            Atmosphere[layer][2][10] *= nh3 / scale_values[2][10]
            Atmosphere[layer][2][11] *= hno3 / scale_values[2][11]

        parameters = MakeTape5.ReadParFile(parameterfile=TelluricModelingDir + 'ParameterFile')
        parameters[48] = '%.1f' % lat
        parameters[49] = '%.1f' % alt
        parameters[51] = '%.5f' % angle
        parameters[17] = lowfreq
        freq, transmission = np.array([]), np.array([])
        maxdiff = 1999.9
        if highfreq - lowfreq > maxdiff:
            while lowfreq + maxdiff <= highfreq:
                parameters[18] = lowfreq + maxdiff
                MakeTape5.WriteTape5(parameters, output=TelluricModelingDir + 'TAPE5', atmosphere=Atmosphere)
                cmd = 'cd ' + TelluricModelingDir + ';sh runlblrtm_v3.sh'
                try:
                    command = subprocess.check_call(cmd, shell=True)
                except subprocess.CalledProcessError:
                    print "Error: Command '%s' failed in directory %s" % (cmd, TelluricModelingDir)
                    sys.exit()

                freq, transmission = self.ReadTAPE12(TelluricModelingDir, appendto=(freq, transmission))
                lowfreq = lowfreq + 2000.00001
                parameters[17] = lowfreq

        parameters[18] = highfreq
        MakeTape5.WriteTape5(parameters, output=TelluricModelingDir + 'TAPE5', atmosphere=Atmosphere)
        cmd = 'cd ' + TelluricModelingDir + ';sh runlblrtm_v3.sh'
        try:
            command = subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError:
            print "Error: Command '%s' failed in directory %s" % (cmd, TelluricModelingDir)
            sys.exit()

        freq, transmission = self.ReadTAPE12(TelluricModelingDir, appendto=(freq, transmission))
        wavelength = units.cm.to(units.nm) / freq
        if vac2air:
            wave_A = wavelength * units.nm.to(units.angstrom)
            n = 1.0002735182 + 131.4182 / wave_A ** 2 + 276249000.0 / wave_A ** 4
            wavelength /= n
        if save:
            model_name = ModelDir + 'transmission' + '-%.2f' % pressure + '-%.2f' % temperature + '-%.1f' % humidity + '-%.1f' % angle + '-%.2f' % co2 + '-%.2f' % (o3 * 100) + '-%.2f' % ch4 + '-%.2f' % (co * 10)
            print 'All done! Output Transmission spectrum is located in the file below:'
            print model_name
            np.savetxt(model_name, np.transpose((wavelength[::-1], transmission[::-1])), fmt='%.8g')
            if libfile != None:
                infile = open(libfile, 'a')
                infile.write(model_name + '\n')
                infile.close()
        self.Cleanup()
        if wavegrid != None:
            model = DataStructures.xypoint(x=wavelength[::-1], y=transmission[::-1])
            return FittingUtilities.RebinData(model, wavegrid)
        else:
            return DataStructures.xypoint(x=wavelength[::-1], y=transmission[::-1])

    def ReadTAPE12(self, directory, filename='TAPE12_ex', appendto=None):
        """
        Here is a function to read in the binary output of lblrtm, and convert
          it into arrays of frequency and transmission.
        Warning! Some values are hard-coded in for single precision calculations.
          You MUST compile lblrtm as single precision or this won't work!
        Not meant to be called directly by the user.
        """
        debug = self.debug
        if not directory.endswith('/'):
            directory = directory + '/'
        infile = open('%s%s' % (directory, filename), 'rb')
        content = infile.read()
        infile.close()
        offset = 1068
        size = struct.calcsize('=ddfl')
        pv1, pv2, pdv, numpoints = struct.unpack('=ddfl', content[offset:offset + size])
        v1 = pv1
        v2 = pv2
        dv = pdv
        if debug:
            print 'info: ', pv1, pv2, pdv, numpoints
        npts = numpoints
        spectrum = []
        while numpoints > 0:
            offset += size + struct.calcsize('=4f')
            size = struct.calcsize('=%if' % numpoints)
            temp1 = struct.unpack('=%if' % numpoints, content[offset:offset + size])
            offset += size
            temp2 = struct.unpack('=%if' % numpoints, content[offset:offset + size])
            npts += numpoints
            junk = [ spectrum.append(temp2[i]) for i in range(numpoints) ]
            offset += size + 8
            size = struct.calcsize('=ddfl')
            if len(content) > offset + size:
                pv1, pv2, pdv, numpoints = struct.unpack('=ddfl', content[offset:offset + size])
                v2 = pv2
            else:
                break

        v = np.arange(v1, v2, dv)
        spectrum = np.array(spectrum)
        if v.size < spectrum.size:
            v = np.r_[(v, v2 + dv)]
        if debug:
            print 'v, spec size: ', v.size, spectrum.size
        if appendto != None and appendto[0].size > 0:
            old_v, old_spectrum = appendto[0], appendto[1]
            last_v = old_v[(-1)]
            firstindex = np.searchsorted(v, last_v)
            v = np.r_[(old_v, v[firstindex:])]
            spectrum = np.r_[(old_spectrum, spectrum[firstindex:])]
        return (v, spectrum)


def VaporPressure(T):
    """
      This function uses equations and constants from
      http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
      to determine the vapor pressure at the given temperature

      T must be a float with the temperature (or dew point) in Kelvin
    """
    c1, c2, c3, c4, c5, c6 = (-7.85951783, 1.84408259, -11.7866497, 22.6807411, -15.9618719,
                              1.8022502)
    a0, a1 = (-13.928169, 34.707823)
    if T > 273.15:
        theta = 1.0 - T / 647.096
        Pw = 220640.0 * np.exp(1.0 / (1.0 - theta) * (c1 * theta + c2 * theta ** 1.5 + c3 * theta ** 3 + c4 * theta ** 3.5 + c5 * theta ** 4 + c6 * theta ** 7.5))
    elif T > 173.15:
        theta = T / 273.16
        Pw = 6.11657 * np.exp(a0 * (1.0 - theta ** (-1.5)) + a1 * (1.0 - theta ** (-1.25)))
    else:
        Pw = 0.0
    return Pw


def humidity_to_ppmv(RH, T, P):
    """
    Given the relative humidity, temperature, and pressure, return the ppmv water concentration
    """
    Psat = VaporPressure(T)
    Pw = Psat * RH / 100.0
    h2o = Pw / (P - Pw) * 1000000.0
    return h2o


def ppmv_to_humidity(h2o, T, P):
    """
    Given the ppmv water concentration, temperature, and pressure, return the relative humidity
    """
    Psat = VaporPressure(T)
    RH = 100.0 * h2o * P / (Psat * (1000000.0 + h2o))
    return RH


if __name__ == '__main__':
    pressure = 796.22906
    temperature = 270.4
    humidity = 40.0
    angle = 40.8
    co2 = 368.5
    o3 = 0.039
    ch4 = 4.0
    co = 0.15
    o2 = 220000.0
    lowwave = 620
    highwave = 650
    lowfreq = 10000000.0 / highwave
    highfreq = 10000000.0 / lowwave
    modeler = Modeler(debug=False)
    modeler.MakeModel(pressure=pressure, temperature=temperature, humidity=humidity, lowfreq=lowfreq, highfreq=highfreq, angle=angle, o2=o2, alt=2.1, save=True)