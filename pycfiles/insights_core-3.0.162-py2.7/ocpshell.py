# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/ocpshell.py
# Compiled at: 2019-12-13 11:35:35
import argparse, logging
from insights.ocp import analyze
log = logging.getLogger(__name__)
banner = '\nOpenshift Configuration Explorer\n\nTutorial: https://github.com/RedHatInsights/insights-core/blob/master/docs/notebooks/Parsr%20Query%20Tutorial.ipynb\n\nconf is the top level configuration. Use conf.get_keys() to see first level keys.\n\nAvailable Predicates\n    lt, le, eq, gt, ge\n\n    isin, contains\n\n    startswith, endswith, matches\n\n    ieq, icontains, istartswith, iendswith\n\nAvailable Operators\n    ~ (not)\n    | (or)\n    & (and)\n\nExample\n    api = conf.where("kind", "KubeAPIServer")\n    latest = api.status.latestAvailableRevision.value\n    api.status.nodeStatuses.where("currentRevision", ~eq(latest))\n'

def parse_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('archives', nargs='+', help='Archive or directory to analyze.')
    p.add_argument('-D', '--debug', help='Verbose debug output.', action='store_true')
    p.add_argument('--exclude', default='*.log', help='Glob patterns to exclude separated by commas')
    return p.parse_args()


def parse_exclude(exc):
    return [ e.strip() for e in exc.split(',') ]


def main():
    args = parse_args()
    archives = args.archives
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    excludes = parse_exclude(args.exclude) if args.exclude else ['*.log']
    conf = analyze(archives, excludes)
    from insights.parsr.query import lt, le, eq, gt, ge, isin, contains, startswith, endswith, ieq, icontains, istartswith, iendswith, matches, make_child_query
    q = make_child_query
    import IPython
    from traitlets.config.loader import Config
    IPython.core.completer.Completer.use_jedi = False
    c = Config()
    c.TerminalInteractiveShell.banner1 = banner
    IPython.start_ipython([], user_ns=locals(), config=c)


if __name__ == '__main__':
    main()