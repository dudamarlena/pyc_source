# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/frame.py
# Compiled at: 2017-10-27 23:34:05
from trepan.processor import cmdfns as Mcmdfns
from trepan.lib import complete as Mcomplete

def frame_low_high(proc_obj, direction):
    stack_size = len(proc_obj.stack)
    if direction is None:
        return [
         -stack_size, stack_size - 1]
    else:
        frame_index = proc_obj.curindex
        low, high = frame_index * -direction, (stack_size - frame_index - 1) * direction
        if direction < 0:
            low, high = high, low
        return (
         low, high)
    return


def frame_complete(proc_obj, prefix, direction):
    (low, high) = frame_low_high(proc_obj, direction)
    ary = [ str(low + i) for i in range(high - low + 1) ]
    return Mcomplete.complete_token(ary, prefix)


def frame_num(proc_obj, pos):
    return len(proc_obj.stack) - pos - 1


def adjust_frame(proc_obj, name, pos, absolute_pos):
    """Adjust stack frame by pos positions. If absolute_pos then
    pos is an absolute number. Otherwise it is a relative number.

    A negative number indexes from the other end."""
    if not proc_obj.curframe:
        proc_obj.errmsg('No stack.')
        return
    if absolute_pos:
        if pos >= 0:
            pos = frame_num(proc_obj, pos)
        else:
            pos = -pos - 1
    else:
        pos += proc_obj.curindex
    if pos < 0:
        proc_obj.errmsg('Adjusting would put us beyond the oldest frame.')
        return
    elif pos >= len(proc_obj.stack):
        proc_obj.errmsg('Adjusting would put us beyond the newest frame.')
        return
    proc_obj.curindex = pos
    proc_obj.curframe = proc_obj.stack[proc_obj.curindex][0]
    proc_obj.location()
    proc_obj.list_lineno = None
    proc_obj.list_offset = proc_obj.curframe.f_lasti
    proc_obj.list_object = proc_obj.curframe
    proc_obj.list_filename = proc_obj.curframe.f_code.co_filename
    return


def adjust_relative(proc_obj, name, args, signum):
    if not proc_obj.stack:
        proc_obj.errmsg('Program has no stack frame set.')
        return False
    if len(args) == 1:
        count = 1
    else:
        count_str = args[1]
        (low, high) = frame_low_high(proc_obj, signum)
        count = Mcmdfns.get_an_int(proc_obj.errmsg, count_str, ("The '%s' command argument must eval to" + ' an integer. Got: %s') % (name, count_str), low, high)
        if count is None:
            return
    adjust_frame(proc_obj, name, pos=signum * count, absolute_pos=False)
    return