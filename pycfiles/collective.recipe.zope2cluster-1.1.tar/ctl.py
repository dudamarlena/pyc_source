# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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