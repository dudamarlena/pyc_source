# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Tests.py
# Compiled at: 2020-02-19 13:22:18
# Size of source mod 2**32: 9242 bytes
"""
Tests.py

Created by Marc-André  on 2010-07-20.

Runs tests on selected modules using the integrated unittests in the different SPIKE modules.

most default values can be overloaded with run time arguments

Example on a module :
    python -m spike.Tests -D DATA_test -t File.Apex

"""
from __future__ import print_function, division
import unittest, os
import os.path as op
import shutil, sys
from .Display import testplot
__version__ = '2.0'
CLEAN = True
MAIL = False
list_of_mails = []
DATA_dir = '/Volume/DATA_test'
RUN = True
mod_util = ('plugins', 'util.dynsubplot', 'util.debug_tools')
mod_algo = ('Algo.Cadzow', 'Algo.Linpredic', 'Algo.urQRd', 'Algo.sane', 'Algo.SL0',
            'Algo.maxent', 'Algo.BC')
mod_plugins = ('plugins.Peaks', 'plugins.Fitter', 'plugins.Bruker_NMR_FT', 'plugins.Peaks')
mod_file = ('File.BrukerNMR', 'File.GifaFile', 'File.HDF5File', 'File.Apex', 'File.csv',
            'File.Solarix', 'File.mzXML')
mod_basicproc = ('NPKData', 'NMR', 'FTICR', 'Orbitrap', 'NPKConfigParser')
mod_user = ('processing', )
list_of_modules = mod_basicproc + mod_file + mod_util + mod_algo + mod_plugins + mod_user

def directory():
    """returns the location of the directory containing dataset for tests"""
    global DATA_dir
    try:
        dd = testplot.config['DATA_dir']
    except AttributeError:
        dd = DATA_dir

    return dd


def filename(name):
    """returns the full name of a test dataset located in the test directory"""
    return op.join(directory(), name)


def msg(st, sep='='):
    """
    Message in Tests.py
    """
    s = sep * (len(st) + 4) + '\n'
    s = s + '| ' + st + ' |' + '\n'
    s = s + sep * (len(st) + 4) + '\n'
    print(s)
    return s


def cleanspike():
    """
    Removes the .pyc in spike
    """
    for root, dirs, files in os.walk('spike'):
        for f in files:
            r, ext = os.path.splitext(f)
            if ext == 'pyc':
                addr = os.path.join(root, f)
                print(addr)
                os.remove(addr)

        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d))


def cleandir(verbose=True):
    """checking files in DATA_dir directory and removes files created by previous tests"""
    global CLEAN
    import glob
    files_to_keep = ('ubiquitin_5_scan_res_30000_1.dat', 'cytoC_ms_1scan_000001.d',
                     'cytoC_2D_000001.d', 'dosy-cluster2-corr.gs2', 'dosy-cluster2.gs2',
                     'proj.gs1', 'ubiquitine_2D_000002.d', 'Lasalocid-Tocsy', 'Sampling_file.list',
                     'ubiquitine_2D_000002_Sampling_2k.list', 'test.mscf', 'test_.mscf',
                     'ubiquitine_2D_000002.msh5', 'ubiquitine_2D_000002_mr.msh5',
                     'Sampling_file_aposteriori_cytoCpnas.list', 'angio_ms_000005.d',
                     'SubsP_220615_2DFT_2k_128k_000001.d', 'testsmzXML')
    for i in glob.glob(filename('*')):
        if verbose:
            print(i, end=' ')
        else:
            if os.path.basename(i) in files_to_keep:
                if verbose:
                    print(' Ok')
                else:
                    if CLEAN:
                        try:
                            os.remove(i)
                            if verbose:
                                print(' removed')
                        except OSError:
                            if verbose:
                                print(' **** could not be removed ****')

            else:
                if verbose:
                    print(' should be removed')
            print(i, ' should be removed')


class NPKTest(unittest.TestCase):
    __doc__ = 'overload unittest.TestCase for default verbosity - Not Used - '

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')


