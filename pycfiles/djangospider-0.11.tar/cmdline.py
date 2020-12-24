# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/djangospider-0.1-py2.7.egg/djangospider/monitor/cmdline.py
# Compiled at: 2016-02-28 00:58:07
import commands, os, sys

def Run_Django():
    print 'i come into Run_Django'
    path = os.path.split(os.path.realpath(__file__))[0]
    command1 = ' cd  %s ; python manage.py runserver ' % path
    status, output = commands.getstatusoutput(command1)
    print 'Run_Django status is %s' % status
    print output


if __name__ == '__main__':
    command1 = 'python manage.py runserver'
    status, output = commands.getstatusoutput(command1)