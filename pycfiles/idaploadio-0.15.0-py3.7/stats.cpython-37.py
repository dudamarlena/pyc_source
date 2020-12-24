# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/stats.py
# Compiled at: 2020-04-15 05:34:35
# Size of source mod 2**32: 32860 bytes
import hashlib, time
from collections import namedtuple, OrderedDict
from copy import copy
from itertools import chain
import gevent
from .exception import StopLocust
from .log import console_logger
STATS_NAME_WIDTH = 60
STATS_TYPE_WIDTH = 20
CSV_STATS_INTERVAL_SEC = 2
CONSOLE_STATS_INTERVAL_SEC = 2
CURRENT_RESPONSE_TIME_PERCENTILE_WINDOW = 10
CachedResponseTimes = namedtuple('CachedResponseTimes', ['response_times', 'num_requests'])
PERCENTILES_TO_REPORT = [
 0.5,
 0.66,
 0.75,
 0.8,
 0.9,
 0.95,
 0.98,
 0.99,
 0.999,
 0.9999,
 0.99999,
 1.0]

class RequestStatsAdditionError(Exception):
    pass


def calculate_response_time_percentile(response_times, num_requests, percent):
    """
    Get the response time that a certain number of percent of the requests
    finished within. Arguments:
    
    response_times: A StatsEntry.response_times dict
    num_requests: Number of request made (could be derived from response_times, 
                  but we save some CPU cycles by using the value which we already store)
    percent: The percentile we want to calculate. Specified in range: 0.0 - 1.0
    """
    num_of_request = int(num_requests * percent)
    processed_count = 0
    for response_time in sorted((response_times.keys()), reverse=True):
        processed_count += response_times[response_time]
        if num_requests - processed_count <= num_of_request:
            return response_time

    return 0


def diff_response_time_dicts(latest, old):
    """
    Returns the delta between two {response_times:request_count} dicts.
    
    Used together with the response_times cache to get the response times for the 
    last X seconds, which in turn is used to calculate the current response time 
    percentiles.
    """
    new = {}
    for time in latest:
        diff = latest[time] - old.get(time, 0)
        if diff:
            new[time] = diff

    return new


class RequestStats(object):

    def __init__(self):
        self.entries = {}
        self.errors = {}
        self.total = StatsEntry(self, 'Aggregated', None, use_response_times_cache=True)

    @property
    def num_requests(self):
        return self.total.num_requests

    @property
    def num_none_requests(self):
        return self.total.num_none_requests

    @property
    def num_failures(self):
        return self.total.num_failures

    @property
    def last_request_timestamp(self):
        return self.total.last_request_timestamp

    @property
    def start_time(self):
        return self.total.start_time

    def log_request(self, method, name, response_time, content_length):
        self.total.log(response_time, content_length)
        self.get(name, method).log(response_time, content_length)

    def log_error(self, method, name, error):
        self.total.log_error(error)
        self.get(name, method).log_error(error)
        key = StatsError.create_key(method, name, error)
        entry = self.errors.get(key)
        if not entry:
            entry = StatsError(method, name, error)
            self.errors[key] = entry
        entry.occurred()

    def get(self, name, method):
        """
        Retrieve a StatsEntry instance by name and method
        """
        entry = self.entries.get((name, method))
        if not entry:
            entry = StatsEntry(self, name, method, True)
            self.entries[(name, method)] = entry
        return entry

    def reset_all(self):
        """
        Go through all stats entries and reset them to zero
        """
        self.total.reset()
        self.errors = {}
        for r in self.entries.values():
            r.reset()

    def clear_all(self):
        """
        Remove all stats entries and errors
        """
        self.total = StatsEntry(self, 'Aggregated', None, use_response_times_cache=True)
        self.entries = {}
        self.errors = {}

    def serialize_stats(self):
        return [self.entries[key].num_failures == 0 or self.entries[key].get_stripped_report() for key in self.entries.keys() if self.entries[key].num_requests == 0]

    def serialize_errors(self):
        return dict([(k, e.to_dict()) for k, e in self.errors.items()])


