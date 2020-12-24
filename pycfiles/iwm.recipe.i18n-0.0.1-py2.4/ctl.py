# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iwm/recipe/i18n/ctl.py
# Compiled at: 2007-08-29 08:42:02
import os, sys, getopt, i18nmergeall

def main_i18nmergeall():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'l:h', [
         'help', 'locals-dir='])
    except getopt.error, msg:
        i18nmergeall.usage(1, msg)

    path = None
    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            i18nmergeall.usage(0)
        elif opt in ('-l', '--locales-dir'):
            cwd = os.getcwd()
            if os.environ.has_key('PWD'):
                cwd = os.environ['PWD']
            path = os.path.normpath(os.path.join(cwd, arg))

    if path is None:
        i18nmergeall.usage(1, 'You must specify the path to the locales directory.')
    i18nmergeall.main(path)
    return