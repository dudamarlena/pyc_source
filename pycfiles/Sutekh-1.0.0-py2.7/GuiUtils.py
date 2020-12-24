# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/GuiUtils.py
# Compiled at: 2019-12-11 16:37:48
"""Various helpful functions that are generic enough to belong in base.gui"""
from __future__ import print_function
import os, gtk
from .SutekhDialog import do_complaint_error, do_exception_complaint, do_complaint_warning

def prepare_gui(sName):
    """Handle all the checks needed to ensure we can run the gui."""
    if gtk.gdk.screen_get_default() is None:
        print('Unable to find windowing system. Aborting')
        return False
    else:
        sMessage = gtk.check_version(2, 16, 0)
        if sMessage is not None:
            do_complaint_error('Incorrect gtk version. %s requires at least gtk 2.16.0.\nError reported %s' % (
             sName,
             sMessage))
            return False
        os.environ['UBUNTU_MENUPROXY'] = '0'
        return True


def load_config(cConfigFile, sRCFile):
    """Load the config and handle the checks needed before we
       start using it."""
    oConfig = cConfigFile(sRCFile)
    oConfig.validate()
    if not oConfig.check_writeable():
        iRes = do_complaint_warning('Unable to write to the config file %s.\nConfig changes will NOT be saved.\nDo you wish to continue?' % sRCFile)
        if iRes == gtk.RESPONSE_CANCEL:
            return None
    return oConfig


def save_config(oConfig):
    """Handle writing the config file and complaining if it fails."""
    try:
        oConfig.write()
    except IOError as oExp:
        sMesg = 'Unable to write the configuration file\nError was: %s' % oExp
        do_exception_complaint(sMesg)


def make_markup_button(sMarkup):
    """Create a gtk.Button using the given markup string for the label."""
    oBut = gtk.Button()
    oLabel = gtk.Label()
    oLabel.set_markup(sMarkup)
    oBut.add(oLabel)
    oBut.show_all()
    return oBut


def wrap(sText):
    """Return a gtk.Label which wraps the given text"""
    oLabel = gtk.Label()
    oLabel.set_line_wrap(True)
    oLabel.set_width_chars(80)
    oLabel.set_alignment(0, 0)
    oLabel.set_markup(sText)
    return oLabel