# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/pbar_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--pbar', action='store_true', help='Show a progress bar')

def process_options(options):
    if options.pbar is not None:
        from testoob.reporting.progress_bar import ProgressBarReporter
        parsing.kwargs['reporters'].append(ProgressBarReporter())
    return


parsing.option_processors.append(process_options)