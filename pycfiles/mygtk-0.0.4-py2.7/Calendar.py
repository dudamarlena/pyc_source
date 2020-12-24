# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mygtk/Calendar.py
# Compiled at: 2018-03-04 09:50:47
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import os, sys, time, logging
from datetime import date
logger = logging.getLogger('Calendar')

class Calendar(Gtk.Calendar):

    def __init__(self):
        Gtk.Calendar.__init__(self)

    def get_datetime(self):
        logger.debug('get_datetime')
        year, month, day = self.get_date()
        month += 1
        mydate = date(year, month, day)
        return date(year, month, day)

    def get_real_date(self):
        year, month, day = self.get_date()
        month += 1
        logger.warning('return: %s', [year, month, day])
        return [year, month, day]