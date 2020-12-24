# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/applications/schedule_to_errors.py
# Compiled at: 2009-05-11 19:02:38
"""
Generate an RSS feed errors in the schedule.
"""
import PyRSS2Gen, datetime, sys, logging
from nowandnext.utils.cmdline import cmdline
from nowandnext.utils.detectos import osinfo
from nowandnext.timezones.utc import utc
from nowandnext.calendar import periods
from nowandnext.calendar.scheduleevent import scheduleevent
from nowandnext.calendar.calQuery import CalQuery, NoCalendarEntry
from nowandnext.calendar.detecterrorsinevent import DetectErrorsInEvent
log = logging.getLogger(__name__)

class schedule_to_rss(cmdline):

    @classmethod
    def mkParser(cls):
        parser = cmdline.mkParser()
        parser.add_option('--good', '-g', dest='good', help='Forget about the bad, focus on the good.', default=False, action='store_true')
        return parser

    def __init__(self, configfilepath, good=False):
        self._config = self.getconfiguration(configfilepath)
        self._good = good
        self._calargs = (self._config.get('pinger', 'account'),
         self._config.get('pinger', 'password'),
         self._config.get('pinger', 'calendar_name'))

    def filter(self, item):
        if self._good ^ (item.getErrorCount() > 0):
            return True
        return False

    def filterandconvertitems(self, calendaritems):
        for calendaritem in calendaritems:
            log.warn('Checking %s' % calendaritem)
            report = DetectErrorsInEvent(calendaritem)
            if self.filter(report):
                item = PyRSS2Gen.RSSItem(title=calendaritem.getTitle(), link=calendaritem.getWebLink(), description=report.getErrorHTMLList(), guid=calendaritem.getWebLink(), pubDate=calendaritem.getPublishDate())
                yield item

    def __call__(self):
        calendaritems = self.getcalendaritems()
        rss = PyRSS2Gen.RSS2(title=self._config.get('errors', 'title'), link=self._config.get('errors', 'link'), description=self._config.get('errors', 'description'), lastBuildDate=datetime.datetime.now(), items=self.filterandconvertitems(calendaritems))
        rss.write_xml(sys.stdout, encoding='utf-8')

    def getcalendaritems(self):
        now = datetime.datetime.now(utc)
        sometimeinthefuture = now + periods.onehour * 24 * 7
        cal = CalQuery(*self._calargs)
        events = []
        events.extend([ a for a in cal.getEvents(now, sometimeinthefuture) ])
        return events


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
    s2r = schedule_to_rss(options.configfilepath, options.good)
    s2r()


if __name__ == '__main__':
    main()