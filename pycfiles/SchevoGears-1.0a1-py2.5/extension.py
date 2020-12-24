# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevogears/extension.py
# Compiled at: 2008-01-19 12:10:14
"""Schevo extensions for TurboGears.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from paste.script import templates
import turbogears
from turbogears.command import quickstart as tgquickstart
from turbogears import visit as tgvisit
from schevogears import visit as sgvisit
original = tgquickstart.quickstart

class quickstart(original):
    desc = 'Create a new Schevo/TurboGears project'

    def __init__(self, version):
        original.__init__(self, version)
        if self.templates:
            self.templates += ' schevo schevogears'
        else:
            self.templates = 'schevo schevogears'


def install():
    print 'Installing Schevo extensions for TurboGears.'
    tgquickstart.quickstart = quickstart
    tgvisit.start_extension = sgvisit.start_extension
    tgvisit.shutdown_extension = tgvisit.shutdown_extension


def tg_admin(argv):
    sys.argv = argv
    import turbogears.command
    return turbogears.command.main()