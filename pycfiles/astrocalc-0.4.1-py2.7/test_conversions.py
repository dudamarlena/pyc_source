# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/times/tests/test_conversions.py
# Compiled at: 2020-05-01 12:03:38
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml
from astrocalc.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser('~')
packageDirectory = utKit('').get_project_root()
settingsFile = packageDirectory + '/test_settings.yaml'
su = tools(arguments={'settingsFile': settingsFile}, docString=__doc__, logLevel='DEBUG', options_first=False, projectName=None, defaultSettingsFile=False)
arguments, settings, log, dbConn = su.setup()
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + '/input/'
pathToOutputDir = moduleDirectory + '/output/'
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

shutil.copytree(pathToInputDir, pathToOutputDir)
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_conversions(unittest.TestCase):

    def test_utdatetime_conversions_function(self):
        from astrocalc.times import conversions
        converter = conversions(log=log)
        print('\nUT = 20160426t144643.033433')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t144643.033433'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61577585013))
        print('\nUT = 20160426t144643.033433')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t144643.033433'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61577585013))
        print('\nUT = 20160426t144643.033433')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t144643.033433'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61577585013))
        print('\nUT = 20160426t1446')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t1446'))
        print(converter.mjd_to_ut_datetime(mjd=57504.6153))
        print('\nUT = 20160426t144643')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t144643'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61578))
        print('\nUT = 20160426t144643.033433')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426t144643.033433'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61577585013))
        print('\nUT = 20161231t234643.033433')
        print(converter.ut_datetime_to_mjd(utDatetime='20161231t234643.033433'))
        print(converter.ut_datetime_to_mjd(utDatetime='20161231t234643.033433'))
        print(converter.mjd_to_ut_datetime(mjd='57753.99077585013'))
        print('\nUT = 201604261444')
        print(converter.ut_datetime_to_mjd(utDatetime='201604261444'))
        print(converter.mjd_to_ut_datetime(mjd=57504.6139))
        print('\nUT = 20160426')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426'))
        print(converter.mjd_to_ut_datetime(mjd=57504.0))
        print('\nUT = 2016-04-26.33433')
        print(converter.ut_datetime_to_mjd(utDatetime='2016-04-26.33433'))
        print(converter.mjd_to_ut_datetime(mjd=57504.33411))
        print('\nUT = 20160426144444.5452')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426144444.5452'))
        print(converter.mjd_to_ut_datetime(mjd=57504.614404459))
        print('\nUT = 2016-04-26 14:44:44.234')
        print(converter.ut_datetime_to_mjd(utDatetime='2016-04-26 14:44:44.234'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61440086))
        print('\nUT = 20160426 14h44m44.432s')
        print(converter.ut_datetime_to_mjd(utDatetime='20160426 14h44m44.432s'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61440315))
        print('\nUT = 2016-04-26T14:44:44.234')
        print(converter.ut_datetime_to_mjd(utDatetime='2016-04-26T14:44:44.234'))
        print(converter.mjd_to_ut_datetime(mjd=57504.61440086, sqlDate=True))

    def test_mjd_conversions_function(self):
        from astrocalc.times import conversions
        converter = conversions(log=log)
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))
        print(converter.mjd_to_ut_datetime(mjd=57504.6144))

    def test_decimal_day_to_day_hour_min_sec_function(self):
        from astrocalc.times import conversions
        converter = conversions(log=log)
        daysInt, hoursInt, minsInt, secFloat = converter.decimal_day_to_day_hour_min_sec(daysFloat=24.2453)
        print('%(daysInt)s days, %(hoursInt)s hours, %(minsInt)s mins, %(secFloat)s sec' % locals())
        daysInt, hoursInt, minsInt, secFloat = converter.decimal_day_to_day_hour_min_sec(daysFloat=24.12345)
        print('%(daysInt)s days, %(hoursInt)s hours, %(minsInt)s mins, %(secFloat)s sec' % locals())
        daysInt, hoursInt, minsInt, secFloat = converter.decimal_day_to_day_hour_min_sec(daysFloat=24.2)
        print('%(daysInt)s days, %(hoursInt)s hours, %(minsInt)s mins, %(secFloat)s sec' % locals())
        daysInt, hoursInt, minsInt, secFloat = converter.decimal_day_to_day_hour_min_sec(daysFloat=24.1232435454)
        print('%(daysInt)s days, %(hoursInt)s hours, %(minsInt)s mins, %(secFloat)s sec' % locals())