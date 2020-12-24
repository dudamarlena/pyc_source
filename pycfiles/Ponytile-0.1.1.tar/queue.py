# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/queue.py
# Compiled at: 2011-09-15 18:59:45
__doc__ = 'Command-line tool to empty the ponyexpress qeueue\n\nUsage::\n\n\t\t$ python -m ponyexpress.queue\n\n'
import sys, manage
if __name__ == '__main__':
    outfile = sys.stdout
    outfile.write(manage.queue())