class StatsEntry(object):
    __doc__ = '\n    Represents a single stats entry (name and method)\n    '
    name = None
    method = None
    num_requests = None
    num_none_requests = None
    num_failures = None
    total_response_time = None
    min_response_time = None
    max_response_time = None
    num_reqs_per_sec = None
    num_fail_per_sec = None
    response_times = None
    use_response_times_cache = False
    response_times_cache = None
    total_content_length = None
    start_time = None
    last_request_timestamp = None

    def __init__(self, stats, name, method, use_response_times_cache=False):
        self.stats = stats
        self.name = name
        self.method = method
        self.use_response_times_cache = use_response_times_cache
        self.reset()

    def reset(self):
        self.start_time = time.time()
        self.num_requests = 0
        self.num_none_requests = 0
        self.num_failures = 0
        self.total_response_time = 0
        self.response_times = {}
        self.min_response_time = None
        self.max_response_time = 0
        self.last_request_timestamp = None
        self.num_reqs_per_sec = {}
        self.num_fail_per_sec = {}
        self.total_content_length = 0
        if self.use_response_times_cache:
            self.response_times_cache = OrderedDict()
            self._cache_response_times(int(time.time()))

    def log(self, response_time, content_length):
        current_time = time.time()
        t = int(current_time)
        if self.use_response_times_cache:
            if self.last_request_timestamp:
                if t > int(self.last_request_timestamp):
                    self._cache_response_times(t - 1)
        self.num_requests += 1
        self._log_time_of_request(current_time)
        self._log_response_time(response_time)
        self.total_content_length += content_length

    def _log_time_of_request(self, current_time):
        t = int(current_time)
        self.num_reqs_per_sec[t] = self.num_reqs_per_sec.setdefault(t, 0) + 1
        self.last_request_timestamp = current_time

    def _log_response_time(self, response_time):
        if response_time is None:
            self.num_none_requests += 1
            return
        else:
            self.total_response_time += response_time
            if self.min_response_time is None:
                self.min_response_time = response_time
            else:
                self.min_response_time = min(self.min_response_time, response_time)
                self.max_response_time = max(self.max_response_time, response_time)
                if response_time < 100:
                    rounded_response_time = round(response_time)
                else:
                    if response_time < 1000:
                        rounded_response_time = round(response_time, -1)
                    else:
                        if response_time < 10000:
                            rounded_response_time = round(response_time, -2)
                        else:
                            rounded_response_time = round(response_time, -3)
        self.response_times.setdefault(rounded_response_time, 0)
        self.response_times[rounded_response_time] += 1

    def log_error(self, error):
        self.num_failures += 1
        t = int(time.time())
        self.num_fail_per_sec[t] = self.num_fail_per_sec.setdefault(t, 0) + 1

    @property
    def fail_ratio(self):
        try:
            return float(self.num_failures) / self.num_requests
        except ZeroDivisionError:
            if self.num_failures > 0:
                return 1.0
            return 0.0

    @property
    def avg_response_time(self):
        try:
            return float(self.total_response_time) / (self.num_requests - self.num_none_requests)
        except ZeroDivisionError:
            return 0

    @property
    def median_response_time(self):
        if not self.response_times:
            return 0
        else:
            median = median_from_dict(self.num_requests - self.num_none_requests, self.response_times) or 0
            if median > self.max_response_time:
                median = self.max_response_time
            else:
                if median < self.min_response_time:
                    median = self.min_response_time
        return median

    @property
    def current_rps(self):
        if self.stats.last_request_timestamp is None:
            return 0
        slice_start_time = max(int(self.stats.last_request_timestamp) - 12, int(self.stats.start_time or 0))
        reqs = [self.num_reqs_per_sec.get(t, 0) for t in range(slice_start_time, int(self.stats.last_request_timestamp) - 2)]
        return avg(reqs)

    @property
    def current_fail_per_sec(self):
        if self.stats.last_request_timestamp is None:
            return 0
        slice_start_time = max(int(self.stats.last_request_timestamp) - 12, int(self.stats.start_time or 0))
        reqs = [self.num_fail_per_sec.get(t, 0) for t in range(slice_start_time, int(self.stats.last_request_timestamp) - 2)]
        return avg(reqs)

    @property
    def total_rps(self):
        return self.stats.last_request_timestamp and self.stats.start_time or 0.0
        try:
            return self.num_requests / (self.stats.last_request_timestamp - self.stats.start_time)
        except ZeroDivisionError:
            return 0.0

    @property
    def total_fail_per_sec(self):
        return self.stats.last_request_timestamp and self.stats.start_time or 0.0
        try:
            return self.num_failures / (self.stats.last_request_timestamp - self.stats.start_time)
        except ZeroDivisionError:
            return 0.0

    @property
    def avg_content_length(self):
        try:
            return self.total_content_length / self.num_requests
        except ZeroDivisionError:
            return 0

    def extend(self, other):
        """
        Extend the data from the current StatsEntry with the stats from another
        StatsEntry instance. 
        """
        if self.last_request_timestamp is not None and other.last_request_timestamp is not None:
            self.last_request_timestamp = max(self.last_request_timestamp, other.last_request_timestamp)
        else:
            if other.last_request_timestamp is not None:
                self.last_request_timestamp = other.last_request_timestamp
            else:
                self.start_time = min(self.start_time, other.start_time)
                self.num_requests = self.num_requests + other.num_requests
                self.num_none_requests = self.num_none_requests + other.num_none_requests
                self.num_failures = self.num_failures + other.num_failures
                self.total_response_time = self.total_response_time + other.total_response_time
                self.max_response_time = max(self.max_response_time, other.max_response_time)
                if self.min_response_time is not None and other.min_response_time is not None:
                    self.min_response_time = min(self.min_response_time, other.min_response_time)
                else:
                    if other.min_response_time is not None:
                        self.min_response_time = other.min_response_time
            self.total_content_length = self.total_content_length + other.total_content_length
            for key in other.response_times:
                self.response_times[key] = self.response_times.get(key, 0) + other.response_times[key]

            for key in other.num_reqs_per_sec:
                self.num_reqs_per_sec[key] = self.num_reqs_per_sec.get(key, 0) + other.num_reqs_per_sec[key]

            for key in other.num_fail_per_sec:
                self.num_fail_per_sec[key] = self.num_fail_per_sec.get(key, 0) + other.num_fail_per_sec[key]

    def serialize(self):
        return {'name':self.name,  'method':self.method, 
         'last_request_timestamp':self.last_request_timestamp, 
         'start_time':self.start_time, 
         'num_requests':self.num_requests, 
         'num_none_requests':self.num_none_requests, 
         'num_failures':self.num_failures, 
         'total_response_time':self.total_response_time, 
         'max_response_time':self.max_response_time, 
         'min_response_time':self.min_response_time, 
         'total_content_length':self.total_content_length, 
         'response_times':self.response_times, 
         'num_reqs_per_sec':self.num_reqs_per_sec, 
         'num_fail_per_sec':self.num_fail_per_sec}

    @classmethod
    def unserialize(cls, data):
        obj = cls(None, data['name'], data['method'])
        for key in ('last_request_timestamp', 'start_time', 'num_requests', 'num_none_requests',
                    'num_failures', 'total_response_time', 'max_response_time', 'min_response_time',
                    'total_content_length', 'response_times', 'num_reqs_per_sec',
                    'num_fail_per_sec'):
            setattr(obj, key, data[key])

        return obj

    def get_stripped_report(self):
        """
        Return the serialized version of this StatsEntry, and then clear the current stats.
        """
        report = self.serialize()
        self.reset()
        return report

    def to_string(self, current=True):
        """
        Return the stats as a string suitable for console output. If current is True, it'll show 
        the RPS and failure rait for the last 10 seconds. If it's false, it'll show the total stats 
        for the whole run.
        """
        if current:
            rps = self.current_rps
            fail_per_sec = self.current_fail_per_sec
        else:
            rps = self.total_rps
            fail_per_sec = self.total_fail_per_sec
        return (' %-' + str(STATS_NAME_WIDTH) + 's %7d %12s %7d %7d %7d  | %7d %7.2f %7.2f') % (
         (self.method and self.method + ' ' or '') + self.name,
         self.num_requests,
         '%d(%.2f%%)' % (self.num_failures, self.fail_ratio * 100),
         self.avg_response_time,
         self.min_response_time or 0,
         self.max_response_time,
         self.median_response_time or 0,
         rps or 0,
         fail_per_sec or 0)

    def __str__(self):
        return self.to_string(current=True)

    def get_response_time_percentile(self, percent):
        """
        Get the response time that a certain number of percent of the requests
        finished within.
        
        Percent specified in range: 0.0 - 1.0
        """
        return calculate_response_time_percentile(self.response_times, self.num_requests, percent)

    def get_current_response_time_percentile(self, percent):
        """
        Calculate the *current* response time for a certain percentile. We use a sliding 
        window of (approximately) the last 10 seconds (specified by CURRENT_RESPONSE_TIME_PERCENTILE_WINDOW) 
        when calculating this.
        """
        if not self.use_response_times_cache:
            raise ValueError('StatsEntry.use_response_times_cache must be set to True if we should be able to calculate the _current_ response time percentile')
        t = int(time.time())
        acceptable_timestamps = []
        for i in range(9):
            acceptable_timestamps.append(t - CURRENT_RESPONSE_TIME_PERCENTILE_WINDOW - i)
            acceptable_timestamps.append(t - CURRENT_RESPONSE_TIME_PERCENTILE_WINDOW + i)

        cached = None
        for ts in acceptable_timestamps:
            if ts in self.response_times_cache:
                cached = self.response_times_cache[ts]
                break

        if cached:
            return calculate_response_time_percentile(diff_response_time_dicts(self.response_times, cached.response_times), self.num_requests - cached.num_requests, percent)

    def percentile(self, tpl=' %-' + str(STATS_TYPE_WIDTH) + 's %-' + str(STATS_NAME_WIDTH) + 's %8d %6d %6d %6d %6d %6d %6d %6d %6d %6d %6d %6d'):
        if not self.num_requests:
            raise ValueError("Can't calculate percentile on url with no successful requests")
        return tpl % (
         self.method,
         self.name,
         self.num_requests,
         self.get_response_time_percentile(0.5),
         self.get_response_time_percentile(0.66),
         self.get_response_time_percentile(0.75),
         self.get_response_time_percentile(0.8),
         self.get_response_time_percentile(0.9),
         self.get_response_time_percentile(0.95),
         self.get_response_time_percentile(0.98),
         self.get_response_time_percentile(0.99),
         self.get_response_time_percentile(0.999),
         self.get_response_time_percentile(0.9999),
         self.get_response_time_percentile(1.0))

    def _cache_response_times(self, t):
        self.response_times_cache[t] = CachedResponseTimes(response_times=(copy(self.response_times)),
          num_requests=(self.num_requests))
        cache_size = CURRENT_RESPONSE_TIME_PERCENTILE_WINDOW + 10
        if len(self.response_times_cache) > cache_size:
            for i in range(len(self.response_times_cache) - cache_size):
                self.response_times_cache.popitem(last=False)


