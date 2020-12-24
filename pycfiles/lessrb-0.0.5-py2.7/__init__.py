# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lessrb/__init__.py
# Compiled at: 2012-04-12 15:26:48
import os, sys

def run():
    lessbin = os.path.join(os.path.dirname(__file__), 'rb', 'bin', 'lessc')
    if not os.access(lessbin, os.X_OK):
        os.chmod(lessbin, 493)
    os.execv(lessbin, ['lessc'] + sys.argv[1:])


if __name__ == '__main__':
    run()