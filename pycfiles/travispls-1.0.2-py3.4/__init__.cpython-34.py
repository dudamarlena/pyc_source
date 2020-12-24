# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/travispls/__init__.py
# Compiled at: 2017-03-10 16:06:34
# Size of source mod 2**32: 2629 bytes
from datetime import datetime
from datetime import timedelta
import argparse, os, signal, subprocess, sys

class AnsiColors:
    CLEAR = '\x1b[0m'
    BOLD_YELLOW = '\x1b[1;33m'
    BOLD_RED = '\x1b[1;31m'

    @classmethod
    def enabled(cls):
        """Are both standard output and standard error TTYs?"""
        return os.isatty(sys.stdout.fileno()) and os.isatty(sys.stderr.fileno())


def main():
    """Runs a command in Travis, periodically interrupting the output."""
    parser = argparse.ArgumentParser(description='Periodically disturbs Travis to allow long-running builds with stalled output.')
    parser.add_argument('-i', '--interval', type=int, default=540, help='Disturbance interval.')
    parser.add_argument('-m', '--max-timeout', type=int, default=3600, help='The maximum allowed run time in order to be a good internet citizen.')
    parser.add_argument('command', help='The command to run.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command.')
    args = parser.parse_args()
    if args.max_timeout > 0:
        end_of_line = datetime.utcnow() + timedelta(seconds=args.max_timeout)
    p = subprocess.Popen([args.command] + args.args)
    signal.signal(signal.SIGTERM, lambda sig, frame: stop_process(p, sig))
    try:
        while p.returncode is None:
            try:
                p.wait(args.interval)
                break
            except subprocess.TimeoutExpired:
                if end_of_line:
                    if datetime.utcnow() > end_of_line:
                        log('ERROR: max timeout of {} seconds exceeded.'.format(args.max_timeout), sys.stderr, AnsiColors.BOLD_RED)
                        stop_process(p)
                disturb()

    except KeyboardInterrupt:
        stop_process(p)

    sys.exit(p.returncode)


def stop_process(process, sig=signal.SIGTERM):
    """Stops a process and exits with its return code."""
    process.send_signal(sig)
    process.wait()
    sys.exit(process.returncode)


def disturb():
    """Disturb standard error."""
    log('travis pls', sys.stderr, AnsiColors.BOLD_YELLOW)


def log(message, output=sys.stdout, color=AnsiColors.CLEAR):
    """Log things"""
    output.write('{prefix}{message}{postfix}\n'.format(prefix=color if AnsiColors.enabled() else '', message=message, postfix=AnsiColors.CLEAR if AnsiColors.enabled() else ''))


if __name__ == '__main__':
    main()