class StatsError(object):

    def __init__(self, method, name, error, occurrences=0):
        self.method = method
        self.name = name
        self.error = error
        self.occurrences = occurrences

    @classmethod
    def parse_error(cls, error):
        string_error = repr(error)
        target = 'object at 0x'
        target_index = string_error.find(target)
        if target_index < 0:
            return string_error
        start = target_index + len(target) - 2
        end = string_error.find('>', start)
        if end < 0:
            return string_error
        hex_address = string_error[start:end]
        return string_error.replace(hex_address, '0x....')

    @classmethod
    def create_key(cls, method, name, error):
        key = '%s.%s.%r' % (method, name, StatsError.parse_error(error))
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def occurred(self):
        self.occurrences += 1

    def to_name(self):
        return '%s %s: %r' % (self.method,
         self.name, repr(self.error))

    def to_dict(self):
        return {'method':self.method, 
         'name':self.name, 
         'error':StatsError.parse_error(self.error), 
         'occurrences':self.occurrences}

    @classmethod
    def from_dict(cls, data):
        return cls(data['method'], data['name'], data['error'], data['occurrences'])


def avg(values):
    return sum(values, 0.0) / max(len(values), 1)


def median_from_dict(total, count):
    """
    total is the number of requests made
    count is a dict {response_time: count}
    """
    pos = (total - 1) / 2
    for k in sorted(count.keys()):
        if pos < count[k]:
            return k
        pos -= count[k]


