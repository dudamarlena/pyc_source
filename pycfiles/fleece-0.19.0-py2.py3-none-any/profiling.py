# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bruc5529/git/fleece/fleece/profiling.py
# Compiled at: 2019-11-06 12:49:13
from cProfile import Profile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from functools import wraps
from pstats import Stats
import random, re
from fleece import log
DEFAULT_LOGGER = log.getLogger('profiler')
RE_SUMMARY_LINE = re.compile('^\\s+(?P<total_calls>\\d+) function calls \\((?P<primitive_calls>\\d+) primitive calls\\) in (?P<total_time>\\d+\\.\\d+) seconds$')
RE_PROFILE_LINE = re.compile('^\\s+(?P<ncalls>\\d+)\\s+(?P<tottime>\\d+\\.\\d+)\\s+(?P<tpercall>\\d+\\.\\d+)\\s+(?P<cumtime>\\d+\\.\\d+)\\s+(?P<cpercall>\\d+\\.\\d+)\\s+(?P<filename>.*):(?P<lineno>\\d+)\\((?P<function>.*)\\)$')
PROFILE_SAMPLE = 0.5
DEFAULT_FILTER = [
 '/var/task/']
DEFAULT_LIMIT = 20

def process_profiling_data(stream, logger, event):
    profiling_data = []
    extra_dict = {}
    raw_string = stream.getvalue()
    lines = raw_string.split('\n')
    match_summary = RE_SUMMARY_LINE.match(lines[0])
    if match_summary is not None:
        extra_dict = match_summary.groupdict()
    for line in lines[1:]:
        match = RE_PROFILE_LINE.match(line)
        if match is not None:
            profiling_data.append(match.groupdict())

    logger.info('Profiling completed', lambda_event=event, profiling_data=profiling_data, **extra_dict)
    return


def profile_handler(sample=PROFILE_SAMPLE, stats_filter=None, stats_limit=DEFAULT_LIMIT, logger=DEFAULT_LOGGER):

    def decorator(func):

        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            if random.random() <= PROFILE_SAMPLE:
                print_stats_filter = stats_filter or DEFAULT_FILTER
                print_stats_filter.append(stats_limit)
                profile = Profile()
                profile.enable()
                try:
                    return_value = func(event, context, *args, **kwargs)
                finally:
                    profile.disable()
                    stream = StringIO()
                    stats = Stats(profile, stream=stream)
                    stats.sort_stats('cumulative')
                    stats.print_stats(*print_stats_filter)
                    process_profiling_data(stream, logger, event)

            else:
                logger.info('Skipping profiling')
                return_value = func(event, context, *args, **kwargs)
            return return_value

        return wrapper

    return decorator