# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/__init__.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 1818 bytes
import os
os.chdir(os.path.dirname(__file__) or '.')
import sys, subprocess
from pybot.data import *
import pip
pyLoc = sys.executable
dependencies = {'tornado': 'tornado>=4.3', 'requests': 'requests>=2.9.1'}
get = {'https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.min.js': 'web\\Chart.min.js', 
 'https://raw.githubusercontent.com/dhg/Skeleton/master/css/normalize.css': 'web\\css\\normalize.css', 
 'https://raw.githubusercontent.com/dhg/Skeleton/master/css/skeleton.css': 'web\\css\\skeleton.css'}

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-run':
            print('Starting main pybot process...')
            subprocess.call([pyLoc, os.path.join(os.getcwd(), 'pybot_main.py')], cwd=os.getcwd())
        else:
            if sys.argv[1] == '-tests':
                subprocess.call([pyLoc, os.path.join(os.getcwd(), 'tests.py')], cwd=os.getcwd())
            else:
                if sys.argv[1] == '--config':
                    if len(sys.argv) > 2:
                        settings = Settings().getConf()
                        args = sys.argv[2].split('.')
                        settings.set(args[0], args[1], sys.argv[3])
                        with open('pybot.conf', 'w') as (configfile):
                            settings.write(configfile)
                    else:
                        print('Invalid use, type pybot -help')
                elif sys.argv[1] == '-help':
                    help()
    else:
        print('Invalid usage, type pybot -help')


def help():
    print('Pybot Help\n\t-run\tRuns pybot\n\t-setup\tCreates config file\n\t-help\tI really wonder...\n\n\t--config\n\t\tbot.name\n\t\tbot.auth\n\t\ttwitch.channel\n\t\tetc...')


if __name__ == '__main__':
    main()