def setup_distributed_stats_event_listeners(events, stats):

    def on_report_to_master(client_id, data):
        data['stats'] = stats.serialize_stats()
        data['stats_total'] = stats.total.get_stripped_report()
        data['errors'] = stats.serialize_errors()
        stats.errors = {}

    def on_slave_report(client_id, data):
        for stats_data in data['stats']:
            entry = StatsEntry.unserialize(stats_data)
            request_key = (entry.name, entry.method)
            if request_key not in stats.entries:
                stats.entries[request_key] = StatsEntry(stats, entry.name, entry.method)
            stats.entries[request_key].extend(entry)

        for error_key, error in data['errors'].items():
            if error_key not in stats.errors:
                stats.errors[error_key] = StatsError.from_dict(error)
            else:
                stats.errors[error_key].occurrences += error['occurrences']

        old_last_request_timestamp = stats.total.last_request_timestamp
        stats.total.extend(StatsEntry.unserialize(data['stats_total']))
        if stats.total.last_request_timestamp:
            if stats.total.last_request_timestamp > (old_last_request_timestamp or 0):
                stats.total._cache_response_times(int(stats.total.last_request_timestamp))

    events.report_to_master.add_listener(on_report_to_master)
    events.slave_report.add_listener(on_slave_report)


def print_stats(stats, current=True):
    console_logger.info((' %-' + str(STATS_NAME_WIDTH) + 's %7s %12s %7s %7s %7s  | %7s %7s %7s') % ('Name',
                                                                                                     '# reqs',
                                                                                                     '# fails',
                                                                                                     'Avg',
                                                                                                     'Min',
                                                                                                     'Max',
                                                                                                     'Median',
                                                                                                     'req/s',
                                                                                                     'failures/s'))
    console_logger.info('-' * (80 + STATS_NAME_WIDTH))
    for key in sorted(stats.entries.keys()):
        r = stats.entries[key]
        console_logger.info(r.to_string(current=current))

    console_logger.info('-' * (80 + STATS_NAME_WIDTH))
    console_logger.info(stats.total.to_string(current=current))
    console_logger.info('')


