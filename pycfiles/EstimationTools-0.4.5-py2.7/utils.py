# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/estimationtools/utils.py
# Compiled at: 2011-09-05 07:25:07
import urllib, urllib2
from datetime import datetime
from time import strptime
from trac.config import Option, ListOption, BoolOption
from trac.core import TracError, Component, implements
from trac.web.api import IRequestFilter, IRequestHandler, RequestDone
from trac.wiki.api import parse_args
from trac.ticket.query import Query
from trac.util.text import unicode_urlencode
from trac.util.datefmt import utc
try:
    from trac.util.datefmt import from_utimestamp as from_timestamp
except ImportError:

    def from_timestamp(ts):
        return datetime.fromtimestamp(ts, utc)


AVAILABLE_OPTIONS = ['startdate', 'enddate', 'today', 'width', 'height',
 'color', 'bgcolor', 'wecolor', 'weekends', 'gridlines',
 'expected', 'colorexpected', 'title']

def get_estimation_field():
    return Option('estimation-tools', 'estimation_field', 'estimatedhours', doc="Defines what custom field should be used to calculate estimation charts.\n        Defaults to 'estimatedhours'")


def get_closed_states():
    return ListOption('estimation-tools', 'closed_states', 'closed', doc='Set to a comma separated list of workflow states that count as "closed",\n        where the effort will be treated as zero, e.g. closed_states=closed,another_state.\n        Defaults to closed.')


def get_estimation_suffix():
    return Option('estimation-tools', 'estimation_suffix', 'h', doc="Suffix used for estimations. Defaults to 'h'")


def get_serverside_charts():
    return BoolOption('estimation-tools', 'serverside_charts', 'false', doc='Generate charts links internally and fetch charts server-side\n        before returning to client, instead of generating Google links that the\n        users browser fetches directly. Particularly useful for sites served behind SSL.\n        Server-side charts uses POST requests internally, increasing chart data size\n        from 2K to 16K. Defaults to false.')


class EstimationToolsBase(Component):
    """ Base class EstimationTools components that auto-disables if
    estimation field is not properly configured. """
    abstract = True
    estimation_field = get_estimation_field()

    def __init__(self, *args, **kwargs):
        if not self.env.config.has_option('ticket-custom', self.estimation_field):
            self.log.error('EstimationTools (%s): Estimation field not configured. Component disabled.' % (
             self.__class__.__name__,))
            self.env.disable_component(self)


class GoogleChartProxy(EstimationToolsBase):
    """ A Google Chart API proxy handler that moves chart fetching server-side.
    Implemented to allow serving the charts under SSL encryption between client
    and server - without the nagging error messages."""
    implements(IRequestHandler)

    def match_request(self, req):
        return req.path_info == '/estimationtools/chart'

    def process_request(self, req):
        req.perm.require('TICKET_VIEW')
        data = req.args.get('data', '')
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        chart_req = urllib2.Request('http://chart.apis.google.com/chart', data=data)
        self.log.debug('Fetch chart, %r + data: %r' % (chart_req.get_method(), data))
        chart = opener.open(chart_req)
        for header, value in chart.headers.items():
            req.send_header(header, value)

        req.write(chart.read())
        raise RequestDone


def parse_options(db, content, options):
    """Parses the parameters, makes some sanity checks, and creates default values
    for missing parameters.
    """
    cursor = db.cursor()
    _, parsed_options = parse_args(content, strict=False)
    options.update(parsed_options)
    today = datetime.now().date()
    startdatearg = options.get('startdate')
    if startdatearg:
        options['startdate'] = datetime(*strptime(startdatearg, '%Y-%m-%d')[0:5]).date()
    enddatearg = options.get('enddate')
    options['enddate'] = None
    if enddatearg:
        options['enddate'] = datetime(*strptime(enddatearg, '%Y-%m-%d')[0:5]).date()
    if not options['enddate'] and options.get('milestone'):
        milestone = options['milestone'].split('|')[0]
        cursor.execute('SELECT completed, due FROM milestone WHERE name = %s', [milestone])
        row = cursor.fetchone()
        if not row:
            raise TracError("Couldn't find milestone %s" % milestone)
        if row[0]:
            options['enddate'] = from_timestamp(row[0]).date()
        elif row[1]:
            due = from_timestamp(row[1]).date()
            if due >= today:
                options['enddate'] = due
    options['enddate'] = options['enddate'] or today
    options['today'] = options.get('today') or today
    if options.get('weekends'):
        options['weekends'] = parse_bool(options['weekends'])
    query_args = {}
    for key in options.keys():
        if key not in AVAILABLE_OPTIONS:
            query_args[key] = options[key]

    return (
     options, query_args)


def execute_query(env, req, query_args):
    query_args['max'] = 0
    query_string = unicode_urlencode(query_args).replace('%21=', '!=').replace('%7C', '|').replace('+', ' ').replace('%23', '#').replace('%28', '(').replace('%29', ')')
    env.log.debug('query_string: %s' % query_string)
    query = Query.from_string(env, query_string)
    tickets = query.execute(req)
    tickets = [ t for t in tickets if ('TICKET_VIEW' or 'TICKET_VIEW_CC') in req.perm('ticket', t['id'])
              ]
    return tickets


def parse_bool(s):
    if s is True or s is False:
        return s
    s = str(s).strip().lower()
    return s not in ('false', 'f', 'n', '0', '')


def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k, v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = [
                 v]

    return d