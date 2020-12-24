# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/applications/schedule_to_digiguide.py
# Compiled at: 2009-05-11 19:02:38
"""
Generate an RSS feed of the schedule.
"""
import datetime, sys, logging
from nowandnext.utils.cmdline import cmdline
from nowandnext.utils.detectos import osinfo
from nowandnext.timezones.utc import utc
from nowandnext.calendar import periods
from nowandnext.calendar.scheduleevent import scheduleevent
from nowandnext.calendar.calQuery import CalQuery
from nowandnext.digiguide import dgxml
log = logging.getLogger(__name__)

class schedule_to_rss(cmdline):
    DAYS_PER_READ = 1

    def __init__(self, configfilepath):
        self._config = self.getconfiguration(configfilepath)
        self._calargs = (self._config.get('pinger', 'account'),
         self._config.get('pinger', 'password'),
         self._config.get('pinger', 'calendar_name'))
        self._channelname = self._config.get('digiguide', 'title')
        self._default_category = self._config.get('digiguide', 'default_category')
        self._days_in_schedule = int(self._config.get('digiguide', 'days'))

    def __call__(self):
        schedulevents = self.getcalendaritems()
        programs = [ dgxml.dgxmlfeed.program(i) for i in schedulevents ]
        channels = [
         dgxml.dgxmlfeed.channel(self._channelname, programs)]
        xml = dgxml.dgxmlfeed(channels)
        xml.dump(sys.stdout)

    def getcalendaritems(self):
        now = datetime.datetime.now(utc)
        eventinstances = []
        defaults = {'default_category': self._default_category}
        for day in range(0, self._days_in_schedule, self.DAYS_PER_READ):
            start = now + periods.oneday * day
            end = now + periods.oneday * (day + self.DAYS_PER_READ)
            log.info('Loading schedule for %s to %s' % (start, end))
            cal = CalQuery(*self._calargs)
            eventinstances.extend([ scheduleevent(a, **defaults) for a in cal.getEventInstances(start, end) ])

        return eventinstances


def main():
    logging.basicConfig()
    (options, args) = schedule_to_rss.mkParser().parse_args()
    if options.verbose:
        logging.getLogger('').setLevel(logging.INFO)
    else:
        logging.getLogger('').setLevel(logging.WARN)
    os_spesific_handler = osinfo.get_logger('Pinger')
    os_spesific_handler.setLevel(logging.WARN)
    logging.getLogger('').addHandler(os_spesific_handler)
    s2r = schedule_to_rss(options.configfilepath)
    s2r()


if __name__ == '__main__':
    main()