def print_percentile_stats(stats):
    console_logger.info('Percentage of the requests completed within given times')
    console_logger.info((' %-' + str(STATS_TYPE_WIDTH) + 's %-' + str(STATS_NAME_WIDTH) + 's %8s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s') % ('Type',
                                                                                                                                                  'Name',
                                                                                                                                                  '# reqs',
                                                                                                                                                  '50%',
                                                                                                                                                  '66%',
                                                                                                                                                  '75%',
                                                                                                                                                  '80%',
                                                                                                                                                  '90%',
                                                                                                                                                  '95%',
                                                                                                                                                  '98%',
                                                                                                                                                  '99%',
                                                                                                                                                  '99.9%',
                                                                                                                                                  '99.99%',
                                                                                                                                                  '100%'))
    console_logger.info('-' * (90 + STATS_NAME_WIDTH))
    for key in sorted(stats.entries.keys()):
        r = stats.entries[key]
        if r.response_times:
            console_logger.info(r.percentile())

    console_logger.info('-' * (90 + STATS_NAME_WIDTH))
    if stats.total.response_times:
        console_logger.info(stats.total.percentile())
    console_logger.info('')


def print_error_report(stats):
    if not len(stats.errors):
        return
    console_logger.info('Error report')
    console_logger.info(' %-18s %-100s' % ('# occurrences', 'Error'))
    console_logger.info('-' * (80 + STATS_NAME_WIDTH))
    for error in stats.errors.values():
        console_logger.info(' %-18i %-100s' % (error.occurrences, error.to_name()))

    console_logger.info('-' * (80 + STATS_NAME_WIDTH))
    console_logger.info('')


def stats_printer(stats):

    def stats_printer_func():
        while True:
            print_stats(stats)
            gevent.sleep(CONSOLE_STATS_INTERVAL_SEC)

    return stats_printer_func


def stats_writer(stats, base_filepath, stats_history_enabled=False):
    """Writes the csv files for the idapload run."""
    with open(base_filepath + '_stats_history.csv', 'w') as (f):
        f.write(stats_history_csv_header())
    while True:
        write_stat_csvs(stats, base_filepath, stats_history_enabled)
        gevent.sleep(CSV_STATS_INTERVAL_SEC)


