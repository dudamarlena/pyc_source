# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/html_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--html', metavar='FILE', help='output results in HTML')

def process_options(options):
    if options.html is not None:
        parsing.require_modules('--html', 'Ft.Xml')
        from testoob.reporting import HTMLReporter
        parsing.kwargs['reporters'].append(HTMLReporter(filename=options.html))
    return


parsing.option_processors.append(process_options)