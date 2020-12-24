# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/data/fake_pipeline_prog.py
# Compiled at: 2009-12-08 17:43:30
"""
Fake nl_parser / nl_loader for
testing the nl_pipeline.
"""
import logging, os, signal, sys, time
from netlogger.nllog import get_logger, OptionParser
from netlogger.pipeline import PipelineApplication
options = None
dir = os.path.dirname(sys.argv[0])
prog = os.path.basename(sys.argv[0])

def on_term(signo, frame):
    log = get_logger(__file__)
    log.info('terminated', signo=signo)
    sys.exit(0)


signal.signal(signal.SIGTERM, on_term)

def parse_args():
    """
    Just enough of the args that parser and loader take to fake out
    the pipeline.
    """
    global options
    parser = OptionParser(description=(' ').join(__doc__.split()))
    parser.add_option('-c', '--config', action='store', dest='config', default=None, metavar='FILE', help='use configuration in FILE')
    parser.add_option('-d', '--daemon', action='store_true', dest='daemon', help='run in daemon mode')
    (options, args) = parser.parse_args()
    return


def main():
    parse_args()
    log = get_logger(__file__)
    log.info('run.start')
    fakePipelineApp = PipelineApplication()
    while True:
        time.sleep(1)

    log.info('run.end', status=0)
    return 0


if __name__ == '__main__':
    sys.exit(main())