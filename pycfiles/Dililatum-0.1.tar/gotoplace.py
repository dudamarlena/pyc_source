# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niels/Programming/Dililatum/debugtests/gotoplace.py
# Compiled at: 2010-07-11 21:49:58


def goto(event):
    game = event.args[0]
    sys = game.sys
    sys.signalactions.clear('beforeworldrun')
    try:
        plcnum = int(sys.etc.arguments[0])
    except IndexError:
        plcnum = 0

    try:
        pos = eval('[' + sys.etc.arguments[1] + ']')
    except Exception:
        pos = None

    game.world.set_place(plcnum, pos)
    return


def main():
    action('beforegamerun', goto)