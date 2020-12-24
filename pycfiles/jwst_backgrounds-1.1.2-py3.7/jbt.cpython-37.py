# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/jwst_backgrounds/jbt.py
# Compiled at: 2020-03-25 13:57:38
# Size of source mod 2**32: 17738 bytes
"""
This is a module to predict the background levels for JWST observations, 
for use in JWST proposal planning. 

It accesses a precompiled background cache prepared by STScI, to do the following:
- Plot the background versus calendar day.
- Compute the number of days per year that a target is observable at low background,
  for a given wavelength and a selectable threshold.

Software is provided as-is, with no warranty. Use the latest versions of APT and ETC to confirm 
the observability of any JWST targets. 
 
"""
import os, struct, urllib, healpy, numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from jwst_backgrounds.version import __version__

class background:
    __doc__ = '\n    Main background class. It is initialized with all background data for a specific\n    position (RA, DEC). The wavelength at which the bathtub curve is calculated \n    can be updated as needed.\n    \n    Parameters\n    ----------\n    ra: float\n        Right ascension in decimal degrees\n    dec: float \n        Declination in decimal degrees\n    wavelength: float \n        Wavelength at which the bathtub curve is calculated, in micron\n    thresh: float\n        the background threshold, relative to the minimum.  Default=1.1, which corresponds to <5% above the minimum background noise.\n        Note that the actual noise difference will be even smaller, as there are often other significant sources of noise than just the\n        background (source shot noise, detector noise, etc.).\n        \n    Attributes\n    ----------\n    bkg_data: dict\n        Contains all the data for the background for the input (RA,DEC) position \n    bathtub: \n        Contains the (RA,DEC) background information as a function of calendar day, interpolated at wavelength\n    '

    def __init__(self, ra, dec, wavelength, thresh=1.1):
        self.cache_url = 'https://archive.stsci.edu/missions/jwst/simulations/straylight/sl_cache/'
        self.local_path = os.path.join(os.path.dirname(__file__), 'refdata')
        self.wave_file = 'std_spectrum_wavelengths.txt'
        self.thermal_file = 'thermal_curve_jwst_jrigby_cchen_1.1a.csv'
        self.nside = 128
        self.wave_array, self.thermal_bg = self.read_static_data()
        self.sl_nwave = self.wave_array.size
        self.ra = ra
        self.dec = dec
        self.wavelength = wavelength
        self.thresh = thresh
        self.cache_file = self.myfile_from_healpix(ra, dec)
        self.bkg_data = self.read_bkg_data(self.cache_file)
        self.make_bathtub(wavelength)

    def myfile_from_healpix(self, ra, dec):
        healpix = healpy.pixelfunc.ang2pix((self.nside), ra, dec, nest=False, lonlat=True)
        healpix_str_pad = str(healpix).zfill(6)
        file = healpix_str_pad[0:4] + '/sl_pix_' + healpix_str_pad + '.bin'
        return file

    def read_static_data(self):
        abs_wave_file = os.path.join(self.local_path, self.wave_file)
        wave_array = np.loadtxt(abs_wave_file)
        thermal = np.genfromtxt((os.path.join(self.local_path, self.thermal_file)), delimiter=',')
        thermal_int = self.interpolate_spec((thermal[:, 0]), (thermal[:, 1]), wave_array, fill=0.0)
        return (
         wave_array, thermal_int)

    def read_bkg_data(self, cache_file, verbose=False):
        """
        Method for reading one JWST background file, and parsing it.    
        
        Schema of each binary file in the cache:
        ----------------------------------------
        JRR verified the schema against the source code, generate_stray_light_with_threads.c. 
        The cache uses a Healpix RING tesselation, with NSIDE=128.  Every point on the sky 
        (tesselated tile) corresponds to one binary file, whose name includes its healpix 
        pixel number, in a directory corresponding to the first 4 digits of the healpix number.  

        - double RA
        - double DEC
        - double pos[3]
        - double nonzodi_bg[SL_NWAVE]
        - int[366] date_map  : This maps dates to indices.  NOTE: There are 366 days, not 365!
        - for each day in FOR:
            - double zodi_bg[SL_NWAVE]
            - double stray_light_bg[SL_NWAVE]
        
        parameters
        ----------
        cache_file: string
        
        attributes
        ----------
        
        """
        try:
            version_file = urllib.request.urlopen(self.cache_url + 'VERSION')
            sbet_file = urllib.request.urlopen(self.cache_url + cache_file)
        except:
            version_file = urllib.urlopen(self.cache_url + 'VERSION')
            sbet_file = urllib.urlopen(self.cache_url + cache_file)

        self.cache_version = version_file.readlines()[0].decode('utf-8')[:-1]
        sbet_data = sbet_file.read()
        if verbose:
            print('File has', len(sbet_data), 'bytes, which is', len(sbet_data) / 8.0, 'doubles')
        size_calendar = struct.calcsize('366i')
        partA = struct.unpack(str(5 + self.sl_nwave) + 'd', sbet_data[0:(5 + self.sl_nwave) * 8])
        ra = partA[0]
        dec = partA[1]
        pos = partA[2:5]
        nonzodi_bg = np.array(partA[5:5 + self.sl_nwave])
        date_map = np.array(struct.unpack('366i', sbet_data[(5 + self.sl_nwave) * 8:(5 + self.sl_nwave) * 8 + size_calendar]))
        if verbose:
            print('Out of', len(date_map), 'days, these many are legal:', np.sum(date_map >= 0))
        calendar = np.where(date_map >= 0)[0]
        Ndays = len(calendar)
        if verbose:
            print(len(date_map), Ndays)
        zodi_bg = np.zeros((Ndays, self.sl_nwave))
        stray_light_bg = np.zeros((Ndays, self.sl_nwave))
        perday = self.sl_nwave * 2
        partB = struct.unpack(str(len(calendar) * self.sl_nwave * 2) + 'd', sbet_data[perday * Ndays * -8:])
        for dd in range(0, int(Ndays)):
            br1 = dd * perday
            br2 = br1 + self.sl_nwave
            br3 = br2 + self.sl_nwave
            zodi_bg[(dd,)] = partB[br1:br2]
            stray_light_bg[(dd,)] = partB[br2:br3]

        total_bg = np.tile(nonzodi_bg + self.thermal_bg, (Ndays, 1)) + stray_light_bg + zodi_bg
        return {'calendar':calendar, 
         'ra':ra,  'dec':dec,  'pos':pos,  'wave_array':self.wave_array,  'nonzodi_bg':nonzodi_bg,  'thermal_bg':self.thermal_bg, 
         'zodi_bg':zodi_bg,  'stray_light_bg':stray_light_bg,  'total_bg':total_bg}

    def make_bathtub(self, wavelength):
        """
        This method interpolates a bathtub curve at a given wavelength.
        It also uses the threshold fraction ("thresh") above the minimum background, to calculate number of good days.
        
        parameters
        ----------
        wavelength: float
        
        """
        self.wavelength = wavelength
        wave_array = self.bkg_data['wave_array']
        total_thiswave = interp1d(wave_array, (self.bkg_data['total_bg']), bounds_error=True)(wavelength)
        stray_thiswave = interp1d(wave_array, (self.bkg_data['stray_light_bg']), bounds_error=True)(wavelength)
        zodi_thiswave = interp1d(wave_array, (self.bkg_data['zodi_bg']), bounds_error=True)(wavelength)
        thermal_thiswave = interp1d(wave_array, (self.bkg_data['thermal_bg']), bounds_error=True)(wavelength)
        nonzodi_thiswave = interp1d(wave_array, (self.bkg_data['nonzodi_bg']), bounds_error=True)(wavelength)
        themin = np.min(total_thiswave)
        good_days = int(np.sum(total_thiswave < themin * self.thresh) * 1.0)
        self.bathtub = {'wavelength':wavelength, 
         'themin':themin,  'good_days':good_days,  'total_thiswave':total_thiswave, 
         'stray_thiswave':stray_thiswave,  'zodi_thiswave':zodi_thiswave,  'thermal_thiswave':thermal_thiswave, 
         'nonzodi_thiswave':nonzodi_thiswave}

    def interpolate_spec(self, wave, specin, new_wave, fill=np.nan):
        f = interp1d(wave, specin, bounds_error=False, fill_value=fill)
        new_spec = f(new_wave)
        return new_spec

    def plot_background(self, fontsize=16, xrange=(0.6, 30), yrange=(0.0001, 10000.0), thisday=None):
        wave_array = self.bkg_data['wave_array']
        calendar = self.bkg_data['calendar']
        if thisday in calendar:
            thisday_index = np.where(thisday == calendar)[0][0]
        else:
            print('The input calendar day {}'.format(thisday) + ' is not available')
            return
            plt.plot(wave_array, (self.bkg_data['nonzodi_bg']), label='ISM')
            plt.plot(wave_array, (self.bkg_data['zodi_bg'][thisday_index, :]), label='Zodi')
            plt.plot(wave_array, (self.bkg_data['stray_light_bg'][thisday_index, :]), label='Stray light')
            plt.plot(wave_array, (self.bkg_data['thermal_bg']), label='Thermal')
            plt.plot(wave_array, (self.bkg_data['total_bg'][thisday_index, :]), label='Total', color='black', lw=3)
            plt.xlim(xrange)
            plt.ylim(yrange)
            plt.xlabel('wavelength (micron)', fontsize=fontsize)
            plt.ylabel('Equivalent in-field radiance (MJy/sr)', fontsize=fontsize)
            plt.title('Background for calendar day ' + str(thisday))
            plt.legend()
            plt.yscale('log')
            plt.show()

    def plot_bathtub(self, showthresh=True, showplot=False, showsubbkgs=False, showannotate=True, title=False, label=False):
        bathtub = self.bathtub
        if not label:
            label = 'Total ' + str(bathtub['wavelength']) + ' micron'
        else:
            calendar = self.bkg_data['calendar']
            plt.scatter(calendar, (bathtub['total_thiswave']), s=20, label=label)
            plt.xlabel('Day of the year', fontsize=12)
            plt.xlim(0, 366)
            if showannotate:
                annotation = str(bathtub['good_days']) + ' good days out of ' + str(calendar.size) + ' days observable, for threshold ' + str(self.thresh)
                plt.title(annotation)
                plt.ylabel(('bkg at ' + str(bathtub['wavelength']) + ' um (MJy/sr)'), fontsize=12)
            else:
                plt.ylabel('bkg (MJy/SR)', fontsize=fontsize)
        if showsubbkgs:
            plt.scatter(calendar, (bathtub['zodi_thiswave']), s=20, label='Zodiacal')
            plt.scatter(calendar, (bathtub['stray_thiswave']), s=20, label='Stray light')
            plt.scatter(calendar, (bathtub['nonzodi_thiswave'] * np.ones_like(calendar)), s=20, label='ISM+CIB')
            plt.scatter(calendar, (bathtub['thermal_thiswave'] * np.ones_like(calendar)), s=20, label='Thermal')
            plt.legend(fontsize=10, frameon=False, labelspacing=0)
            plt.grid()
            plt.locator_params(axis='x', nbins=10)
            plt.locator_params(axis='y', nbins=10)
        if showthresh:
            percentiles = (
             bathtub['themin'], bathtub['themin'] * self.thresh)
            plt.hlines(percentiles, 0, 365, color='black')
        if title:
            plt.title(title)
        plt.show()

    def write_bathtub(self, bathtub_file='background_versus_day.txt'):
        f = open(bathtub_file, 'w')
        header_text = ['# Output of JWST_backgrounds version ' + str(__version__) + '\n',
         '# background cache version ' + str(self.cache_version) + '\n',
         '\n# for RA=' + str(self.ra) + ', DEC=' + str(self.dec) + ' at wavelength=' + str(self.wavelength) + ' micron \n',
         '# Columns: \n',
         '# - Calendar day (Jan1=0) \n',
         '# - Total background (MJy/sr)\n']
        for line in header_text:
            f.write(line)

        for i, calendar_day in enumerate(self.bkg_data['calendar']):
            f.write('{0}    {1:5.4f}'.format(calendar_day, self.bathtub['total_thiswave'][i]) + '\n')

        f.close()

    def write_background(self, background_file='background.txt', thisday=None):
        calendar = self.bkg_data['calendar']
        if thisday in calendar:
            thisday_index = np.where(thisday == calendar)[0][0]
        else:
            print('The input calendar day {}'.format(thisday) + ' is not available')
            return
            f = open(background_file, 'w')
            header_text = ['# Output of JWST_backgrounds version ' + str(__version__) + '\n',
             '# background cache version ' + str(self.cache_version) + '\n',
             '\n# for RA=' + str(self.ra) + ', DEC=' + str(self.dec) + ' On calendar day ' + str(thisday) + '\n',
             '# Columns: \n',
             '# - Wavelength [micron] \n',
             '# - Total background (MJy/sr)\n',
             '# - In-field zodiacal light (MJy/sr)\n',
             '# - In-field galactic light (MJy/sr)\n',
             '# - Stray light (MJy/sr)\n',
             '# - Thermal self-emission (MJy/sr)\n']
            for line in header_text:
                f.write(line)

            for i, wavelength in enumerate(self.bkg_data['wave_array']):
                f.write('{0:f}    {1:5.4f}    {2:5.4f}    {3:5.4f}    {4:5.4f}    {5:5.4f}'.format(wavelength, self.bkg_data['total_bg'][thisday_index][i], self.bkg_data['zodi_bg'][thisday_index][i], self.bkg_data['nonzodi_bg'][i], self.bkg_data['stray_light_bg'][thisday_index][i], self.bkg_data['thermal_bg'][i]) + '\n')

            f.close()


