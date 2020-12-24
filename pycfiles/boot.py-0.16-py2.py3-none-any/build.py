# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/build.py
# Compiled at: 2012-08-24 12:09:35
import sys, os
from subprocess import call
try:
    from boot_pkg import nanorc
except:
    pass

def make_desktop_launcher():
    """copy the boot launcher file from /usr/share/applications/ into 
       your ~/Desktop folder.
    """
    try:
        cmd = 'sudo chmod +x /usr/share/applications/boot.desktop'
        call(cmd.split())
        cmd = 'cp /usr/share/applications/boot.desktop ' + os.getenv('HOME') + '/Desktop/'
        call(cmd.split())
        cmd = 'sudo chown ' + os.getlogin() + ' ' + os.getenv('HOME') + '/Desktop/boot.desktop'
        call(cmd.split())
        cmd = 'sudo chgrp ' + os.getlogin() + ' ' + os.getenv('HOME') + '/Desktop/boot.desktop'
        call(cmd.split())
        print 'Desktop launcher file created.'
    except:
        print 'Problems in creating a desktop launcher file.'

    return 0


def build_all():
    """Download and install everything that is needed for boot to function 
       properly.
    """
    if 'linux' in sys.platform:
        call('clear')
        print 'Downloading and install necessary packages.'
        print 'You need to be connected to the Internet.\n'
        call(('sudo apt-get install ghdl gtkwave').split())
        make_desktop_launcher()
        nanorc.make()
        if True:
            call(('sudo apt-get install python-pip').split())
            call(('sudo apt-get install gtk2-engines-pixbuf').split())
            call(('sudo pip install argparse pygments mechanize').split())
        if True:
            call(('sudo apt-get install python-gtk2 python-gobject').split())
    elif 'darwin' in sys.platform:
        print 'Operating system not supported.'
    elif 'win32' in sys.platform:
        print 'Operating system not supported.'
    elif 'cygwin' in sys.platform:
        print 'Operating system not supported.'
    else:
        print 'Operating system not supported.'
    print 'All done.\n'
    return 0