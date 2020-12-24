# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/rmopkgenv.py
# Compiled at: 2009-11-25 02:54:10
import Csys, os, os.path, sys, re
__doc__ = 'Clear OpenPKG instance variables from enviornment\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: rmopkgenv.py,v 1.2 2009/11/25 07:54:10 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]
skipKeys = {}.fromkeys(('_', 'RPM_BUILD_DIR', 'RPM_DOC_DIR', 'RPM_BUILD_ROOT', 'RPM_SOURCE_DIR',
                        'HOME', 'PWD', 'OLDPWD', 'TMPDIR'))

def rmopkgenv():
    l_prefix = Csys.prefix
    newenv = []
    for key, val in os.environ.items():
        if key not in skipKeys and val.find(l_prefix) != -1:
            parts = []
            for part in val.split(':'):
                if part.find(l_prefix) == -1:
                    parts.append(part)

            if not parts:
                del os.environ[key]
                cmd = 'unset ' + key
            else:
                val = os.environ[key] = (':').join(parts)
                cmd = '%s=%s\nexport %s' % (
                 key,
                 repr(val),
                 key)
            newenv.append(cmd)

    return newenv


if __name__ == '__main__':

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        return parser


    parser = setOptions()
    options, args = parser.parse_args()
    if options.verbose:
        verbose = '-v'
    else:
        verbose = ''
    Csys.getoptionsEnvironment(options)
    print ('\n').join(rmopkgenv())