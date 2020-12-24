# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mengwei/workspace/mine/airtest_run/airrun/cli/__main__.py
# Compiled at: 2020-04-15 05:24:46
# Size of source mod 2**32: 640 bytes
from airrun.cli.parser import get_parser

def main(argv=None):
    ap = get_parser()
    args = ap.parse_args(argv)
    if args.action == 'info':
        from airrun.cli.info import infos
        print(infos)
    elif args.action == 'report':
        import airrun.report.report as report_main
        report_main(args)
    elif args.action == 'run':
        import airrun.main as runner
        runner(args)
    elif args.action == 'version':
        from airrun.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()