# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: airrun/cli/__main__.py
# Compiled at: 2020-04-15 05:24:46
from airrun.cli.parser import get_parser

def main(argv=None):
    ap = get_parser()
    args = ap.parse_args(argv)
    if args.action == 'info':
        from airrun.cli.info import infos
        print infos
    elif args.action == 'report':
        from airrun.report.report import main as report_main
        report_main(args)
    elif args.action == 'run':
        from airrun.main import main as runner
        runner(args)
    elif args.action == 'version':
        from airrun.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()