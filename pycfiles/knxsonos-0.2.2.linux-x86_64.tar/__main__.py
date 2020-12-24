# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/knxsonos/__main__.py
# Compiled at: 2016-04-16 10:28:54
from sys import argv
import cProfile
try:
    module_to_run = argv[1]
    argv = argv[1:]
    exec 'from %s import main' % module_to_run
except Exception as e:
    print 'Error: %s' % e
    print "usage: 'python -m knxsonos <filename>'"
    print "        the function 'main' in the specified file will be run"

main()