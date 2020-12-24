# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\progress_bar.py
# Compiled at: 2015-01-12 09:34:30
# Size of source mod 2**32: 499 bytes
import threading, time, sys
done = False

def progressBar(l=[
 '|', '/', '-', '\\', 0]):
    global done
    while not done:
        sys.stdout.write('\r{}\r'.format(l[l[(-1)]]))
        l[-1] = (l[(-1)] + 1) % (len(l) - 1)
        time.sleep(0.4)


def progress_bar2():
    while not done:
        sys.stdout.write('.')
        time.sleep(1)


def run():
    t = threading.Thread(target=progress_bar2)
    t.setDaemon(1)
    t.start()


def stop():
    global done
    done = True