def get_background(ra, dec, wavelength, thresh=1.1, plot_background=True, plot_bathtub=True, thisday=None, showsubbkgs=False, write_background=True, write_bathtub=True, background_file='background.txt', bathtub_file='background_versus_day.txt'):
    """
    This is the main method, which serves as a wrapper to get the background data and create plots and outputs with one command.
    
    Parameters
    ----------
    ra: float
        Right ascension in decimal degrees
    dec: float 
        Declination in decimal degrees
    wavelength: float 
        Wavelength at which the bathtub curve is calculated, in micron
    thresh: float
        the background threshold, relative to the minimum.  Default=1.1, which corresponds to <5% above the minimum background noise.
        Note that the actual noise difference will be even smaller, as there are often other significant sources of noise than just the
        background (source shot noise, detector noise, etc.).
    plot_background: bool 
        whether to plot the background spectrum (and its components) for this day.
    thisday: int
        calendar day to use for plot_spec.  If not given, will use the average of visible calendar days.
    plot_days: bool
        whether to show the plot of background at wavelength_input versus calendar days
    showsubbkgs: bool
        whether to show the components of the background in the bathtub plot.
    write_bathtub: bool
        whether to print the background levels that are plotted in plot_days to an output file
    outfile:     output filename

    """
    bkg = background(ra, dec, wavelength, thresh=thresh)
    calendar = bkg.bkg_data['calendar']
    print('These coordinates are observable by JWST', len(bkg.bkg_data['calendar']), 'days per year.')
    print('For', bkg.bathtub['good_days'], 'of those days, the background is <', thresh, 'times the minimum, at wavelength', wavelength, 'micron')
    if thisday not in calendar:
        ndays = calendar.size
        if ndays > 0:
            thisday_input = thisday
            thisday = calendar[int(ndays / 2)]
            print('Warning: The input calendar day {}'.format(thisday_input) + ' is not available, assuming the middle day: {} instead'.format(thisday))
        else:
            print('No valid days')
            return
    if plot_background:
        bkg.plot_background(thisday=thisday)
    if write_background:
        bkg.write_background(thisday=thisday, background_file=background_file)
    if plot_bathtub:
        bkg.plot_bathtub(showsubbkgs=showsubbkgs)
    if write_bathtub:
        bkg.write_bathtub(bathtub_file=bathtub_file)