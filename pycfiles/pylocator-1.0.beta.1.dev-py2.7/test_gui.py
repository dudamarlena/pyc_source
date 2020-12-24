# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/tests/test_gui.py
# Compiled at: 2011-09-21 08:56:33
import gobject, gtk, getopt, sys, os
from pylocator.pylocator_mainwindow import PyLocatorMainWindow
from pylocator.shared import shared
from nose.tools import assert_raises
usage = 'usage: %s [options]\noptions:\n--help -h         print this message\n--filename -f     filename' % sys.argv[0]

def test_mainwindow_noargs():
    window = PyLocatorMainWindow()
    window.show()


def test_mainwindow():
    my_argv = [
     '-f', 'somestrangeand_inexistent_file.nii.gz']
    options, args = getopt.getopt(my_argv[:], 'hf:s:', ['help', 'filename', 'surface'])
    filename = None
    surface = None
    for option, value in options:
        if option in ('-h', '--help'):
            print usage
            sys.exit(0)
        if option in ('-f', '--file'):
            filename = value
        if option in ('-s', '--surface'):
            surface = value

    assert_raises(IOError, PyLocatorMainWindow, filename=filename, surface=surface)
    return