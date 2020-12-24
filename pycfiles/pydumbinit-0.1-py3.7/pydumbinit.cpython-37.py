# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pydumbinit.py
# Compiled at: 2019-05-11 23:51:07
# Size of source mod 2**32: 4331 bytes
"""PyDumbInit

Simple init system that uses signal proxiying for managining children. Inspired from yelp/dumb-init
"""
import fcntl, logging, os, signal, subprocess, sys, termios
MAXSIG = 31
SIGMAP = dict.fromkeys(range(1, MAXSIG + 1), -1)
IGNORED_SIGMAP = dict.fromkeys(range(MAXSIG), False)
child_pid = -1
use_setsid = 1
logger = logging.getLogger()

def translate_signal(signum: int) -> int:
    if SIGMAP.get(signum, -1) > 0:
        res = SIGMAP[signum]
        logger.info(f"Translating signal {signum} to {res}")
        return res
    return signum


def forward_signal(signum: int) -> None:
    signum = translate_signal(signum)
    if signum != 0:
        os.kill(-child_pid if use_setsid else child_pid, signum)
        logger.info(f"Forwarded signal {signum} to children.")
    else:
        logger.info(f"Not forwarding signal {signum} to children (ignored).")


def handle_signal(signum: int) -> None:
    logger.info(f"Received signal {signum}")
    if IGNORED_SIGMAP[signum]:
        logger.info(f"Ignoring tty hand-off signal {signum}")
        IGNORED_SIGMAP[signum] = False
    else:
        if signum == signal.SIGCHLD:
            killed_pid, status = os.waitpid(-1, os.WNOHANG)
            while killed_pid > 0:
                if os.WIFEXITED(status):
                    exit_status = os.WEXITSTATUS(status)
                    logger.info(f"A child with PID {killed_pid} exited with exit status {exit_status}.")
                else:
                    assert os.WIFSIGNALED(status)
                    exit_status = 128 + os.WTERMSIG(status)
                    logger.info(f"A child with PID {killed_pid} was terminated by signal {exit_status - 128}.")
                if killed_pid == child_pid:
                    forward_signal(signal.SIGTERM)
                    logger.info(f"Child exited with status {exit_status}. Goodbye.")
                    sys.exit(exit_status)
                killed_pid, status = os.waitpid(-1, os.WNOHANG)

        else:
            forward_signal(signum)
            if signum in {signal.SIGTSTP, signal.SIGTTOU, signal.SIGTTIN}:
                logger.info('Suspending self due to TTY signal.')
                os.kill(os.getpid(), signal.SIGSTOP)


def parse_rewrite_signum--- This code section failed: ---

 L.  76         0  SETUP_EXCEPT         64  'to 64'

 L.  77         2  LOAD_FAST                'arg'
                4  LOAD_METHOD              split
                6  LOAD_STR                 ':'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'signum'
               14  STORE_FAST               'replacement'

 L.  78        16  LOAD_FAST                'signum'
               18  LOAD_CONST               1
               20  COMPARE_OP               <
               22  POP_JUMP_IF_TRUE     48  'to 48'
               24  LOAD_FAST                'signum'
               26  LOAD_GLOBAL              MAXSIG
               28  COMPARE_OP               >
               30  POP_JUMP_IF_TRUE     48  'to 48'
               32  LOAD_FAST                'replacement'
               34  LOAD_CONST               0
               36  COMPARE_OP               <
               38  POP_JUMP_IF_TRUE     48  'to 48'
               40  LOAD_FAST                'replacement'
               42  LOAD_GLOBAL              MAXSIG
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE    52  'to 52'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            30  '30'
             48_2  COME_FROM            22  '22'

 L.  79        48  LOAD_GLOBAL              ValueError
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            46  '46'

 L.  80        52  LOAD_FAST                'replacement'
               54  LOAD_GLOBAL              SIGMAP
               56  LOAD_FAST                'signum'
               58  STORE_SUBSCR     
               60  POP_BLOCK        
               62  JUMP_FORWARD         94  'to 94'
             64_0  COME_FROM_EXCEPT      0  '0'

 L.  81        64  DUP_TOP          
               66  LOAD_GLOBAL              ValueError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    92  'to 92'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L.  82        78  LOAD_GLOBAL              logger
               80  LOAD_METHOD              error
               82  LOAD_STR                 'Incorrect rewrite format'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_TOP          
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            70  '70'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            62  '62'

Parse error at or near `COME_FROM' instruction at offset 52_0


def set_rewrite_to_sigstop_if_not_defined(signum: int) -> None:
    if SIGMAP[signum] == -1:
        SIGMAP[signum] = signal.SIGSTOP


def dummy(*args):
    pass


def register_signals() -> None:
    for i in range(1, MAXSIG + 1):
        if i in {9, 19}:
            continue
        signal.signal(i, dummy)


def run(program, *args):
    register_signals()
    if fcntl.ioctl(0, termios.TIOCNOTTY) == -1:
        logger.warn('Unable to detach from controlling tty')
    else:
        if os.getsid(0) == os.getpid():
            logger.info('Detached from controlling tty, ignoring the first SIGHUP and SIGCONT we receive')
            IGNORED_SIGMAP[signal.SIGHUP] = 1
            IGNORED_SIGMAP[signal.SIGCONT] = 1
        else:
            logger.info('Detached from controlling tty, but was not session leader.')
    child_pid = os.fork()
    if child_pid < 0:
        logger.error('Unable to fork. Exiting.')
        return 1
    if child_pid == 0:
        if use_setsid:
            os.setsid()
        os.execvp(program, args)
        return 2
    logger.info(f"Child spawned with PID {child_pid}.")
    while True:
        signum = signal.sigwait(set(SIGMAP.keys()))
        handle_signal(signum)


def main(args):
    cmd, *args = args
    cmd = cmd.strip('--')
    if cmd == 'run':
        sys.exit(run(*args))


def test_translate_signal():
    assert translate_signal(5) == 5
    SIGMAP[14] = 3
    assert translate_signal(14) == 3
    assert translate_signal(-1) == -1


def test_rewrite_parsing():
    parse_rewrite_signum('5:6')
    assert SIGMAP[5] == 6


def test_forward_signal() -> None:
    print('NO, It works well')


if __name__ == '__main__':
    main(sys.argv[1:])