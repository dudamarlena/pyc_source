# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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