# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/opacify/progress.py
# Compiled at: 2019-01-24 17:28:59
# Size of source mod 2**32: 2007 bytes
import sys, time
prev_tail = '|'
tail = '|'

def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', timer_start=None):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        timer_start - Optional  : for estimating remaining time (time.time())
    """
    global tail
    if tail == '.':
        tail = '*'
    else:
        tail = '.'
    estimate = None
    if timer_start:
        duration = time.time() - timer_start
        estimate = (1 + duration) / float(iteration + 1) * (total - iteration) / 60.0
    else:
        percent = ('{0:.' + str(decimals) + 'f}').format(100 * ((1 + iteration) / float(total + 1)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        if estimate:
            sys.stdout.write('\r%s |%s| %s %s%% %s  %.2fm remaining    \r' % (prefix, bar, tail, percent, suffix, estimate))
        else:
            sys.stdout.write('\r%s |%s| %s %s%% %s\r' % (prefix, bar, tail, percent, suffix))
    sys.stdout.flush()


# global prev_tail ## Warning: Unused global