def write_stat_csvs(stats, base_filepath, stats_history_enabled=False):
    """Writes the requests, distribution, and failures csvs."""
    with open(base_filepath + '_stats.csv', 'w') as (f):
        f.write(requests_csv(stats))
    with open(base_filepath + '_stats_history.csv', 'a') as (f):
        f.write(stats_history_csv(stats, stats_history_enabled) + '\n')
    with open(base_filepath + '_failures.csv', 'w') as (f):
        f.write(failures_csv(stats))


def sort_stats(stats):
    return [stats[key] for key in sorted(stats.keys())]


def requests_csv(stats):
    from . import runners
    rows = [
     ','.join([
      '"Type"',
      '"Name"',
      '"# requests"',
      '"# failures"',
      '"Median response time"',
      '"Average response time"',
      '"Min response time"',
      '"Max response time"',
      '"Average Content Size"',
      '"Requests/s"',
      '"Requests Failed/s"',
      '"50%"',
      '"66%"',
      '"75%"',
      '"80%"',
      '"90%"',
      '"95%"',
      '"98%"',
      '"99%"',
      '"99.9%"',
      '"99.99%"',
      '"99.999"',
      '"100%"'])]
    for s in chain(sort_stats(stats.entries), [stats.total]):
        if s.num_requests:
            percentile_str = ','.join([str(int(s.get_response_time_percentile(x) or 0)) for x in PERCENTILES_TO_REPORT])
        else:
            percentile_str = ','.join(['"N/A"'] * len(PERCENTILES_TO_REPORT))
        rows.append('"%s","%s",%i,%i,%i,%i,%i,%i,%i,%.2f,%.2f,%s' % (
         s.method,
         s.name,
         s.num_requests,
         s.num_failures,
         s.median_response_time,
         s.avg_response_time,
         s.min_response_time or 0,
         s.max_response_time,
         s.avg_content_length,
         s.total_rps,
         s.total_fail_per_sec,
         percentile_str))

    return '\n'.join(rows)


def stats_history_csv_header():
    """Headers for the stats history CSV"""
    return ','.join(('"Type"', '"Name"', '"Timestamp"', '"# requests"', '"# failures"',
                     '"Requests/s"', '"Requests Failed/s"', '"Median response time"',
                     '"Average response time"', '"Min response time"', '"Max response time"',
                     '"Average Content Size"', '"50%"', '"66%"', '"75%"', '"80%"',
                     '"90%"', '"95%"', '"98%"', '"99%"', '"99.9%"', '"99.99%"', '"99.999"',
                     '"100%"')) + '\n'


def stats_history_csv(stats, stats_history_enabled=False, csv_for_web_ui=False):
    """Returns the Aggregated stats entry every interval"""
    if csv_for_web_ui:
        rows = [
         stats_history_csv_header()]
    else:
        rows = []
    timestamp = int(time.time())
    stats_entries_per_iteration = []
    if stats_history_enabled:
        stats_entries_per_iteration = sort_stats(stats.entries)
    for s in chain(stats_entries_per_iteration, [stats.total]):
        if s.num_requests:
            percentile_str = ','.join([str(int(s.get_current_response_time_percentile(x) or 0)) for x in PERCENTILES_TO_REPORT])
        else:
            percentile_str = ','.join(['"N/A"'] * len(PERCENTILES_TO_REPORT))
        rows.append('"%s","%s","%s",%i,%i,%.2f,%.2f,%i,%i,%i,%.2f,%.2f,%s' % (
         s.method,
         s.name,
         timestamp,
         s.num_requests,
         s.num_failures,
         s.current_rps,
         s.current_fail_per_sec,
         s.median_response_time,
         s.avg_response_time,
         s.min_response_time or 0,
         s.max_response_time,
         s.avg_content_length,
         percentile_str))

    return '\n'.join(rows)


def failures_csv(stats):
    """"Return the contents of the 'failures' tab as a CSV."""
    rows = [
     ','.join(('"Method"', '"Name"', '"Error"', '"Occurrences"'))]
    for s in sort_stats(stats.errors):
        rows.append('"%s","%s","%s",%i' % (
         s.method,
         s.name,
         s.error,
         s.occurrences))

    return '\n'.join(rows)