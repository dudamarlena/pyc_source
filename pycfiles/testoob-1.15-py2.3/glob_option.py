# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/glob_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--glob', metavar='PATTERN', help='Filtering glob pattern')

def process_options(options):
    if options.glob is not None:
        from testoob.extracting import glob
        parsing.kwargs['extraction_decorators'].append(glob(options.glob))
    return


parsing.option_processors.append(process_options)