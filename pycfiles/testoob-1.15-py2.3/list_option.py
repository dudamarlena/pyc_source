# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/list_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('-l', '--list', action='store_true', help='List the test classes and methods found')
parsing.parser.add_option('--list-formatted', metavar='FORMATTER', help="Like option '-l', just formatted (e.g. csv).")

def process_options(options):
    from testoob.running import ListingRunner
    if options.list_formatted:
        parsing.kwargs['runner'] = ListingRunner(output_format=options.list_formatted)
    elif options.list is not None:
        parsing.kwargs['runner'] = ListingRunner()
    return


parsing.option_processors.append(process_options)