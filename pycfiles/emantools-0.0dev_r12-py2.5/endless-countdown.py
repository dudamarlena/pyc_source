# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emantools/endless-countdown.py
# Compiled at: 2008-01-29 13:05:01
from time import sleep
from daemon import Daemon
import countdown

class Countdown(Daemon):
    interval = 5

    def __init__(self):
        self.main()

    def run_script(self, num, *args):
        t = countdown.countdown(*args)
        fp = open('countdown%s.log' % num, 'w')
        fp.write(t + '\n')
        fp.close()

    def run(self):
        date = (2008, 10, 22, 4, 30)
        self.run_script(0, *date)
        sleep(3)
        self.run_script(1, *date)
        sleep(3)
        self.run_script(2, *date)
        sleep(3)


if __name__ == '__main__':
    Countdown()