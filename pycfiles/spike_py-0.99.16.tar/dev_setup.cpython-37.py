# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/dev_setup.py
# Compiled at: 2020-04-22 12:30:01
# Size of source mod 2**32: 21906 bytes
"""
dev_setup.py

To be called any time a new version is rolled out !

Created by Marc-Andre' on 2010-07-20.
"""
from __future__ import print_function
from codecs import decode
ProgramName = 'SPIKE'
VersionName = 'Development version'
VersionInfo = ['0', '99', '16']
release_notes = '\n# SPIKE Relase Notes\n#### 0.99.16 - April 2020 \n- FTICR a new Apex0 bruker importer - to access old datasets, with the "NMR" setup (acqus pdata ...)\n- FTICR a global BrukerMS importer - Import1D - Import2D\n- a few corrected bugs\n\n#### 0.99.15 - March 2020 \nThis release introduces a major modification in the organisation of the `NPKData` object -\nwhich is the central object on which everything is organized.\n\n*Previously* `NPKData.NPKData` was the standard class, which created NMR object, and other classes\n(such as `FTICR.FTICRData` or `Orbitrap.OrbiData`) inherited from this class and had to overloaded a few things. \n`NPKData` held also all `Axis` definition, both generic and for NMR.\n\n*Now*,\n\n- `NPKData._NPKData` is a generic object - agnostic about the spectroscopy\n- `NPKData` holds also the definitions of generic Axes ( `Axis` but also `TimeAxis` and `LaplaceAxis`) \n- `NMR.NMRData` is the new class for NMR data-sets, `NMR` also contains the definitions for all NMR related Axes.\n- `FTICR.FTICRData` and `Orbitrap.OrbiData` now inherit from the `_NPKData` class (through `FTMS`).\n\nIn consequence, to create an NMR dataset from scratch, now do:\n```\n        NMR.NMRData(...)\n```\nwhere you were using `NPKData.NPKData` previously\n\nand do \n```\n        NPKData._NPKData(...)\n```\nto create an empty dataset not associated to any spectroscopy\n\n*This should have been done long ago - but I\'m so lazy...*\n\n**Other modifications**\n- This set-up allows to better adapt compound experiments (LC-NMR LC-MS ...)\n- jupytext extension was added to jupyter Notebooks\n    - means that a python copy is maintained - only this copy is version controlled\n- still improvements in notebooks\n- \n- NMR: improvement in the SpinIt importer\n- FTICR: added a Bo attribute\n- added the NbMaxPeaks flag in Peak display\n- added the self.kind attribute in the Axis class - easier to use than self.NMR !\n- small bugs corrections\n- adding a complex value to a complex datasets was wrong in complex mode.\n- tests in python 2.7 are abandoned - but very few python 3 features are really used...\n- REMARK, it was always mentionned that version 1.0 would be rolled out\n  when interactive functions in notebooks would be really usefull.\n  It will be the next big release probably !\n\n#### 0.99.14 - October 2019 - not released on pypi -\n- NMR: lots of improvements in Proc1DNMR notebooks\n- improvements in NoteBook for mouse interactivity (click and scroll)\n    - requires the additional ipympl module\n\n#### 0.99.13 - October 2019 - not released on pypi -\n- MS: added the EasyDisplayFTICR2D for non programers !\n- improvements in NoteBook interactivity\n- added smoothing in spline baselinecorrection\n\n#### 0.99.12 - September 2019\nThe 0.99.11 had a bug in the display of 1D NMR experiment - the 0.99.12 corrects it.\n\n#### 0.99.11 - September 2019\n- NMR: added a Notebook for processing of DOSY\n- many improvement in the interactive Notebooks, and in the interactive library (still work to do though)\n- added autpoints computation for spline baseline correction\n- corrected axis placement in spectral display (you should not have inverted axis anymore)\n- corrected a bug when computing projections\n\n#### 0.99.10 - August 2019\n- changed calibration in FTICR-MS - now should better correspond to Bruker, both for linear and quadratic\n    - be carefull, the definitions are slightly modified, this should be taken into account when reading files,\n    however you should verify the calibration stored into previous files\n- added Proc2DNMR Notebook - preliminary!\n- continued to improve other Notebooks\n- added skewness and kurtosis in bucket lists (optional)\n- improved Test suite (should mostly work under Windows now)\n- corrected peak-picker so that  width is FWMH after centroid\n- added an option in Peaks.pk2pandas to output or not the uncertainties\n\n#### 0.99.9 - June 2019\n- improved many aspect of the interactive Notebooks\n- improved Proc1DNMR Notebook\n    - added peak-picker\n    - added integration\n    - added bucketing\n- Integrate: plugin for 1D NMR data integration\n- added peak lists export to pandas\n- added limit to the number of peak to be displayed on screen (default 1000)\n\n#### 0.99.8 - April 2019\n- corrects a BIG BUG which hampers the import of 1D NMR data-sets,\n\n#### 0.99.7 - April 2019\n**Please do not use,** see above\n- first version of Interactive Notebooks:\n    - ProcessFTICR-MS\n    - DisplayFTICR2D\n    - Process1DNMR\n- The new BrukerMS importer tries Solarix importer and falls back to Apex importer if it fails\n- improved Interactive tools\n- improved FTICR importers to accept `my_expt.d/fid` as well as `my_expt.d`\n- improved peak-picker behavior\n- improved error messages in FTICR importers\n- cured a bug in Apex.Importxx for a special xml format\n\n#### 0.99.6 - April 2019\n- extended and improved tests - finalized installation through PYPI\n- support for distribution via pip - you can now do `pip instal spike_py` and spike installed globally on your system.\n- still struggling with correct calibration routines for FTICR ! - proceed carefully ! -\n- phase() speeded-up by a factor 20 !\n- added a autothresh scaling to peakpicking (catching peaks "autothresh" times above the noise level - default is 3)\n- slight improvement of peak list reporting (additional key words: format="report" and format="full")\n- a bug in extract of complex 1D data-sets was corrected\n- added the figure keyword to peaklist display\n\n#### 0.99.3 - March 2019\n- Development of Interactive tools, to be used within Jupyter - *should be extended in further releases* -\n    - a tool for displaying multiresolution  2D FT-ICR-MS data-sets\n    - simple interface in Jupyter for 1D NMR\n    - (that part is not tested in python 2)\n- added the setup.py prgm, SPIKE is now a regular installable program - still working on it ! -\n- `scale="auto"` in 2D display, choose a level `autoscalethresh` (default is 3) times above the noise floor.\n- added `gaussenh` apodisation plugin for one-command gaussian enhancement.\n- improved display of FTMS spectra\n- improved `findnoiselevel` and `findnoiselevel_2D`\n- modified `absmax` in NPKData - now a property\n- added phase parameters to NMRAxis: `.P0` and `.P1` \n- removed the old Visu2D program - use the jupyter notebook rather !\n\n#### 0.99.2 - January 2019\n- added number of local peaks in bucketing\n- improved Bruker importer and added support for NEO/TopSpin 4.0 files\n- improved the `.set_unit()` method\n- improved importing DOSY processed with TopSpin\n- corrected a bug for min value in bucketing\n- changed pylint/QC defaults -> new values (and corrected a bad bug)\n- cleaned the code a little\n\n#### 0.99.1 - November 2018\n- added the sane algorithm\n- added the pg-sane algorithm\n- added the `NPKData.set_unit(unit)` method for pipelining\n- added the `NPKData.load_sampling(axis)` method for pipelining\n- improved spinit support\n- corrected a few bugs\n    - `NPKData.save_csv()` now works in python 3\n    - `NPKData.copy()` is now more robust\n\n#### 0.99 - April 2018 - temp release branch\nWe have been developping a lot this last year, and published quite a few results.\nThe program is now quite stable in most of its features.\nAdditions and improvements were added to the repository in the `devel` branch, however we neglected updating the more official `default` branch.\nThis release is an effort to bring everything into normal mode, and hopefully, preparing a 1.0 version !\n\nNew in 0.99:\n\n- SPIKE is now fully compatible with python 2 AND python 3\n- added the SANE noise denoising algorithm and plugin.\n    - an improvement to urQRd\n    - more faithfull to small signal intensity\n    - slightly different optimum parameters (optimal rank slightly smaller, less iterations needed)\n- added the handling of NUS 2D FTICR acquisition\n- added the PALMA DOSY processing algo and plugin (NMR).\n- added a Linear Prediction plugin\n- added the first trial for a m/z calibration plugin (MS)\n- added import from SpinIt (NMR)\n- added a primitive set of interactive tools to be used in Jupyter notebooks ( `INTER.py` )\n- added the possibility to pass a complete dictionary to matplotlib in the .display() method\n- added the .center() method for NPKData\n- added a plugin implementing a subset of Topspin commands: xf1, xf2, xfb.  (NMR)\n- added an line fitter, still very exploratory, only 1D Lorentzian for the moment\n- added more controls on plots (new_fig and mpldic arguments of `.display()` )\n- added a Spinit importer (preliminary) (NMR)\n- added a compress mode in Solarix importer (MS)\n- added new automatic tests\n- improved and extended the Bucketing plugin, with extended features\n- improved the baseline correction code\n- improved import/export to Topspin/Bruker NMR files\n- improved automatic phaser `.apmin()` (NMR)\n- improved the plugin mechanism - with added documentation\n- corrected the extract() method which was broken\n- corrected a bug when importing Topspin/Bruker NMR datasets, where $NC was not used. (NMR)\n- corrected a bug and improved 3 parameters FT-ICR calibration (MS)\n- corrected the extract function for NPKData\n- corrected a bug with contour plots and matplotlib version > 1.5.0\n- modified (improved?) plugin loading code, with additional plugin documentation\n- modified the way None values are stored into hdf5 files\n- modified `.extract()` code to work in current axis unit\n- modified `.mean()` to return complex value is axis is complex\n- improved python 3 compatibility. It is not finished yet, but most of the program is python 2/python 3 independent, some parts are still missing, \n\n- known bugs\n    - `NPKData.extract()` method not fully tested\n    - `NPKData.save_csv()` is buggy in python 3\n\n#### 0.9 - 8 sept 2016\n*never reached the normal distribution - doc partly redundant with 0.8.3*\n\n- added a baseline correction plugins, already quite developed, with 3 different methods\n- added an automatic phasing plugin, `.apmin()` still exploratory (NMR)\n- added a wavelet filtering plugin (requires the PyWavelet library)\n- added a 3D zoom plugin (requires the Mayavi library) \n- added export to Topspin/Bruker files, and added import of processed Topspin files (NMR)\n- added the upgrade of files from previous version\n- added the `d.axis?.cpxsize` : the size of an axis expressed in spectroscopic points (real of complex)\n different from `d.axis?.size` which is the size of an axis expressed in data points so\n   - `d.axis?.cpxsize == d.axis?.size`     is axis is real\n   - `d.axis?.cpxsize == d.axis?.size/2`   is axis is complex\n- improved the Peak-Picker (mostly the output capabilities)\n- improved processing.py for nicer spectra, and possibly faster processing (MS)\n- improved visu2D.py, for a greater stability and improved selection syntax\n- corrected a bug in `.conv_n_p()` (NMR)\n- and many small bugs as well\n\n#### 0.8.3 - April 2016\n- ALL spectro.\n    - added a new `cpxsize` property, associated to axes and dataset, which counts complex and real entries\n    - added: display and peak display now accept a color and markersize arguments\n    - improved plugins, plugins with a filename starting with _ do not load\n    - improved: automatic baseline correction algorithms have been improved ( `Algo/BC.py` )\n    - `finnoiselevel()` set of functions has been rewritten ( `util/signal_tools.py` )\n    - standard test now includes testing for `multiprocessing` - *DOES NOT WORK ON ALL DISTRIBUTION* if it is your case,\n      set `use_multiprocessing = False` in test.mscf\n- NMR\n    - added: BrukerNMR now imports TopSpin processed dataset (1r, 2rr)\n    - improved: and corrected Laplace axes - for a new DOSY module to come...\n    - corrected: conv_n_p() was wrong and has been corrected\n    - corrected: `gm_apod()` was wrong and has been corrected_\n    - corrected: an error in GifaFile access under Windows\n- MS\n   - processing.py (2D FTMS) now includes parallel processing in F2 (helping in certain cases)\n   - and gives sharper lineshape thanks to kaiser() apodisation\n   - files from the previous program version (0.7.x) can now be upgraded and read. just do\n      ```    python -m spike.File.HDF5File update your_file.msh5  ```\n   - improved `.report()` for FTMS datasets\n\n#### 0.8.2 - 2 Feb 2016\n - corrected a bug in processing when running under MPI parallel \n - added warning in set_col() and set_row() if type do not match.\n - starting to work on the documentation\n\n#### 0.8.1 - 24 Jan 2016\n - corrected a bug for Orbitrap related to offsetfreq.\n\n#### 0.8.0 - 23 Jan 2016\n- first clean version using the new HDF5 file set-up  **WARNING** \n    - HDF5 files created with this version cannot be read with previous versions\n    - HDF5 files created with previous versions cannot be read with this version - this should be fixed later -\n      File now contains acquisition parameters files in the attached hdf5 sub-group\n- datasets now carry store and retrieve the parmeters imported from manufacturers file in d.params\n- improved FTMS calibration using 1, 2, and 3 parameters calibration : calibA calibB calibC, retrieve by Import from experimental file\n- improved FTMS Hz unit, added the d.axis.offsetfreq parameter\n- corrected fine details of F1 demodulation and added the parameter freq_f1demodu\n- unittests extended, in particular in visu2D\n- Starting with this version\n    - a stable version will be maintained, downloadable as a zip file in the download page\n  https://bitbucket.org/delsuc/spike/downloads\n    - Two developpement branches will be used, the `default` for the stable version - improved for bugs, and the `devel` branche, used for developping the new features.\n\n#### 0.7.1 - 5 Jan 2016\n- greatly improved internal compression of msh5 files and speed of processing.py\n- many small corrections and bug fixes.\n\n#### 0.7.0 - November 2015\n- a plugin mechanism has been created which allows to add very simply new features to the program\n    - most new features are implemented through this mechanism\n- the organisation of the spectral axes has been complete modified, with the introduction of a Unit class\n    - each axis holds its own series of possible units (called .units)\n    - and the current unit used for display and selection\n    - many commands now have a zoom= ketword that works in the current unit\n    - additionnaly, there are itoc and ctoi unit converters\n- Thanks to this, NMR data-sets are now correctly handled, DOSY are still in progress and should come soon\n    - addtionnaly a plugin for Bruker NMR processing is now implemented\n- A complete 1D and 2D peak-picker is now implemented, with many controls and features\n- New baseline correction algo have been implemented\n- the sane algorithm, which is an evolution from urQrd has been separated from urQRd, so both algo can now be used independently\n- Tests have been reorganized and improved\n- Importers have been extended - parameters are now brought back to the user\n- many others\n\n#### 0.6.4 - march 2015\n- added Bruker NMR import\n- clean-up of the module, still going on\n- Tests improved\n\n#### 0.6.3 - march 2015\n- first installeable release\n\n#### 0.6.0 - dec 2014\n- Fork to SPIKE\n- Large improvements of the display program, renamed visu2D\n- Corrected a bug in the hypercomplex modulus, resulting in splitting in 2D-FT-ICR\n- many improvements everywhere\n\n#### 0.5.1 - 26 mar 2014\n- processing2.py renamed to processing.py   with added features\n    - urQRd\n- source code reorganized by folders\n\n#### 0.5.0 - 24 mar 2014\n- starting new devl effort\n- published ! version of urQRd\n\n#### 0.4.1 - 27 Sep 2012\n- final (?) version of urQRd\n- added data arithmetic\n- many other optimisation\n\n#### 0.4.0 - 20 apr 2012 -\nnew version processing2.py (temporary name)  this one\n\n- processing is performed in steps, F2 from infile to interfile (intermediate file) and F1 from interfile to outfile\n- steps are optionnal, F2 or F1 can be performed alone - allowing denoising on the interfile\n- processing is faster and mpi enabled - speed-up are better for very large files\n- has a better way of computing the smaller spectra - done by downsampling - faster and nicer\n- vignette is now 1024x1024 - can be changed using SIZEMIN in config file\n\n#### 0.3.11 - 29 mar 2012\nSmall tools have been added to modify configuration files and to mix processing.py and ipython visualisation\n\n#### 0.3.10 - 22 jan  2012\nprocessing is now (hopefully) bug free and RAPID !\n\n#### 0.3.9 - 18 jan  2012\nfticrvisu.py, processing working, getting all parameters correctly from FTICRData and Apex\n\n#### 0.3.8 - 13 jan  2012\nfticrvisu.py, processing working, corrected after Marie came\n\n#### 0.3.7 - 12 dec  2011\ncorrection of Gifa file bug, bug in Apex for narrow band data-sets, changes in msh5 file format\n\n#### 0.3.6\n3 Oct  2011 - added  HDF5 file format (.msh5), multiresolution files, configuration files (.mscf), fticrvisu\n\n#### 0.3.5\n5 Sept 2011 - added  cadzow in MPI / savitsky-golay / HDF5 still in progress\n\n#### 0.3.4\n26 July 2011 - added  autotests / savehdf5 first version\n\n#### 0.3.3\n12 July 2011 - first reliable/taged  FTICR version\n'
UsingSVN = False
UsingHG = True
if UsingSVN:
    if UsingHG:
        raise Exception('Please define only one flag UsingHG or UsingHG !')
