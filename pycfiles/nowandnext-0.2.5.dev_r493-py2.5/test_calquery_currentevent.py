# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext_tests/test_calquery_currentevent.py
# Compiled at: 2009-05-11 19:02:40
import datetime, unittest
from nowandnext_tests.caltestcase import caltestcase
from nowandnext.timezones.utc import utc
from nowandnext.timezones.uk import uk

class test_calquery_currentevent(caltestcase):

    def dotestCurrentEvent(self, thetime, expectedshow):
        assert type(thetime) == datetime.datetime
        assert type(expectedshow) == str
        currentEventInstance = self._cal.getCurrentEventInstance(thetime)
        showtitle = currentEventInstance.getEvent().getTitle()
        assert showtitle == expectedshow, 'Expected: %s, got %s' % (expectedshow, showtitle)

    def testHootingYard1(self):
        self.dotestCurrentEvent(datetime.datetime(2008, 5, 29, 17, 30, 1, 0, utc), 'Hooting Yard')

    def testHootingYard2(self):
        self.dotestCurrentEvent(datetime.datetime(2008, 5, 29, 17, 59, 59, 0, utc), 'Hooting Yard')

    def testHootingYard3(self):
        self.dotestCurrentEvent(datetime.datetime(2008, 5, 29, 17, 59, 59, 0, tzinfo=uk), 'Hooting Yard')

    def testDeRidder1(self):
        self.dotestCurrentEvent(datetime.datetime(2008, 5, 26, 14, 59, 59, 0, utc), 'de Ridder Day')


if __name__ == '__main__':
    unittest.main()