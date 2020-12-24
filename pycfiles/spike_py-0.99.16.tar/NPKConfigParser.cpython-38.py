# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/NPKConfigParser.py
# Compiled at: 2020-01-30 15:08:54
# Size of source mod 2**32: 6297 bytes
"""
A utility that wraps ConfigParser for NPK

Typical use is :

cp = NPKConfigParser()
cp.readfp(open(configfilename))     # where configfilename is the name of the config file
var1 =    cp.get( section, varname1)
var2 =    cp.get( section, varname2, default_value)
...
you can use
get()  getint()  getfloat()  getboolean()
see details in methods.

Created by Marc-André on 2011-10-14.
Copyright (c) 2011 IGBMC. All rights reserved.

MAD modif on 21 - may 2012 - added getword and removing trailing comments
MAD, in April 2017 : adapted (painfully) to python3
"""
from __future__ import print_function, division
import unittest, sys
if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser as ConfigParser
    Python3 = False
else:
    from configparser import ConfigParser, _UNSET
    Python3 = True
import re

class NPKConfigParser(ConfigParser):
    __doc__ = '\n    this is a subclass of ConfigParser.ConfigParser, providing default value for values\n    will never raise an error on missing values\n    '
    _boolean_states = {'1':True, 
     'on':True,  'false':False,  '0':False,  'off':False,  'yes':True,  'no':False,  'true':True}
    if Python3:

        def get(self, section, option, default=None, raw=0, verbose=False, fallback=_UNSET):
            """read a value from the configuration, with a default value"""
            if self.has_option(section, option):
                vv = ConfigParser.get(self, section, option, raw=raw, fallback=None)
                vl = re.split('\\s*#', vv)
                return vl[0]
            if verbose:
                print('Using default value for {} : {}'.format(option, default))
            return default

    else:

        def get(self, section, option, default=None, raw=0, vars=None, verbose=False):
            """read a value from the configuration, with a default value"""
            if self.has_option(section, option):
                vv = ConfigParser.get(self, section, option, raw=raw, vars=vars)
                vl = re.split('\\s*#', vv)
                return vl[0]
            if verbose:
                print('Using default value for {} : {}'.format(option, default))
            return default

    def getword(self, section, option, default=None, raw=0, verbose=False):
        """read a value from the configuration, with a default value - takes the first word of the string"""
        vv = self.get(section, option, default=(str(default)), raw=raw, verbose=verbose)
        v = vv.split()[0]
        return v

    def getint(self, section, option, default=0, raw=0, verbose=False):
        """
        read a int value from the configuration, with a default value
        understands 123 16k 32M 4G 2T ... (units in power of 2, not power of 10 !!)
        """
        v = self.getword(section, option, default=(str(default)), raw=raw, verbose=verbose).lower()
        if v.endswith('k'):
            val = 1024 * int(v[:-1])
        else:
            if v.endswith('m'):
                val = 1048576 * int(v[:-1])
            else:
                if v.endswith('g'):
                    val = 1073741824 * int(v[:-1])
                else:
                    if v.endswith('t'):
                        val = 1099511627776 * int(v[:-1])
                    else:
                        val = int(v)
        return val

    def getfloat(self, section, option, default=0.0, raw=0, verbose=False):
        """read a float value from the configuration, with a default value"""
        return float(self.getword(section, option, default=(str(default)), raw=raw, verbose=verbose))

    def getboolean(self, section, option, default='OFF', raw=0, verbose=False):
        """read a boolean value from the configuration, with a default value"""
        v = self.getword(section, option, default=(str(default)), raw=raw, verbose=verbose)
        if v.lower() not in self._boolean_states:
            raise ValueError('Not a boolean: %s' % v)
        return self._boolean_states[v.lower()]


class Tests(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print(self.shortDescription())

    def test_def(self):
        """testing configparser default values"""
        self.announce()
        cp = NPKConfigParser()
        cp.read('None')
        self.assertEqual('def_apex', cp.get('section', 'apex', default='def_apex'))
        self.assertEqual(123, cp.getint('section', 'int_value', default=123))
        self.assertEqual(2048, cp.getint('section', 'int_value', default='2k'))
        self.assertEqual(3145728, cp.getint('section', 'int_value', default='3M'))
        self.assertEqual(123.45, cp.getfloat('section', 'f_value', default=123.45))
        self.assertEqual(0.0, cp.getfloat('section', 'f_value'))
        self.assertFalse(cp.getboolean('section', 'b_value'))
        self.assertTrue(cp.getboolean('section', 'b_value', default='true'))

    def test_read(self):
        """testing configparser - getting values from file"""
        from .Tests import filename
        self.announce()
        cp = NPKConfigParser()
        cp.read(filename('test.mscf'))
        print('sections:', list(cp.sections()))
        for sec in ('import', 'processing', 'visu2d'):
            self.assertTrue(sec in list(cp.sections()))
        else:
            fname = cp.get('import', 'apex', verbose=True, default='def_apex')
            self.assertEqual('ubiquitine_2D_000002.d', fname)
            self.assertEqual(2500.0, cp.getfloat('import', 'highmass', default=123.45))
            self.assertEqual(True, cp.getboolean('processing', 'do_modulus', default=False))
            self.assertEqual(68719476736, cp.getint('processing', 'largest_file', default=123))


if __name__ == '__main__':
    unittest.main()