def do_Test():
    """
    Performs all tests then indicates if successfull.
    Gives total time elapsed.
    """
    global MAIL
    global RUN
    global list_of_mails
    global list_of_modules
    import time, numpy, platform
    python = ('{0}.{1}.{2}'.format)(*sys.version_info)
    npv = numpy.version.version
    subject = ('SPIKE tests performed on {2} {4} running python {0} / numpy {1} on host {3}'.format)(python, npv, *platform.uname())
    to_mail = [msg(subject), 'Test program version %s' % __version__]
    list_of_modules = ['spike.' + mod for mod in list_of_modules]
    msg('modules to be tested are:')
    for mod in list_of_modules:
        print(mod)

    stdata = '\nDatasets for tests are located in : %s' % DATA_dir
    to_mail.append(stdata)
    print(stdata)
    if not RUN:
        print('\nDry run - stopping now, without executing the tests')
        sys.exit(0)
    else:
        msg('First removing leftover files')
        cleandir()
        if CLEAN:
            msg('removing .pyc in spike')
            cleanspike()
        msg('Running automatic Tests')
        t0 = time.time()
        suite = unittest.defaultTestLoader.loadTestsFromNames(list_of_modules)
        nbtests = suite.countTestCases()
        results = unittest.TextTestRunner(verbosity=2).run(suite)
        elaps = time.time() - t0
        to_mail.append('Ran %d tests in %.3fs' % (nbtests, elaps))
        if results.wasSuccessful():
            to_mail.append(msg('CONGRATULATIONS - all the {} SPIKE tested modules performed succesfully '.format(len(list_of_modules))))
            subject = 'SUCCESS :)  ' + subject
            to_mail.append(msg('modules tested were:'))
            for mod in list_of_modules:
                print(mod)
                to_mail.append(mod)

            to_mail.append(msg('test performed in %.2f sec' % elaps))
        else:
            subject = 'Failed :(  ' + subject
            to_mail.append(msg('Tests Failed, Please revise error codes', sep='!'))
            to_mail.append('%d test(s) failed :' % len(results.errors))
            for err in results.errors:
                to_mail.append(msg('%s' % err[0]))
                to_mail.append(err[1])

    print('\n'.join(to_mail))
    if MAIL:
        from util.sendgmail import mail
        for address in list_of_mails:
            mail(address, subject, '\n'.join(to_mail))

    cleandir(verbose=False)


def main():
    global CLEAN
    global DATA_dir
    global MAIL
    global RUN
    global list_of_mails
    global list_of_modules
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-m', '--mail', action='append', help='a mail address to which the result is sent at the end of the test - multiple entries possible -')
    parser.add_argument('-D', '--Data', help='the location of the folder containing files for the tests')
    parser.add_argument('-t', '--test_modules', action='append', help='overwrite the list of modules to test - multiple entries possible -')
    parser.add_argument('-n', '--dry', action='store_true', help='list parameters and do not run the tests')
    parser.add_argument('-d', '--dirty', action='store_true', help='do not remove temporary files')
    parser.add_argument('-c', '--clean', action='store_true', help='just remove left-over temporary files')
    parser.add_argument('-g', '--graphic', action='store_true', help='restore graphic output (off by default for background testing)')
    args = parser.parse_args()
    print('mail', args.mail)
    print('data', args.Data)
    print('module', args.test_modules)
    print('dry', args.dry)
    print('dirty', args.dirty)
    print('clean', args.clean)
    print('graphic', args.graphic)
    if args.dry:
        RUN = False
    else:
        if args.mail is not None:
            MAIL = True
            list_of_mails = args.mail
        else:
            if args.test_modules is not None:
                list_of_modules = args.test_modules
            if args.Data is not None:
                DATA_dir = args.Data
            if args.dirty:
                CLEAN = False
            if args.graphic:
                testplot.PLOT = True
            else:
                testplot.PLOT = False
        testplot.config = {}
        testplot.config['DATA_dir'] = DATA_dir
        if args.clean:
            CLEAN = True
            cleandir(verbose=True)
        else:
            do_Test()


if __name__ == '__main__':
    main()