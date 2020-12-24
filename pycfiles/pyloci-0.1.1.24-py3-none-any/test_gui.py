# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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