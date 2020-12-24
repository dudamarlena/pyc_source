# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/factory.py
# Compiled at: 2013-05-21 04:52:29
import telnetlib, sys, getopt, time, os, termios, fcntl
from beanstalkdstats import BeanstalkdStats
from beanstalkd import Beanstalkd
from console import Console
from clock import Clock
from charreader import CharReader
from screenprinter import ScreenPrinter
from arguments import Arguments

def create_arguments_parser():
    return Arguments(sys, getopt)


def start_application(host, port):
    telnet = telnetlib.Telnet()
    beanstalkd = Beanstalkd(telnet, host, port)
    stats = BeanstalkdStats(beanstalkd)
    char_reader = CharReader(os, sys, termios, fcntl)
    screen_printer = ScreenPrinter(os, sys)
    console = Console(Clock(time), char_reader, screen_printer, stats)
    return (beanstalkd, console)