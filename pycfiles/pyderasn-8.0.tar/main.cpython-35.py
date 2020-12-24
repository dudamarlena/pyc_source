# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/python/main.py
# Compiled at: 2016-05-16 12:08:29
# Size of source mod 2**32: 2086 bytes
import sys
from builder import *

def help():
    print('\n    Hello! Welcome to Pyder.\n    Usage:\n      Pyder new STRING\n        Where STRING is the title of your site.\n      \n      Pyder help\n        Prints these docs\n\n    Flag options:\n      --no-config       \n        Generates the site without prompting to fill out a config.yml file.\n\n    @2016 Graham Hough, Ethan Miller\n    ')
    sys.exit()


if len(sys.argv) == 2:
    if str(sys.argv[1]).title() == 'Help':
        print(help())
    if str(sys.argv[1]).title() == 'H':
        print(help())
else:
    if len(sys.argv) == 3:
        if str(sys.argv[1]).title() != 'Post' and str(sys.argv[1]).title() != 'New':
            print(help())
        else:
            arg1 = str(sys.argv[1])
        arg2 = str(sys.argv[2])
    else:
        if len(sys.argv) == 4:
            if str(sys.argv[1]).title() != 'Post' and str(sys.argv[1]).title() != 'New':
                print(help())
            else:
                arg1 = str(sys.argv[1])
            arg2 = str(sys.argv[2])
            if str(sys.argv[3]) == '--no-config':
                arg3 = str(sys.argv[3])
            else:
                print('Invalid flag option')
                print(help())
        else:
            print('Incorrect arguments, please refer to the docs.')
            print(help())
        if 'arg1' in locals() and 'arg2' in locals() and arg1 == 'new':
            projectTitle = arg2
            print('New blog will be generated as ' + str(arg2))
            newSite = Site(str(arg2))
            newSite.directoryDraw()
            if 'arg3' in locals() and arg3 == '--no-config':
                print('Please fill out config.yml in your sites directory')
                newSite.noConfigDraw()
                newSite.configDraw()
            else:
                newSite.config()
                newSite.configDraw()