# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/hours_seconds_2_hours.py
# Compiled at: 2014-03-24 23:34:48
"""
Converts hours and seconds like 10:11 to
hours (decimal).
"""
import six, benchline.args

def mins2hours(minute_str):
    """
    >>> mins2hours("30")
    0.5
    """
    return float(minute_str) / 60.0


def hours_mins_2_hours(hours_minutes_str):
    """
    >>> hours_mins_2_hours("10:30")
    10.5
    """
    hour_str, minute_str = hours_minutes_str.split(':')
    return int(hour_str) + mins2hours(minute_str)


def validate_args(parser, options, args):
    if len(args) == 0:
        parser.error("The first argument must be hours and seconds like '10:11'")


def main():
    options, args = benchline.args.go(__doc__, validate_args=validate_args)
    six.print_(hours_mins_2_hours(args[0]))


if __name__ == '__main__':
    main()