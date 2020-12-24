# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tsenum/__main__.py
# Compiled at: 2019-11-15 16:07:43
# Size of source mod 2**32: 1551 bytes
import argparse, sys, tsenum
from datetime import datetime, timedelta, timezone

def main():
    parser = argparse.ArgumentParser(prog='tsenum',
      description=(tsenum.__doc__),
      epilog=('tsenum v%s, Copyright (C) 2019 %s <%s> Licensed under %s. See source distribution for detailed copyright notices.' % (tsenum.__version__, tsenum.__author__, tsenum.__email__, tsenum.__license__)))
    parser.add_argument('-u',
      '--utc', help='Current time is in UTC',
      dest='utc',
      action='store_true',
      default=False)
    parser.add_argument('-o',
      '--offset', help='Offset to enumerate from',
      dest='offset',
      type=int,
      required=True)
    parser.add_argument('-c',
      '--count', help='Count to enumerate',
      dest='count',
      type=int,
      required=True)
    parser.add_argument('-s',
      '--step', help='Step width',
      dest='step',
      choices=[
     tsenum.STEP_WEEK,
     tsenum.STEP_DAY,
     tsenum.STEP_HOUR,
     tsenum.STEP_MINUTE,
     tsenum.STEP_SECOND],
      type=str,
      required=True)
    parser.add_argument('-p',
      '--pattern', help="Date pattern to use (see Python's strftime in datetime)",
      dest='pattern',
      type=str,
      required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        if args.utc:
            now = datetime.utcnow()
        else:
            now = datetime.now().astimezone()
    for i in tsenum.enumerate_times(now, args.offset, args.count, args.step, args.pattern):
        print(i)

    sys.exit(0)


if __name__ == '__main__':
    main()