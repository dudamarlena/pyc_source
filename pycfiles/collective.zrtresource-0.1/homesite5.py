# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/zopeedit/Plugins/homesite5.py
# Compiled at: 2010-01-08 08:26:25
__doc__ = 'External Editor HomeSite Plugin\n\n$Id: homesite5.py 67450 2002-09-01 05:03:43Z caseman $\n'
from time import sleep
import win32com
from win32com import client

class EditorProcess:

    def __init__(self, file):
        """Launch editor process"""
        hs = win32com.client.Dispatch('AllaireClientApp.TAllaireClientApp')
        i = 0
        timeout = 45
        while i < timeout:
            try:
                hs.OpenFile(file)
            except:
                i += 1
                if i >= timeout:
                    raise RuntimeError('Could not launch Homesite.')
                sleep(1)
            else:
                break

        self.hs = hs
        self.file = file

    def wait(self, timeout):
        """Wait for editor to exit or until timeout"""
        sleep(timeout)

    def isAlive(self):
        """Returns true if the editor process is still alive"""
        return self.hs.IsFileOpen(self.file)


def test():
    import os
    from time import sleep
    from tempfile import mktemp
    fn = mktemp('.html')
    f = open(fn, 'w')
    f.write('<html>\n  <head></head>\n  <body>\n  </body>\n</html>')
    f.close()
    print 'Connecting to HomeSite...'
    f = EditorProcess(fn)
    print 'Attached to %s %s' % (`(f.hs)`, f.hs.VersionText)
    print '%s is open...' % fn,
    if f.isAlive():
        print 'yes'
        print 'Test Passed.'
    else:
        print 'no'
        print 'Test Failed.'


if __name__ == '__main__':
    test()