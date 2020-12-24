# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/__init__.py
# Compiled at: 2018-12-15 16:31:41
__doc__ = '\nThe JModelica.org Python package for working with FMI <http:/www.jmodelica.org/>\n'
__all__ = [
 'fmi_algorithm_drivers', 'examples', 'fmi', 'common']
from .fmi import FMUModel, load_fmu, FMUModelME1, FMUModelME2
from .fmi import FMUModelCS1, FMUModelCS2
from .fmi_coupled import CoupledFMUModelME2
from .master import Master
from .fmi_extended import FMUModelME1Extended
import numpy as N, os.path
int = N.int32
N.int = N.int32

def testattr(**kwargs):
    """Add attributes to a test function/method/class.
    
    This function is needed to be able to add
      @attr(slow = True)
    for functions.
    
    """

    def wrap(func):
        func.__dict__.update(kwargs)
        return func

    return wrap


try:
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    _fpath = os.path.join(curr_dir, 'version.txt')
    with open(_fpath, 'r') as (f):
        __version__ = f.readline().strip()
        __revision__ = f.readline().strip()
except:
    __version__ = 'unknown'
    __revision__ = 'unknown'

def check_packages():
    import sys, time
    le = 30
    le_short = 15
    startstr = 'Performing pyfmi package check'
    sys.stdout.write('\n')
    sys.stdout.write(startstr + ' \n')
    sys.stdout.write('=' * len(startstr))
    sys.stdout.write('\n\n')
    sys.stdout.flush()
    time.sleep(0.25)
    sys.stdout.write('%s %s' % (('PyFMI version ').ljust(le, '.'), __version__.ljust(le) + '\n\n'))
    sys.stdout.flush()
    time.sleep(0.25)
    platform = sys.platform
    sys.stdout.write('%s %s' % (('Platform ').ljust(le, '.'), str(platform).ljust(le) + '\n\n'))
    sys.stdout.flush()
    time.sleep(0.25)
    pyversion = sys.version.partition(' ')[0]
    sys.stdout.write('%s %s' % (('Python version ').ljust(le, '.'), pyversion.ljust(le)))
    sys.stdout.write('\n\n')
    sys.stdout.flush()
    time.sleep(0.25)
    import imp
    sys.stdout.write('\n\n')
    sys.stdout.write(('Dependencies: \n\n').rjust(0))
    modstr = 'Package'
    verstr = 'Version'
    sys.stdout.write('%s %s' % (modstr.ljust(le), verstr.ljust(le)))
    sys.stdout.write('\n')
    sys.stdout.write('%s %s' % (('-' * len(modstr)).ljust(le), ('-' * len(verstr)).ljust(le)))
    sys.stdout.write('\n')
    packages = [
     'assimulo', 'Cython', 'lxml', 'matplotlib', 'numpy', 'scipy', 'wxPython']
    if platform == 'win32':
        packages.append('pyreadline')
        packages.append('setuptools')
    error_packages = []
    warning_packages = []
    fp = None
    for package in packages:
        try:
            try:
                vers = '--'
                fp, path, desc = imp.find_module(package)
                mod = imp.load_module(package, fp, path, desc)
                try:
                    if package == 'pyreadline':
                        vers = mod.release.version
                    elif package == 'lxml':
                        from lxml import etree
                        vers = etree.__version__
                    else:
                        vers = mod.__version__
                except AttributeError:
                    pass

                sys.stdout.write('%s %s' % (package.ljust(le, '.'), vers.ljust(le)))
            except ImportError:
                if package == 'assimulo' or package == 'wxPython':
                    sys.stdout.write('%s %s %s' % (package.ljust(le, '.'), vers.ljust(le_short), ('Package missing - Warning issued, see details below').ljust(le_short)))
                    warning_packages.append(package)
                else:
                    sys.stdout.write('%s %s %s ' % (package.ljust(le, '.'), vers.ljust(le_short), ('Package missing - Error issued, see details below.').ljust(le_short)))
                    error_packages.append(package)

        finally:
            if fp:
                fp.close()

        sys.stdout.write('\n')
        sys.stdout.flush()
        time.sleep(0.25)

    if len(error_packages) > 0:
        sys.stdout.write('\n')
        errtitle = 'Errors'
        sys.stdout.write('\n')
        sys.stdout.write(errtitle + ' \n')
        sys.stdout.write('-' * len(errtitle))
        sys.stdout.write('\n\n')
        sys.stdout.write('The package(s): \n\n')
        for er in error_packages:
            sys.stdout.write('   - ' + str(er))
            sys.stdout.write('\n')

        sys.stdout.write('\n')
        sys.stdout.write('could not be found. It is not possible to run the pyfmi package without it/them.\n')
    if len(warning_packages) > 0:
        sys.stdout.write('\n')
        wartitle = 'Warnings'
        sys.stdout.write('\n')
        sys.stdout.write(wartitle + ' \n')
        sys.stdout.write('-' * len(wartitle))
        sys.stdout.write('\n\n')
        for w in warning_packages:
            if w == 'assimulo':
                sys.stdout.write('-- The package assimulo could not be found. This package is needed to be able to simulate FMUs. Also, some of the examples in pyfmi.examples will not work.')
            elif w == 'wxPython':
                sys.stdout.write('-- The package wxPython could not be found. This package is needed to be able to use the plot-GUI.')
            sys.stdout.write('\n\n')

    return