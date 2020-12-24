# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/dump_frames_on.py
# Compiled at: 2020-05-08 08:03:23
# Size of source mod 2**32: 1066 bytes
import signal, sys, types, typing as tp
try:
    SIG_TYPE = signal._SIG
except AttributeError:
    SIG_TYPE = int

def dump_frames_on(sig_no: SIG_TYPE, stack_frame: types.FrameType, output: tp.TextIO):
    from satella.instrumentation import Traceback
    output.write('Stack frame dump requested in response to signal %s\n' % (sig_no,))
    for frame_no, frame in sys._current_frames().items():
        output.write('For stack frame %s' % (frame_no,))
        tb = Traceback(frame)
        tb.pretty_print(output=output)

    output.write('End of stack frame dump\n')


def install_dump_frames_on(signal_number: SIG_TYPE, output: tp.TextIO=sys.stderr):
    """
    Instruct Python to dump all frames onto output, along with their local variables
    upon receiving given signal
    """
    signal.signal(signal_number, lambda sig_no, stack_frame: dump_frames_on(sig_no, stack_frame, output))