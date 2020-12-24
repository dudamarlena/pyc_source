# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/recipe/z2testrunner/ctl.py
# Compiled at: 2009-02-17 13:06:48
import subprocess, sys

def run(args):
    (scr, defaults, packages, modules, extrapath, exitwithstatus) = args
    cmdargs = [
     scr, 'test']
    cmdargs.extend(defaults)
    cmdargs.extend([ '-s' + x for x in packages ])
    cmdargs.extend([ '-m' + x for x in modules ])
    cmdargs.extend([ '--path ' + x for x in extrapath ])
    if exitwithstatus:
        cmdargs.append('--exit-with-status')
    cmdargs.extend(sys.argv[1:])
    return sys.exit(subprocess.call(cmdargs))