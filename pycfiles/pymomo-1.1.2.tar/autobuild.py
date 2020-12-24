# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/autobuild.py
# Compiled at: 2015-03-19 14:45:48
import utilities, pic24, pic12, unit_test, unit_test12
from SCons.Script import *
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymomo.exceptions import *
import pymomo

def autobuild_pic12(module, test_dir='test', modulefile=None):
    """
        Build the given module for all targets and build all unit tests.
        targets are determined from /config/build_settings.json using
        the module name and the tests are found automatically and built 
        using their builtin metadata
        """
    try:
        family = utilities.get_family('mib12', modulefile=modulefile)
        family.for_all_targets(module, lambda x: pic12.build_module(module, x))
        unit_test.build_units(test_dir, family.targets(module))
        Alias('release', os.path.join('build', 'output'))
        Alias('test', os.path.join('build', 'test', 'output'))
        Default('release')
    except MoMoException as e:
        print e.format()
        sys.exit(1)


def autobuild_pic24(module, test_dir='test', modulefile=None, postprocess_hex=None):
    """
        Build the given pic24 module for all targets.
        """
    try:
        family = utilities.get_family('mib24', modulefile=modulefile)
        family.for_all_targets(module, lambda x: pic24.build_module(module, x, postprocess_hex=postprocess_hex))
        Alias('release', os.path.join('build', 'output'))
        Alias('test', os.path.join('build', 'test', 'output'))
        Default('release')
    except MoMoException as e:
        print e.format()
        sys.exit(1)