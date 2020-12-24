# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/it.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 8790 bytes
from dexy.commands.utils import init_wrapper
from dexy.utils import defaults
from operator import attrgetter
import dexy.exceptions, os, subprocess, sys, time

def dexy_command(__cli_options, artifactsdir, conf, configs, debug, directory, dryrun, encoding, exclude, excludealso, full, globals, help, h, hashfunction, include, logdir, logfile, logformat, loglevel, nocache, noreports, outputroot, pickle, plugins, profile, r, recurse, reports, reset, silent, strace=Falsedefaults['artifacts_dir']defaults['config_file']defaults['configs']defaults['debug']defaults['directory']defaults['dry_run']defaults['encoding']defaults['exclude']defaults['exclude_also']defaults['full']defaults['globals']FalseFalsedefaults['hashfunction']defaults['include']defaults['log_dir']defaults['log_file']defaults['log_format']defaults['log_level']defaults['dont_use_cache']Falsedefaults['output_root']defaults['pickle']defaults['plugins']defaults['profile']Falsedefaults['recurse']defaults['reports']Falsedefaults['silent']defaults['strace'], uselocals=defaults['uselocals'], target=defaults['target'], version=False, writeanywhere=defaults['writeanywhere']):
    """
    Runs Dexy.
    """
    if not h:
        if help:
            return dexy.commands.help_command()
        if version:
            return dexy.commands.version_command()
        if r or reset:
            dexy.commands.dirs.reset_command(artifactsdir=artifactsdir, logdir=logdir)
        if silent:
            print('sorry, -silent option not implemented yet https://github.com/ananelson/dexy/issues/33')
    else:
        wrapper = init_wrapper(locals())
        wrapper.assert_dexy_dirs_exist()
        run_reports = not noreports
        try:
            if profile:
                run_dexy_in_profiler(wrapper, profile)
            else:
                if strace:
                    run_dexy_in_strace(wrapper, strace)
                    run_reports = False
                else:
                    start = time.time()
                    wrapper.run_from_new()
                    elapsed = time.time() - start
                    print('dexy run finished in %0.3f%s' % (elapsed, wrapper.state_message()))
        except dexy.exceptions.UserFeedback as e:
            try:
                handle_user_feedback_exception(wrapper, e)
            finally:
                e = None
                del e

        except KeyboardInterrupt:
            handle_keyboard_interrupt()
        except Exception as e:
            try:
                log_and_print_exception(wrapper, e)
                raise
            finally:
                e = None
                del e

        if run_reports and hasattr(wrapper, 'batch'):
            start_time = time.time()
            wrapper.report()
            print('dexy reports finished in %0.3f' % (time.time() - start_time))


it_command = dexy_command

def log_and_print_exception(wrapper, e):
    if hasattr(wrapper, 'log'):
        wrapper.log.error('An error has occurred.')
        wrapper.log.error(e)
        wrapper.log.error(e.message)
    import traceback
    traceback.print_exc()


def handle_user_feedback_exception(wrapper, e):
    if hasattr(wrapper, 'log'):
        wrapper.log.error('A problem has occurred with one of your documents:')
        wrapper.log.error(e.message)
    sys.stderr.write("ERROR: Oops, there's a problem processing one of your documents. Here is the error message:" + os.linesep)
    for line in e.message.splitlines():
        sys.stderr.write('  ' + line + '\n')

    if not e.message.endswith(os.linesep) or e.message.endswith('\n'):
        sys.stderr.write(os.linesep)


def handle_keyboard_interrupt():
    sys.stderr.write("\n    ok, stopping your dexy run\n    you might want to 'dexy reset' before running again\n")
    sys.exit(1)


def run_dexy_in_profiler(wrapper, profile):
    if isinstance(profile, bool):
        profile_filename = os.path.join(wrapper.artifacts_dir, 'dexy.prof')
    else:
        profile_filename = profile
    import cProfile
    print('running dexy with cProfile, writing profile data to %s' % profile_filename)
    cProfile.runctx('wrapper.run_from_new()', None, locals(), profile_filename)
    import pstats
    stats_output_file = os.path.join(wrapper.artifacts_dir, 'profile-report.txt')
    with open(stats_output_file, 'w') as (f):
        stat = pstats.Stats(profile_filename, stream=f)
        stat.sort_stats('cumulative')
        stat.print_stats()
    print('Report is in %s, profile data is in %s.' % (stats_output_file, profile_filename))


def run_dexy_in_strace(wrapper, strace):
    if isinstance(strace, bool):
        strace_filename = 'dexy.strace'
    else:
        strace_filename = strace

    def run_command(command):
        proc = subprocess.Popen(command,
          shell=True,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        stdout, stderr = proc.communicate()
        print(stdout)

    commands = (
     'strace dexy --reports "" 2> %s' % strace_filename,
     'echo "calls to stat:" ; grep "^stat(" %s | wc -l' % strace_filename,
     'echo "calls to read:" ; grep "^read(" %s | wc -l' % strace_filename,
     'echo "calls to write:" ; grep "^write(" %s | wc -l' % strace_filename,
     'grep "^stat(" %s | sort | uniq -c | sort -r -n > strace-stats.txt' % strace_filename,
     'grep "^read(" %s | sort | uniq -c | sort -r -n > strace-reads.txt' % strace_filename,
     'grep "^write(" %s | sort | uniq -c | sort -r -n > strace-writes.txt' % strace_filename)
    for command in commands:
        run_command(command)


def targets_command(full=False, **kwargs):
    """
    Prints a list of available targets, which can be run via "dexy -target name".
    """
    wrapper = init_wrapper(locals())
    wrapper.assert_dexy_dirs_exist()
    wrapper.to_valid()
    wrapper.to_walked()
    print('Targets you can pass to -target option:')
    for doc in sorted((wrapper.bundle_docs()), key=(attrgetter('key'))):
        print('  ', doc.key)

    if full:
        print()
        print('These targets are also available, with lower priority:')
        for doc in sorted((wrapper.non_bundle_docs()), key=(attrgetter('key'))):
            print('  ', doc.key)

        print()
        print('Target names can be matched exactly or with the first few characters,\nin which case all matching targets will be run.')
    else:
        print()
        print('Run this command with --full option for additional available target names.')