from subprocess import Popen, PIPE
import re
from datetime import date

def generate_notes(fname):
    """write the release notes file"""
    with open(fname, 'w') as (F):
        F.write('<!-- DO NOT MODIFY this file, it is generated automatically from dev_setup ! -->')
        F.write(release_notes)


def generate_version():
    """generates version string, revision id and data"""
    version = '.'.join(VersionInfo)
    if UsingSVN:
        svn = Popen(['svn', 'info'], stdout=PIPE).communicate()[0]
        revision = re.search('^Revision: (\\d*)', svn, re.MULTILINE).group(1)
    else:
        if UsingHG:
            hg = Popen(['hg', 'summary'], stdout=PIPE).communicate()[0]
            revision = re.search('^parent: ([\\d]*):', decode(hg), re.MULTILINE).group(1)
        else:
            revision = 'Undefined'
    today = date.today().strftime('%d-%m-%Y')
    return (version, revision, today)


def generate_file(fname):
    """
    write version to the file "name", usually "version.py", used later on
    then version.py is imported at SPIKE initialization.
    No revision version is included
    """
    f = open(fname, 'w')
    f.write('\n# This file is generated automatically by dev_setup.py \n# Do not edit\n')
    version, revision, today = generate_version()
    f.write("ProgramName = '%s'\n" % ProgramName)
    f.write("VersionName = '%s'\n" % VersionName)
    f.write("version = '%s'\n" % version)
    f.write("revision = '%s'\n" % revision)
    f.write("rev_date = '%s'\n" % today)
    f.write('\ndef report():\n    "prints version name when SPIKE starts"\n    return \'\'\'\n    ========================\n          {0}\n    ========================\n    Version     : {1}\n    Date        : {2}\n    Revision Id : {3}\n    ========================\'\'\'.format(ProgramName, version, rev_date, revision)\nprint(report())\n')
    f.close()


