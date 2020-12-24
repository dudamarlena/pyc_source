# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guidjango/gui.py
# Compiled at: 2008-06-17 13:59:30
import os, sys, time, atexit, pickle
from os.path import dirname, join
import psi
from django.http import HttpResponse
try:
    from Foundation import NSURL
    from AppKit import NSWorkspace
    HAVE_PYOBJC = True
except ImportError:
    HAVE_PYOBJC = False

from tmpfile import pickledDataPath

def startDjango(port):
    """Start Django server in the background."""
    print 'Starting Django'
    path = join(dirname(__file__), 'manage.py')
    cmd = '/usr/local/bin/python2.5 %s runserver %s' % (path, port)
    atexit.register(stopDjango, cmd)
    os.system(cmd + ' &')


def stopDjango(cmd):
    """Stop Django server."""
    print 'Stopping Django'
    processTable = psi.process.ProcessTable()
    pids = processTable.pids
    processes = [ processTable.processes[i] for (i, pid) in enumerate(pids) ]
    psd = []
    for p in processes:
        try:
            args = p.args
        except:
            continue

        if (' ').join(p.args) == cmd:
            psd.append(p)

    for p in psd:
        print 'terminating %d (%s)' % (p.pid, (' ').join(p.args))
        os.system('kill -9 %d' % p.pid)

    os.remove(pickledDataPath)


def openPageInBrowser(url):
    time.sleep(1.5)
    if HAVE_PYOBJC:
        nsurl = NSURL.alloc().initWithString_(url)
        workspace = NSWorkspace.sharedWorkspace()
        workspace.openURL_(nsurl)
    elif sys.platform == 'darwin':
        cmd = 'osascript -e \'tell application "Firefox" to open location "%s"\'' % url
        os.system(cmd)
    else:
        print 'No idea how to open %s in a browser. Please DIY!' % url


def main(HEADER, TABLE, FOOTER):
    port = '8899'
    u = 'http://127.0.0.1:%s/test/' % port
    startDjango(port)
    data = (
     HEADER, TABLE, FOOTER[0])
    pickle.dump(data, open(pickledDataPath, 'w'))
    openPageInBrowser(u)
    try:
        while True:
            pass

    except:
        pass


def test():
    TABLE = '    size;file(fake)\n    608;crons\n    8;ex.csv\n    0;fonts\n    123;imm.dat\n    593;imm.license\n    8417;profile1.xml.odt\n    4240;UserDefaults.txt\n    9999;total'
    TABLE = [ line.split(';') for line in TABLE.split('\n') ]
    HEADER = TABLE[0]
    FOOTER = TABLE[(-1)]
    TABLE = TABLE[1:-1]
    main(HEADER, TABLE, FOOTER)


if __name__ == '__main__':
    try:
        TABLE = open(sys.argv[1]).read().strip()
    except IndexError:
        TABLE = '    size;file(fake)\n    608;crons\n    8;ex.csv\n    0;fonts\n    123;imm.dat\n    593;imm.license\n    8417;profile1.xml.odt\n    4240;UserDefaults.txt\n    9999;total'
    else:
        TABLE = [ line.split(';') for line in TABLE.split('\n') ]
        HEADER = TABLE[0]
        FOOTER = TABLE[(-1)]
        TABLE = TABLE[1:-1]
        main(HEADER, TABLE, FOOTER)