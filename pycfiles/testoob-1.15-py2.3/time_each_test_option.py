# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/time_each_test_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--time-each-test', action='store_true', help='Report the total time for each test')

def process_options(options):
    import testoob.reporting.options
    testoob.reporting.options.time_each_test = options.time_each_test


parsing.option_processors.append(process_options)