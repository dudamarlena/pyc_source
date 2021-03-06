# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/poly/watch.py
# Compiled at: 2005-12-13 12:18:53
from __future__ import division
__version__ = '$Revision: 1.10 $'
import commands, exceptions, itertools, os, sys, time
from autolog import autolog
import optbuild, tabdelim
_log = autolog()
LSPLACE_PROGRAM = optbuild.OptionBuilder_ShortOptWithSpace('lsplace')
BMOD_PROGRAM = optbuild.OptionBuilder_ShortOptWithSpace('bmod')
BJOBS_PROGRAM = optbuild.OptionBuilder_ShortOptWithSpace('bjobs')
JOB_SLOT_STEP = 1
SLEEP_TIME = 60

def increase_slot_limit(jobid):
    output = BJOBS_PROGRAM.getoutput(str(jobid), A=True, w=True)
    lines = output.splitlines()
    assert len(lines) <= 2
    if len(lines) < 2:
        return
    reader = tabdelim.DictReader(lines, delimiter=' ', skipinitialspace=True)
    jobinfo = reader.next()
    try:
        slot_limit = int(jobinfo['ARRAY_SPEC'].split('%')[1])
        running = int(jobinfo['RUN'])
        pending = int(jobinfo['PEND'])
    except KeyError:
        _log.error('abnormal bjobs output: %s', output)
        return

    if pending == 0:
        _log.info('no pending jobs left')
        sys.exit(0)
    if slot_limit - running < JOB_SLOT_STEP:
        new_slot_limit = slot_limit + JOB_SLOT_STEP
        try:
            BMOD_PROGRAM.run(str(jobid), J='%%%d' % new_slot_limit)
        except optbuild.ReturncodeError, err:
            _log.info('bmod returned %s', err.returncode)
        else:
            _log.info('%s job slot limit now %s', jobid, new_slot_limit)
    else:
        _log.info('%s job slot limit %s but only %s jobs running', jobid, slot_limit, running)


def watch(jobid, hostgroups=None, sleep_time=None):
    if hostgroups is None:
        hostgroups = get_default_hostgroups()
    if sleep_time is None:
        try:
            sleep_time = float(os.environ['POLYWATCH_SLEEP_TIME'])
        except KeyError:
            sleep_time = SLEEP_TIME

    while True:
        time.sleep(sleep_time)
        for hostgroup in hostgroups:
            try:
                output = LSPLACE_PROGRAM.getoutput(*hostgroup)
            except optbuild.ReturncodeError, err:
                if err.returncode != 1:
                    _log.die('lsplace error; return code %s')
                comma_hostgroups = (',').join(hostgroup)
                _log.info('%s not ready; lsplace return code %s', comma_hostgroups, err.returncode)
                break

        else:
            increase_slot_limit(jobid)

    return


def comma_split(text):
    return text.split(',')


def parse_options(args):
    global options
    from optparse import OptionParser
    usage = '%prog [OPTION]...'
    version = '%%prog %s' % __version__
    parser = OptionParser(usage=usage, version=version)
    (options, args) = parser.parse_args(args)
    return args


def parse_hostgroups(texts):
    return map(comma_split, texts)


def get_default_hostgroups():
    try:
        texts = os.environ['POLYWATCH_HOSTS'].split(' ')
    except KeyError:
        raise RuntimeError, 'no hosts to watch specified'

    return parse_hostgroups(texts)


def main(args):
    args = parse_options(args)
    if args[1:]:
        hostgroups = parse_hostgroups(args[1:])
    else:
        hostgroups = None
    try:
        watch(int(args[0]), hostgroups)
    except KeyboardInterrupt:
        return 2

    return


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))