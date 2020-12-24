# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: animate.py
# Compiled at: 2019-12-25 08:25:01
import itertools, threading, time, sys, os
stop = False

def animate():
    stop = False
    for c in itertools.cycle(['\x1b[1;31m•    \x1b[1;36m|', '\x1b[1;32m••   \x1b[1;36m/', '\x1b[1;34m•••  \x1b[1;36m-', '\x1b[1;35m•••• \x1b[1;36m\\']):
        if stop == True:
            stop = False
            return
            break
        else:
            sys.stdout.write('\r\x1b[1;32mloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)


def star(text):
    text = text.upper()
    teln = len(text) - 1
    lo = 0
    stop = False
    while True:
        if stop == True:
            stop = False
            print 'h'
            break
        else:
            tek = text[:lo] + text[lo].swapcase() + text[lo + 1:]
            sys.stdout.write('\r\x1b[1;32m[+]\x1b[1;33m ' + tek)
            sys.stdout.flush()
            time.sleep(0.2)
            lo -= -1
            if lo > teln:
                lo = 0

    print '\n'


def start(tup):
    stop = False
    while stop == True:
        print 'hj'
        t.exit()
        stop = False
        break

    if not stop:
        t = threading.Thread(target=star, args=(tup,))
        t.daemon = True
        t.start()


def anim():
    b = threading.Thread(target=animate)
    b.daemon = True
    b.start()
    time.sleep(1)