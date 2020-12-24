# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/GNota/nosy.py
# Compiled at: 2007-07-27 21:10:31
import glob, os, stat, time

def checkSum():
    """ Return a long which can be used to know if any .py files have changed.
    Only looks in the current directory. """
    val = 0
    for f in glob.glob('*.py'):
        stats = os.stat(f)
        val += stats[stat.ST_SIZE] + stats[stat.ST_MTIME]

    for f in glob.glob('*.kid'):
        stats = os.stat(f)
        val += stats[stat.ST_SIZE] + stats[stat.ST_MTIME]

    return val


val = 0
while True:
    if checkSum() != val:
        val = checkSum()
        os.system('nosetests')
    time.sleep(1)