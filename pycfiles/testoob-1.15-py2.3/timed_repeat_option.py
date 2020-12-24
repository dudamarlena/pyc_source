# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/timed_repeat_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--timed-repeat', metavar='SECONDS', type='float', help='Repeat each test, for a limited time')

def process_options(options):
    if options.timed_repeat is not None:
        from testoob.running import fixture_decorators
        parsing.kwargs['fixture_decorators'].append(fixture_decorators.get_timed_fixture(options.timed_repeat))
    return


parsing.option_processors.append(process_options)