# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/sum_timelog.py
# Compiled at: 2014-03-25 00:37:36
"""
Prints the sum of a timelog in hours.
"""
import datetime, benchline.args, six

def parse_times(line_str):
    """
    >>> parse_times("Mar 11: IN - 06:48 AM OUT - 05:28 PM")
    ('06:48 AM', '05:28 PM')
    """
    first_part, time_out_str = line_str.split(' OUT - ')
    time_in_str = first_part.split(' IN - ')[1]
    return (time_in_str, time_out_str)


def time_str_2_time(time_str):
    """
    >>> time_str_2_time("06:48 AM")
    datetime.datetime(1900, 1, 1, 6, 48)
    """
    return datetime.datetime.strptime(time_str, '%I:%M %p')


def time_delta_2_hours(time_delta):
    """
    >>> time_delta_2_hours(datetime.timedelta(0, 1800))  # 1800 seconds = 30 minutes
    0.5
    """
    return time_delta.seconds / float(3600)


def line2hours(line_str):
    """
    >>> line2hours("Mar 11: IN - 06:48 AM OUT - 05:28 PM")
    10.666666666666666
    """
    time_in, time_out = map(time_str_2_time, parse_times(line_str))
    delta = time_out - time_in
    return time_delta_2_hours(delta)


def validate_args(parser, options, args):
    if len(args) == 0:
        parser.error('The first argument must be the filename of the zylun timelog.')


def get_lines(file_name_str):
    """
    >>> get_lines("benchline/test/test_timelog.txt")
    ['Mar 11: IN - 06:48 AM OUT - 05:28 PM', 'Mar 12: IN - 06:56 AM OUT - 04:20 PM', 'Mar 13: IN - 06:58 AM OUT - 05:15 PM', 'Mar 14: IN - 06:58 AM OUT - 04:52 PM', 'Mar 15: IN - 06:56 AM OUT - 05:31 PM']
    """
    f = open(file_name_str)
    return [ line[:-1] for line in f.readlines() ]


def main():
    options, args = benchline.args.go(usage='usage: %%prog [options] timelog_file\n%s' % __doc__, validate_args=validate_args)
    lines = get_lines(args[0])
    hours = map(line2hours, lines)
    six.print_(reduce(lambda x, y: x + y, hours))


if __name__ == '__main__':
    main()