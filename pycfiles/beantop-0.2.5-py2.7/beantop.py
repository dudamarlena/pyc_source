# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/beantop.py
# Compiled at: 2013-06-04 05:00:53
from . import factory
import sys

def main():
    arguments = factory.create_arguments_parser()
    host, port = arguments.process(sys.argv[1:])
    beanstalkd, console = factory.start_application(host, port)
    beanstalkd.connect()
    console.main_loop()