def generate_file_rev(fname):
    """
    write version to the file "name", usually "version.py", used later on
    then version.py is imported at SPIKE initialization.
        it assumes hg is used on client side ! - no svn version.
    """
    f = open(fname, 'w')
    f.write('\n# This file is generated automatically by dev_setup.py \n# Do not edit\nfrom subprocess import Popen, PIPE\nimport re\ntry:\n    hg = Popen(["hg", "summary"], stdout=PIPE).communicate()[0]\n    revision = re.search(\'^parent: ([\\d]*):\', hg, re.MULTILINE).group(1)\nexcept:\n    revision = "--not determined--"\n')
    version, revision, today = generate_version()
    f.write("ProgramName = '%s'\n" % ProgramName)
    f.write("VersionName = '%s'\n" % VersionName)
    f.write("version = '%s'\n" % version)
    f.write("rev_date = '%s'\n" % today)
    f.write('\ndef report():\n    "prints version name when SPIKE starts"\n    return \'\'\'\n    ========================\n          {0}\n    ========================\n    Version     : {1}\n    Date        : {2}\n    Revision Id : {3}\n    ========================\'\'\'.format(ProgramName, version, rev_date, revision)\nprint(report())\n')
    f.close()


def do(arg):
    """print and execute"""
    print(' '.join(arg))
    retcode = Popen(arg)


def plier():
    """fabrique le zip"""
    name = 'SPIKE_beta_' + '_'.join(VersionInfo)
    dirn = '../' + name
    zipn = dir + '.zip'
    do(['rm', '-r', dirn])
    do(['rm', zipn])
    do(['mkdir', dirn])
    do(['hg', 'clone', '.', dirn])
    do(['zip', '-r', zipn, dirn])


if __name__ == '__main__':
    version, revision, today = generate_version()
    print('\n=====================\nGenerating version.py\n=====================\nVersion      :  %s\nRevision Id  :  %s\n=====================\n' % (version, revision))
    generate_file('version.py')
    generate_file_rev('version_rev.py')
    generate_notes('../release_notes.md')