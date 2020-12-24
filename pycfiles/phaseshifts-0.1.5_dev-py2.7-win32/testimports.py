# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\test\testimports.py
# Compiled at: 2013-10-25 15:38:11
"""
testimports.py

Copyright (C) 2013 Liam Deacon
MIT License (see LICENSE file for details)

Test Imports - checks whether key modules and extensions can be imported
"""
import sys, os, unittest

def isimportable(package, module):
    """
    Determine whether module is importable from given package
    
    Returns
    -------
    bool : Result is True if import is successful
    
    """
    try:
        sys.stderr.write('Testing import of %s... ' % module)
        sys.stderr.flush()
        exec 'from %s import %s' % (package, module)
        sys.stderr.write('SUCCESS\n')
        sys.stderr.flush()
        return True
    except ImportError as e:
        sys.stderr.write('FAILED\n')
        sys.stderr.flush()
        print e
        return False


imports = {'phaseshifts': ['libphsh', 'conphas', 'atorb']}

class Test(unittest.TestCase):
    """ Test class for imports """

    def testimports(self):
        """ Function to determine if modules in packages are importable 
        
        Returns
        -------
        FailsIf : any module cannot be imported from a given package 
        """
        for packages in imports:
            sys.stderr.write('Inspecting package: %s\n' % packages)
            successes = [ imp for imp in imports.get(packages) if isimportable('phaseshifts', imp)
                        ]
            self.failIf(len(successes) < len(imports.get(packages)))
            sys.stderr.write('Failed to import %i out of %i modules\n\n' % (
             len(imports.get(packages)) - len(successes),
             len(imports.get(packages))))
            sys.stderr.flush()


if __name__ == '__main__':
    sys.stderr.write('======================================================================\n')
    sys.stderr.write('TESTING: %s\n' % os.path.basename(__file__))
    sys.stderr.write('======================================================================\n')
    unittest.main()