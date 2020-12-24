# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hk3380/projects/ding/.env/lib/python3.5/site-packages/ding/ding.py
# Compiled at: 2016-10-28 16:53:08
# Size of source mod 2**32: 4914 bytes
"""Simple CLI beep tool"""
from __future__ import unicode_literals
from __future__ import print_function
import re, os, sys, time, datetime, argparse
VERSION = '2.1.0'
N_BEEPS = 4
WAIT_BEEPS = 0.15

def relative_time(arg):
    """Validate user provided relative time"""
    if not re.match('\\d+[smh]( +\\d+[smh])*', arg):
        raise argparse.ArgumentTypeError('Invalid time format: {}'.format(arg))
    return arg


def absolute_time(arg):
    """Validate user provided absolute time"""
    if not all([t.isdigit() for t in arg.split(':')]):
        raise argparse.ArgumentTypeError('Invalid time format: {}'.format(arg))
    try:
        datetime.time(*map(int, arg.split(':')))
    except ValueError as e:
        raise argparse.ArgumentTypeError('Invalid time format: {}'.format(e))

    return arg


def get_args(args):
    """Parse commandline arguments"""
    parent_parser = argparse.ArgumentParser(add_help=False, description='Lightweight time management CLI tool')
    parent_parser.add_argument('-n', '--no-timer', action='store_true', help='Hide the countdown timer')
    parent_parser.add_argument('-c', '--command', type=str, help='Use a custom command instead of the default beep')
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.required = True
    parser_in = subparsers.add_parser('in', parents=[parent_parser])
    parser_in.add_argument('time', nargs='+', type=relative_time, help='relative time \\d+[smh]( +\\d+[smh])* (e.g. 1h 30m)')
    parser_every = subparsers.add_parser('every', parents=[parent_parser])
    parser_every.add_argument('time', nargs='+', type=relative_time, help='relative time \\d+[smh]( +\\d+[smh])* (e.g. 2m 15s)')
    parser_at = subparsers.add_parser('at', parents=[parent_parser])
    parser_at.add_argument('time', type=absolute_time, help='absolute time [hh:[mm[:ss]]]')
    return parser.parse_args(args)


class TimeParser:
    __doc__ = 'Class helping with parsing user provided time into seconds'
    time_map = {'s': 1, 
     'm': 60, 
     'h': 3600}

    def __init__(self, time, relative):
        self.time = time
        self.relative = relative

    def get_seconds(self):
        if self.relative:
            return self._get_seconds_relative()
        return self._get_seconds_absolute()

    def _get_seconds_relative(self):
        return sum([self.time_map[t[(-1)]] * int(t[:-1]) for t in self.time])

    def _get_seconds_absolute(self):
        now = datetime.datetime.now()
        user_time = datetime.datetime.combine(datetime.date.today(), datetime.time(*map(int, self.time.split(':'))))
        if user_time > now:
            return (user_time - now).seconds
        return (user_time + datetime.timedelta(days=1) - now).seconds


def countdown(seconds, notimer=False):
    """Countdown for `seconds`, printing values unless `notimer`"""
    if not notimer:
        os.system('cls' if os.name == 'nt' else 'clear')
    while seconds > 0:
        start = time.time()
        if not notimer:
            print(datetime.timedelta(seconds=seconds), end='')
            sys.stdout.flush()
        seconds -= 1
        time.sleep(1 - time.time() + start)
        if not notimer:
            print(end='\r')


def beep(seconds, command):
    """Make the beep noise"""
    for _ in range(N_BEEPS):
        if command:
            os.system(command)
        else:
            sys.stdout.write('\x07')
            sys.stdout.flush()
        time.sleep(WAIT_BEEPS)


def parse_time(args):
    """Figure out the number of seconds to wait"""
    relative = args.mode == 'in' or args.mode == 'every'
    parser = TimeParser(args.time, relative)
    return parser.get_seconds()


def main(args=sys.argv[1:]):
    args = get_args(args)
    while True:
        try:
            seconds = parse_time(args)
            countdown(seconds, args.no_timer)
            beep(seconds, args.command)
            if args.mode != 'every':
                pass
            break
        except KeyboardInterrupt:
            print()
            break


if __name__ == '__main__':
    main()