# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/actors/notify.py
# Compiled at: 2011-04-23 08:43:29
import gobject

class Notify(gobject.GObject):

    def __init__(self, core):
        gobject.GObject.__init__(self)
        self.gps_target_bearing_abs = None
        self.gps_target_distance = None
        return

    def __on_settings_changed(self, caller, settings, source):
        pass

    def __on_good_fix(self, caller, gps_data, distance, bearing):
        self.gps_target_distance = distance
        self.gps_target_bearing_abs = bearing - gps_data.bearing

    def __on_no_fix(self, caller, fix, msg):
        self.gps_target_distance = None
        self.gps_target_bearing_abs = None
        return