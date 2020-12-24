# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeb/code/git/WeatherAlerts/tests/test_weatheralerts.py
# Compiled at: 2017-03-27 22:08:29
# Size of source mod 2**32: 3005 bytes
import os, sys
sys.path.insert(0, os.path.abspath('..'))
import unittest
from weatheralerts import WeatherAlerts

class Test_WeatherAlerts(unittest.TestCase):

    def setUp(self):
        self.nws = WeatherAlerts()

    def test_almost_everything(self):
        print('Alerts currently in feed {0}'.format(len(self.nws.alerts)))

    def test_event_state_counties(self):
        self.nws.event_state_counties()

    def test_samecode_alerts_method(self):
        self.nws.samecode_alerts('016027')

    def test_refresh(self):
        self.nws.refresh()

    def test_refresh_forced(self):
        self.nws.refresh(force=True)

    def test_county_state_alerts(self):
        self.nws.county_state_alerts('canyon', 'ID')

    def test_alert_attributes(self):
        for alert in self.nws.alerts:
            x = alert.title
            x = alert.summary
            x = alert.areadesc
            x = alert.event
            x = alert.samecodes
            x = alert.zonecodes
            x = alert.expiration
            x = alert.updated
            x = alert.effective
            x = alert.published
            x = alert.severity
            x = alert.category
            x = alert.urgency

    def test_passing_samecodes(self):
        testobjs = []
        testobjs.append(WeatherAlerts(samecodes='016027'))
        testobjs.append(WeatherAlerts(samecodes=['016027', '016001', '016073', '016075']))
        samecodes = list(self.nws.geo.samecodes.keys())
        testobjs.append(WeatherAlerts(samecodes=samecodes))
        for nws in testobjs:
            for alert in nws.alerts:
                x = alert.title
                x = alert.summary
                x = alert.areadesc
                x = alert.event
                x = alert.samecodes
                x = alert.zonecodes
                x = alert.expiration
                x = alert.updated
                x = alert.effective
                x = alert.published
                x = alert.severity
                x = alert.category
                x = alert.urgency

    def test_passing_state(self):
        nws = WeatherAlerts(state='ID')
        for alert in nws.alerts:
            x = alert.title
            x = alert.summary
            x = alert.areadesc
            x = alert.event
            x = alert.samecodes
            x = alert.zonecodes
            x = alert.expiration
            x = alert.updated
            x = alert.effective
            x = alert.published
            x = alert.severity
            x = alert.category
            x = alert.urgency

    def test_break_on_samecodes(self):
        """break if you pass in non str/list samecodes"""
        try:
            nws = WeatherAlerts(samecodes=1)
        except Exception:
            pass
        else:
            raise Exception("That shouldn't have worked")


if __name__ == '__main__':
    unittest.main()